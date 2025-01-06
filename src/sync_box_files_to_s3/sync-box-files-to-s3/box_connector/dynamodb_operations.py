import boto3
from box_connector.app_config import ITEM_TABLE

dynamodb = boto3.resource("dynamodb", region_name="us-west-2")
table = dynamodb.Table(ITEM_TABLE)

def get_last_sync_time():
    try:
        response = table.get_item(Key={"item_id": "last_sync_time"})
        return response.get("Item", {}).get("modified_at", None)
    except Exception as e:
        print(f"Error retrieving last sync time: {e}")
        return None

def update_last_sync_time(sync_time):
    table.put_item(
        Item={
            "item_id": "last_sync_time",
            "modified_at": sync_time,
        }
    )
