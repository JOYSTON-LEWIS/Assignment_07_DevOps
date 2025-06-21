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
