import boto3

# AWSリソースの初期化
s3 = boto3.client('s3', region_name='us-west-2')

# 設定
S3_BUCKET_NAME = "box-synced-files-bucket"


def create_s3_bucket():
    """
    S3バケットを作成する関数
    """
    try:
        # バケット作成
        print(f"Creating S3 bucket: {S3_BUCKET_NAME}...")
        response = s3.create_bucket(
            Bucket=S3_BUCKET_NAME,
            CreateBucketConfiguration={'LocationConstraint': 'us-west-2'}
        )
        print(f"S3 bucket creation successful: {S3_BUCKET_NAME}")
    except s3.exceptions.BucketAlreadyExists:
        print(f"S3 bucket {S3_BUCKET_NAME} already exists.")
    except s3.exceptions.BucketAlreadyOwnedByYou:
        print(f"S3 bucket {S3_BUCKET_NAME} is already owned by you.")

if __name__ == "__main__":
    create_s3_bucket()