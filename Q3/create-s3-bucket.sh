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