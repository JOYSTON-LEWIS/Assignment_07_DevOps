import boto3
import time

ec2 = boto3.client('ec2')

# The instance you're restoring from
INSTANCE_ID = 'i-09d883059c33b3a84'

def lambda_handler(event, context):
    try:
        # Get instance details
        instance_info = ec2.describe_instances(InstanceIds=[INSTANCE_ID])
        instance = instance_info['Reservations'][0]['Instances'][0]

        volume_id = instance['BlockDeviceMappings'][0]['Ebs']['VolumeId']
        subnet_id = instance['SubnetId']
        key_name = instance.get('KeyName')
        security_group_ids = [sg['GroupId'] for sg in instance['SecurityGroups']]
        instance_type = instance['InstanceType']
        availability_zone = instance['Placement']['AvailabilityZone']
        image_id = instance['ImageId']  # Still needed for run_instances

        # Validate
        if not key_name:
            raise Exception("❌ Key pair is missing from the original instance.")
        if not security_group_ids:
            raise Exception("❌ Security groups are missing from the original instance.")

        print("✔️ Instance details collected.")
        print(f"Volume ID: {volume_id}")

        # Look for existing snapshot
        snapshots = ec2.describe_snapshots(
            Filters=[{'Name': 'volume-id', 'Values': [volume_id]}],
            OwnerIds=['self']
        )['Snapshots']

        if snapshots:
            latest_snapshot = max(snapshots, key=lambda s: s['StartTime'])
            snapshot_id = latest_snapshot['SnapshotId']
            volume_size = latest_snapshot['VolumeSize']
            print(f"📸 Using latest existing snapshot: {snapshot_id}")
        else:
            # Create new snapshot
            print("⚠️ No snapshot found. Creating a new snapshot...")
            snap_response = ec2.create_snapshot(
                VolumeId=volume_id,
                Description=f"Auto snapshot of {INSTANCE_ID}"
            )
            snapshot_id = snap_response['SnapshotId']

            # Tag it (optional)
            ec2.create_tags(Resources=[snapshot_id], Tags=[
                {'Key': 'Name', 'Value': f'AutoSnapshot-{INSTANCE_ID}'}
            ])

            # Wait for snapshot to complete
            print("⏳ Waiting for snapshot to complete...")
            waiter = ec2.get_waiter('snapshot_completed')
            waiter.wait(SnapshotIds=[snapshot_id])
            print(f"✅ Snapshot completed: {snapshot_id}")

            volume_size = snap_response['VolumeSize']

        # Launch new instance using snapshot
        print("🚀 Launching new EC2 instance...")
        response = ec2.run_instances(
            BlockDeviceMappings=[
                {
                    'DeviceName': '/dev/xvda',
                    'Ebs': {
                        'SnapshotId': snapshot_id,
                        'VolumeSize': volume_size,
                        'VolumeType': 'gp2',
                        'DeleteOnTermination': True
                    }
                }
            ],
            ImageId=image_id,
            MinCount=1,
            MaxCount=1,
            InstanceType=instance_type,
            KeyName=key_name,
            NetworkInterfaces=[
                {
                    'DeviceIndex': 0,
                    'SubnetId': subnet_id,
                    'Groups': security_group_ids,
                    'AssociatePublicIpAddress': True
                }
            ],
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [{'Key': 'Name', 'Value': 'Restored-From-Snapshot'}]
                }
            ]
        )

        new_instance_id = response['Instances'][0]['InstanceId']
        print(f"✅ New EC2 instance launched: {new_instance_id}")

        return {
            "status": "success",
            "new_instance_id": new_instance_id,
            "restored_from_snapshot": snapshot_id
        }

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return {
            "status": "failure",
            "reason": str(e)
        }
