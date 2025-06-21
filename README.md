# ⚙️ Graded Assignment on Serverless Architecture using AWS Lambda & Boto3

This repository contains solutions for multiple serverless automation tasks using **AWS Lambda** and **Boto3**. Each task which is solved wtih Lambda Functions Feature of AWS includes a `lambda_function.py` script with automation logic for managing AWS services like EC2 and S3, simulating real-world DevOps and cloud management scenarios.

---

## 📂 Structure Overview

```text
📂 Q01/ -> Task 01: Auto EC2 Management
└── lambda_function.py

📂 Q02/ -> Task 02: S3 Bucket Cleanup
└── lambda_function.py

📂 Q03/ -> Task 03: Unencrypted S3 Monitor
├── lambda_function.py
└── create-s3-bucket.sh

📂 Q05/ -> Task 05: Auto-Tag EC2 on Launch
└── lambda_function.py

📂 Q17/ -> Task 17: Restore EC2 from Snapshot
├── lambda_function.py
└── JL-EC2-Restore-Policy.json
```

---

## 🧪 Task 01: Automated Instance Management Using Tags

- 📁 Directory: `Q01`
- 📜 Script: `lambda_function.py`

### ✅ Lambda Capabilities:
This Lambda function automatically manages EC2 instance states based on tag values:
- Starts instances tagged with `Action = Auto-Start`
- Stops instances tagged with `Action = Auto-Stop`
- Logs all affected instance IDs

```text
lambda_function.py
```
```python
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

```

### 🔐 IAM Permissions:
Attach the `AmazonEC2FullAccess` policy to the Lambda execution role.

### 📸 Screenshots:

![Q1_01](https://github.com/JOYSTON-LEWIS/My-Media-Repository/blob/main/Assignment_07_DevOps_Outputs_Images/Q1_01.png)
![Q1_02](https://github.com/JOYSTON-LEWIS/My-Media-Repository/blob/main/Assignment_07_DevOps_Outputs_Images/Q1_02.png)
![Q1_03](https://github.com/JOYSTON-LEWIS/My-Media-Repository/blob/main/Assignment_07_DevOps_Outputs_Images/Q1_03.png)
![Q1_04](https://github.com/JOYSTON-LEWIS/My-Media-Repository/blob/main/Assignment_07_DevOps_Outputs_Images/Q1_04.png)
![Q1_05](https://github.com/JOYSTON-LEWIS/My-Media-Repository/blob/main/Assignment_07_DevOps_Outputs_Images/Q1_05.png)
![Q1_06](https://github.com/JOYSTON-LEWIS/My-Media-Repository/blob/main/Assignment_07_DevOps_Outputs_Images/Q1_06.png)
![Q1_07](https://github.com/JOYSTON-LEWIS/My-Media-Repository/blob/main/Assignment_07_DevOps_Outputs_Images/Q1_07.png)
![Q1_08](https://github.com/JOYSTON-LEWIS/My-Media-Repository/blob/main/Assignment_07_DevOps_Outputs_Images/Q1_08.png)
![Q1_09](https://github.com/JOYSTON-LEWIS/My-Media-Repository/blob/main/Assignment_07_DevOps_Outputs_Images/Q1_09.png)
![Q1_10](https://github.com/JOYSTON-LEWIS/My-Media-Repository/blob/main/Assignment_07_DevOps_Outputs_Images/Q1_10.png)
![Q1_11](https://github.com/JOYSTON-LEWIS/My-Media-Repository/blob/main/Assignment_07_DevOps_Outputs_Images/Q1_11.png)
![Q1_12](https://github.com/JOYSTON-LEWIS/My-Media-Repository/blob/main/Assignment_07_DevOps_Outputs_Images/Q1_12.png)
![Q1_13](https://github.com/JOYSTON-LEWIS/My-Media-Repository/blob/main/Assignment_07_DevOps_Outputs_Images/Q1_13.png)

---

## 🧪 Task 02: Automated S3 Bucket Cleanup

- 📁 Directory: `Q02`
- 📜 Script: `lambda_function.py`

### ✅ Lambda Capabilities:
This Lambda function cleans up an S3 bucket by:
- Listing all files in the bucket
- Deleting files older than 30 days
- Logging names of deleted files for visibility

```text
lambda_function.py
```
```python
import boto3
from datetime import datetime, timezone, timedelta

# Configuration
BUCKET_NAME = 'joyston-lewis-b10-bucket'  # <-- Replace with your bucket name
DAYS_THRESHOLD = 30

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    now = datetime.now(timezone.utc)
    threshold_date = now - timedelta(days=DAYS_THRESHOLD)

    deleted_files = []

    response = s3.list_objects_v2(Bucket=BUCKET_NAME)

    if 'Contents' in response:
        for obj in response['Contents']:
            if obj['LastModified'] < threshold_date:
                print(f"Deleting: {obj['Key']} (Last Modified: {obj['LastModified']})")
                s3.delete_object(Bucket=BUCKET_NAME, Key=obj['Key'])
                deleted_files.append(obj['Key'])

    if not deleted_files:
        print("No files older than 30 days found.")
    else:
        print(f"Deleted {len(deleted_files)} files: {deleted_files}")

    return {
        'statusCode': 200,
        'body': f'Deleted files: {deleted_files}'
    }

```

### 🔐 IAM Permissions:
Attach the `AmazonS3FullAccess` policy to the Lambda execution role.

### 📸 Screenshots:

![Q2_01](https://github.com/JOYSTON-LEWIS/My-Media-Repository/blob/main/Assignment_07_DevOps_Outputs_Images/Q2_01.png)
![Q2_02](https://github.com/JOYSTON-LEWIS/My-Media-Repository/blob/main/Assignment_07_DevOps_Outputs_Images/Q2_02.png)
![Q2_03](https://github.com/JOYSTON-LEWIS/My-Media-Repository/blob/main/Assignment_07_DevOps_Outputs_Images/Q2_03.png)
![Q2_04](https://github.com/JOYSTON-LEWIS/My-Media-Repository/blob/main/Assignment_07_DevOps_Outputs_Images/Q2_04.png)
![Q2_05](https://github.com/JOYSTON-LEWIS/My-Media-Repository/blob/main/Assignment_07_DevOps_Outputs_Images/Q2_05.png)
![Q2_06](https://github.com/JOYSTON-LEWIS/My-Media-Repository/blob/main/Assignment_07_DevOps_Outputs_Images/Q2_06.png)
![Q2_07](https://github.com/JOYSTON-LEWIS/My-Media-Repository/blob/main/Assignment_07_DevOps_Outputs_Images/Q2_07.png)
![Q2_08](https://github.com/JOYSTON-LEWIS/My-Media-Repository/blob/main/Assignment_07_DevOps_Outputs_Images/Q2_08.png)
![Q2_09](https://github.com/JOYSTON-LEWIS/My-Media-Repository/blob/main/Assignment_07_DevOps_Outputs_Images/Q2_09.png)

---

## 🧪 Task 03: Monitor Unencrypted S3 Buckets

- 📁 Directory: `Q03`
- 📜 Script: `lambda_function.py`

### ✅ Lambda Capabilities:
This function strengthens security by:
- Listing all S3 buckets
- Identifying buckets **without server-side encryption (SSE)**
- Logging the names of unencrypted buckets

```text
lambda_function.py
```
```python
import boto3
import logging
from botocore.exceptions import ClientError

# Setup logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    s3 = boto3.client('s3')

    try:
        response = s3.list_buckets()
        buckets = response.get('Buckets', [])
        unencrypted_buckets = []

        for bucket in buckets:
            bucket_name = bucket['Name']
            try:
                enc = s3.get_bucket_encryption(Bucket=bucket_name)
                rules = enc['ServerSideEncryptionConfiguration']['Rules']
                logger.info(f"✅ Bucket '{bucket_name}' is encrypted with: {rules}")
            except ClientError as e:
                error_code = e.response['Error']['Code']
                if error_code == 'ServerSideEncryptionConfigurationNotFoundError':
                    logger.warning(f⚠️ Bucket '{bucket_name}' has NO default encryption.")
                    unencrypted_buckets.append(bucket_name)
                else:
                    logger.error(f"❌ Error checking encryption for bucket {bucket_name}: {e}")

        if unencrypted_buckets:
            logger.info("🚨 Unencrypted Buckets Found:")
            for ub in unencrypted_buckets:
                logger.info(f"- {ub}")
        else:
            logger.info("✅ All buckets are encrypted.")

        return {
            'statusCode': 200,
            'unencrypted_buckets': unencrypted_buckets
        }

    except Exception as e:
        logger.error(f"Unhandled exception: {e}")
        return {
            'statusCode': 500,
            'error': str(e)
        }

```

### 🔐 IAM Permissions:
Attach the `AmazonS3ReadOnlyAccess` policy to the Lambda execution role.

### 💡 Important Note
- The AWS Account used for testing this did not allow me to create Unencrypted S3 Buckets hence that part of the code remains to be tested.  

### 🛠️ Additional Script:

Use this helper shell script to quickly create a test S3 bucket (assuming AWS CLI is configured):

```bash
nano create-s3-bucket.sh
```

```bash
#!/bin/bash

# Usage check
if [ -z "$1" ]; then
  echo "❌ Usage: $0 <bucket-name>"
  echo "Example: $0 my-test-bucket"
  exit 1
fi

BUCKET_NAME=$1
REGION="ap-south-1"

echo "🔧 Creating S3 bucket: $BUCKET_NAME in region: $REGION..."

# Create bucket
aws s3api create-bucket \
  --bucket "$BUCKET_NAME" \
  --region "$REGION" \
  --create-bucket-configuration LocationConstraint="$REGION"

# Check success
if [ $? -ne 0 ]; then
  echo "❌ Bucket creation failed. It may already exist or you may not have permissions."
  exit 1
fi

# Pause briefly for consistency
sleep 3

echo "🔍 Checking encryption status..."

# Check encryption (capture stderr)
ENCRYPTION_OUTPUT=$(aws s3api get-bucket-encryption --bucket "$BUCKET_NAME" 2>&1)

# Determine encryption state
if echo "$ENCRYPTION_OUTPUT" | grep -q "ServerSideEncryptionConfigurationNotFoundError"; then
  echo "🚨 Bucket '$BUCKET_NAME' is NOT encrypted (no default encryption)."
else
  echo "✅ Bucket '$BUCKET_NAME' is encrypted."
fi
```

```bash
chmod +x create-s3-bucket.sh
./create-s3-bucket.sh your-bucket-name
```

### 📸 Screenshots:

![Q3_01](https://github.com/JOYSTON-LEWIS/My-Media-Repository/blob/main/Assignment_07_DevOps_Outputs_Images/Q3_01.png)
![Q3_02](https://github.com/JOYSTON-LEWIS/My-Media-Repository/blob/main/Assignment_07_DevOps_Outputs_Images/Q3_02.png)
![Q3_03](https://github.com/JOYSTON-LEWIS/My-Media-Repository/blob/main/Assignment_07_DevOps_Outputs_Images/Q3_03.png)
![Q3_04](https://github.com/JOYSTON-LEWIS/My-Media-Repository/blob/main/Assignment_07_DevOps_Outputs_Images/Q3_04.png)
![Q3_05](https://github.com/JOYSTON-LEWIS/My-Media-Repository/blob/main/Assignment_07_DevOps_Outputs_Images/Q3_05.png)
![Q3_06](https://github.com/JOYSTON-LEWIS/My-Media-Repository/blob/main/Assignment_07_DevOps_Outputs_Images/Q3_06.png)

---

## 🧪 Task 05: Auto-Tagging EC2 Instances on Launch

- 📁 Directory: `Q05`
- 📜 Script: `lambda_function.py`

### ✅ Lambda Capabilities:
This Lambda function automatically tags newly launched EC2 instances with metadata to improve visibility and resource tracking.

- Triggers automatically using **CloudWatch Events (EventBridge)** upon EC2 instance launch.
- Extracts the instance ID from the launch event.
- Applies two tags:
  - Current system date (as a launch timestamp)
  - Custom tag (e.g., `"Environment": "Dev"`)
- Helps with governance, auditing, cost tracking, and automation enforcement.

```text
lambda_function.py
```
```python
import boto3
from datetime import datetime

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')

    try:
        instances = event['detail']['responseElements']['instancesSet']['items']
        instance_ids = [instance['instanceId'] for instance in instances]
    except KeyError:
        print("No instance-id(s) found in event.")
        return

    # Generate tags
    current_date = datetime.utcnow().strftime('%Y-%m-%d')
    custom_tag_value = 'AutoTagged'

    # Tag instances
    try:
        ec2.create_tags(
            Resources=instance_ids,
            Tags=[
                {'Key': 'LaunchDate', 'Value': current_date},
                {'Key': 'Environment', 'Value': custom_tag_value}
            ]
        )
        print(f"Successfully tagged instances: {instance_ids}")
    except Exception as e:
        print(f"Failed to tag instances: {str(e)}")

```

### 🔐 Required IAM Permissions:
Attach the `AmazonEC2FullAccess` policy to the Lambda execution role.

### 🧪 Testing:
- Launch a new EC2 instance.
- Wait for the Lambda function to trigger.
- Verify tags under the EC2 **Tags** tab.

### 📸 Screenshots:

![Q5_01](https://github.com/JOYSTON-LEWIS/My-Media-Repository/blob/main/Assignment_07_DevOps_Outputs_Images/Q5_01.png)
![Q5_02](https://github.com/JOYSTON-LEWIS/My-Media-Repository/blob/main/Assignment_07_DevOps_Outputs_Images/Q5_02.png)
![Q5_03](https://github.com/JOYSTON-LEWIS/My-Media-Repository/blob/main/Assignment_07_DevOps_Outputs_Images/Q5_03.png)
![Q5_04](https://github.com/JOYSTON-LEWIS/My-Media-Repository/blob/main/Assignment_07_DevOps_Outputs_Images/Q5_04.png)
![Q5_05](https://github.com/JOYSTON-LEWIS/My-Media-Repository/blob/main/Assignment_07_DevOps_Outputs_Images/Q5_05.png)
![Q5_06](https://github.com/JOYSTON-LEWIS/My-Media-Repository/blob/main/Assignment_07_DevOps_Outputs_Images/Q5_06.png)
![Q5_07](https://github.com/JOYSTON-LEWIS/My-Media-Repository/blob/main/Assignment_07_DevOps_Outputs_Images/Q5_07.png)
![Q5_08](https://github.com/JOYSTON-LEWIS/My-Media-Repository/blob/main/Assignment_07_DevOps_Outputs_Images/Q5_08.png)
![Q5_09](https://github.com/JOYSTON-LEWIS/My-Media-Repository/blob/main/Assignment_07_DevOps_Outputs_Images/Q5_09.png)
![Q5_10](https://github.com/JOYSTON-LEWIS/My-Media-Repository/blob/main/Assignment_07_DevOps_Outputs_Images/Q5_10.png)
![Q5_11](https://github.com/JOYSTON-LEWIS/My-Media-Repository/blob/main/Assignment_07_DevOps_Outputs_Images/Q5_11.png)
![Q5_12](https://github.com/JOYSTON-LEWIS/My-Media-Repository/blob/main/Assignment_07_DevOps_Outputs_Images/Q5_12.png)
![Q5_13](https://github.com/JOYSTON-LEWIS/My-Media-Repository/blob/main/Assignment_07_DevOps_Outputs_Images/Q5_13.png)
![Q5_14](https://github.com/JOYSTON-LEWIS/My-Media-Repository/blob/main/Assignment_07_DevOps_Outputs_Images/Q5_14.png)

---

## 🧪 Task 17: Restore EC2 Instance from Snapshot

- 📁 Directory: `Q17`
- 📜 Script: `lambda_function.py`
- 📄 IAM Policy File: `JL-EC2-Restore-Policy.json`

### ✅ Lambda Capabilities:
This Lambda function automates EC2 recovery operations by launching a new instance from the latest snapshot.

- Lists available snapshots filtered by a defined tag or criteria.
- Selects the most recent snapshot.
- Creates a new volume and launches an EC2 instance using that volume.
- Logs the instance ID of the newly created instance.

This is useful for disaster recovery, scheduled restore testing, or cloning environments from backups.

```text
lambda_function.py
```
```python
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

```

### 🔐 Required IAM Permissions:
Use the custom policy file `JL-EC2-Restore-Policy.json` to grant only the necessary permissions to the Lambda function.

#### 📄 `JL-EC2-Restore-Policy.json`

```json
{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Sid": "AllowEC2SnapshotRestoreOperations",
			"Effect": "Allow",
			"Action": [
				"ec2:DescribeInstances",
				"ec2:DescribeSnapshots",
				"ec2:CreateSnapshot",
				"ec2:CreateTags",
				"ec2:RunInstances",
				"ec2:CreateVolume",
				"ec2:AttachVolume",
				"ec2:DescribeVolumes",
				"ec2:DeleteVolume",
				"ec2:GetConsoleOutput",
				"ec2:DescribeSecurityGroups",
				"ec2:DescribeSubnets"
			],
			"Resource": "*"
		}
	]
}
```

### 📸 Screenshots:

![Q17_01](https://github.com/JOYSTON-LEWIS/My-Media-Repository/blob/main/Assignment_07_DevOps_Outputs_Images/Q17_01.png)
![Q17_02](https://github.com/JOYSTON-LEWIS/My-Media-Repository/blob/main/Assignment_07_DevOps_Outputs_Images/Q17_02.png)
![Q17_03](https://github.com/JOYSTON-LEWIS/My-Media-Repository/blob/main/Assignment_07_DevOps_Outputs_Images/Q17_03.png)
![Q17_04](https://github.com/JOYSTON-LEWIS/My-Media-Repository/blob/main/Assignment_07_DevOps_Outputs_Images/Q17_04.png)
![Q17_05](https://github.com/JOYSTON-LEWIS/My-Media-Repository/blob/main/Assignment_07_DevOps_Outputs_Images/Q17_05.png)
![Q17_06](https://github.com/JOYSTON-LEWIS/My-Media-Repository/blob/main/Assignment_07_DevOps_Outputs_Images/Q17_06.png)
![Q17_07](https://github.com/JOYSTON-LEWIS/My-Media-Repository/blob/main/Assignment_07_DevOps_Outputs_Images/Q17_07.png)
![Q17_08](https://github.com/JOYSTON-LEWIS/My-Media-Repository/blob/main/Assignment_07_DevOps_Outputs_Images/Q17_08.png)
![Q17_09](https://github.com/JOYSTON-LEWIS/My-Media-Repository/blob/main/Assignment_07_DevOps_Outputs_Images/Q17_09.png)
![Q17_10](https://github.com/JOYSTON-LEWIS/My-Media-Repository/blob/main/Assignment_07_DevOps_Outputs_Images/Q17_10.png)

---

## :rocket: Next Version Release
- These are 5 questions resolved out of 19 in the assignment document provided to me
- Further questions with solutions will be updated as and when they are are completed by me so stay tuned 😊
  
## 📜 License
This project is licensed under the MIT License.

## 🤝 Contributing
Feel free to fork and improve the scripts! ⭐ If you find this project useful, please consider starring the repo—it really helps and supports my work! 😊

## 📧 Contact
For any queries, reach out via GitHub Issues.

---

🎯 **Thank you for reviewing this project! 🚀**
