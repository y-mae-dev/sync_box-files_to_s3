import os

BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
S3_KEY_PREFIX = "box-files/"
ITEM_TABLE = os.getenv("ITEM_TABLE")
BOX_FOLDER_ID = os.getenv("BOX_FOLDER_ID")
