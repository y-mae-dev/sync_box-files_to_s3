from datetime import datetime, timezone
import re
import io
from box_connector.app_config import BUCKET_NAME, S3_KEY_PREFIX
import boto3

s3_client = boto3.client("s3", region_name="us-west-2")

def process_box_items(box_client, folder_id, last_sync_time):
    offset = 0
    limit = 100
    while True:
        items = box_client.folders.get_folder_items(folder_id, limit=limit, offset=offset).entries
        if not items:
            break
        for item in items:
            if item.type == "file":
                process_file(box_client, item, last_sync_time)
            elif item.type == "folder":
                process_box_items(box_client, item.id, last_sync_time)
        offset += limit

def process_file(box_client, file, last_sync_time):
    modified_at_str = file.modified_at if file.modified_at else datetime.now(timezone.utc).isoformat()
    # 正規表現で "+hh:m" の形式を "+hh:mm" に修正
    modified_at_str = re.sub(r"(\+00):(\d{1})$", r"\1:0\2", modified_at_str)

    modified_at = datetime.fromisoformat(modified_at_str).replace(tzinfo=timezone.utc)

    if last_sync_time and modified_at <= datetime.fromisoformat(last_sync_time):
        print(f"Skipping unchanged file: {file.name}")
        return

    upload_to_s3(box_client, file)

def upload_to_s3(box_client, file):
    """
    BoxファイルをS3にアップロード
    """
    file_id = file.id

    # ファイルをダウンロードしてメモリに読み込む
    file_stream = box_client.downloads.download_file(file_id)
    file_content = io.BytesIO(file_stream.read())  # メモリ上に全て読み込む

    s3_key = construct_s3_key(file)
    s3_client.put_object(
        Bucket=BUCKET_NAME,
        Key=s3_key,
        Body=file_content,
        ContentType="application/octet-stream",
    )
    print(f"Uploaded file: {file.name} to S3 as {s3_key}")



def construct_s3_key(file):
    """
    S3キーを構築する
    """
    folder_ids = []
    
    # path_collection が None でないかをチェック
    if file.path_collection and file.path_collection.entries:
        folder_ids = [e.id for e in file.path_collection.entries if e.type == "folder"]

    s3_key = S3_KEY_PREFIX + "/".join(folder_ids) + "/" + file.id
    return s3_key
