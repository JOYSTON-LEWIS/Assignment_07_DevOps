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
