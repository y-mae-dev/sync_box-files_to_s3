import boto3
import time

# DynamoDBクライアントの初期化
dynamodb = boto3.client('dynamodb', region_name='us-west-2') 

# 設定
TABLE_NAME = "ItemTable"
GSI_NAME = "key-index"

def create_dynamodb_table():
    """
    DynamoDBテーブルを作成する関数
    """
    try:
        # テーブル作成リクエスト
        print(f"Creating DynamoDB table: {TABLE_NAME}...")
        response = dynamodb.create_table(
            TableName=TABLE_NAME,
            AttributeDefinitions=[
                {"AttributeName": "item_id", "AttributeType": "S"},  # Partition Key
                {"AttributeName": "source_type", "AttributeType": "S"},  # GSI Partition Key
                {"AttributeName": "s3_key", "AttributeType": "S"},  # GSI Sort Key
            ],
            KeySchema=[
                {"AttributeName": "item_id", "KeyType": "HASH"},  # Primary Key: Partition Key
            ],
            GlobalSecondaryIndexes=[
                {
                    "IndexName": GSI_NAME,
                    "KeySchema": [
                        {"AttributeName": "source_type", "KeyType": "HASH"},  # GSI Partition Key
                        {"AttributeName": "s3_key", "KeyType": "RANGE"},  # GSI Sort Key
                    ],
                    "Projection": {"ProjectionType": "ALL"},  # 投影タイプ
                }
            ],
            BillingMode="PAY_PER_REQUEST"  # 従量課金制
        )
        print(f"Table creation initiated: {response['TableDescription']['TableName']}")

        # テーブルがACTIVEになるまで待機
        while True:
            status = dynamodb.describe_table(TableName=TABLE_NAME)['Table']['TableStatus']
            print(f"Waiting for table to become ACTIVE. Current status: {status}")
            if status == "ACTIVE":
                break
            time.sleep(5)
        print(f"DynamoDB table {TABLE_NAME} is ready!")
    except dynamodb.exceptions.ResourceInUseException:
        print(f"DynamoDB table {TABLE_NAME} already exists.")

if __name__ == "__main__":
    create_dynamodb_table()
