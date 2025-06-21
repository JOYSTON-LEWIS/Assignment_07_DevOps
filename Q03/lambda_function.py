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
