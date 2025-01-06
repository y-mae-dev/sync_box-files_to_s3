from datetime import datetime, timezone
from box_connector.initialize_box_client import initialize_box_client
from box_connector.dynamodb_operations import get_last_sync_time, update_last_sync_time
from box_connector.box_operations import process_box_items
from box_connector.app_config import BOX_FOLDER_ID

box_client = initialize_box_client()

def lambda_handler(event, context):
    last_sync_time = get_last_sync_time()
    process_box_items(box_client, BOX_FOLDER_ID, last_sync_time)
    update_last_sync_time(datetime.now(timezone.utc).isoformat())
    return {"statusCode": 200, "body": "Success"}