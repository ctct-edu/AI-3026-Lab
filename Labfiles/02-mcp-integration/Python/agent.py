import os
from dotenv import load_dotenv

# 参照の追加


# .env ファイルから環境変数を読み込む
load_dotenv()
project_endpoint = os.getenv("PROJECT_ENDPOINT")
model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME")

# エージェント クライアントに接続


    # エージェント MCP ツールを初期化


    # MCP ツールを使用して新しいエージェントを作成


    # 会話スレッドを作成


    # MCP ツールをトリガーする初回リクエストを送信


    # MCP 承認リクエストが無くなるまでラウンドを繰り返す


    # エージェント バージョンを削除してリソースをクリーンアップ
