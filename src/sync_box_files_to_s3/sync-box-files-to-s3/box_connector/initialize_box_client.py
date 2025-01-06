# import os
# from box_sdk_gen import BoxClient, BoxCCGAuth, CCGConfig

# def initialize_box_client():
#     """
#     Boxクライアントを初期化する関数。
#     環境変数から認証情報を取得。

#     Returns:
#         BoxClient: 認証済みのBoxクライアント
#     """
#     ccg_config = CCGConfig(
#         client_id=os.getenv("BOX_CLIENT_ID"),
#         client_secret=os.getenv("BOX_CLIENT_SECRET"),
#         user_id=os.getenv("BOX_USER_ID"),
#     )
#     auth = BoxCCGAuth(config=ccg_config)
#     client = BoxClient(auth=auth)
#     return client

# import os
# from boxsdk import BoxClient, OAuth2

# def initialize_box_client():
#     """
#     Boxクライアントを初期化する関数。
#     環境変数から開発者トークンを取得。

#     Returns:
#         BoxClient: 認証済みのBoxクライアント
#     """
#     developer_token = os.getenv("BOX_DEVELOPER_TOKEN")
    
#     # OAuth2 インスタンスを作成し、開発者トークンを渡す
#     auth = OAuth2(client_id=None, client_secret=None, access_token=developer_token)
#     client = BoxClient(auth=auth)
    
#     return client

from box_sdk_gen import BoxClient, BoxDeveloperTokenAuth
import os
def initialize_box_client():
    """
    Boxクライアントを初期化する関数。
    環境変数から開発者トークンを取得。

    Returns:
        BoxClient: 認証済みのBoxクライアント
    """
    developer_token = os.getenv("BOX_DEVELOPER_TOKEN")
    
    auth = BoxDeveloperTokenAuth(token=developer_token)
    client = BoxClient(auth=auth)

    return client