import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')

    # Stop instances with tag Action=Auto-Stop
    stop_response = ec2.describe_instances(
        Filters=[{'Name': 'tag:Action', 'Values': ['Auto-Stop']}]
    )
    stop_ids = [instance['InstanceId']
                for reservation in stop_response['Reservations']
                for instance in reservation['Instances']
                if instance['State']['Name'] != 'stopped']
    
    if stop_ids:
        ec2.stop_instances(InstanceIds=stop_ids)
        print(f"Stopped instances: {stop_ids}")
    else:
        print("No instances to stop.")

    # Start instances with tag Action=Auto-Start
    start_response = ec2.describe_instances(
        Filters=[{'Name': 'tag:Action', 'Values': ['Auto-Start']}]
    )
    start_ids = [instance['InstanceId']
                 for reservation in start_response['Reservations']
                 for instance in reservation['Instances']
                 if instance['State']['Name'] != 'running']
    
    if start_ids:
        ec2.start_instances(InstanceIds=start_ids)
        print(f"Started instances: {start_ids}")
    else:
        print("No instances to start.")
