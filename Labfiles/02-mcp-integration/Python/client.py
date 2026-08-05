import os
import asyncio
import json
from dotenv import load_dotenv
from contextlib import AsyncExitStack
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import FunctionTool
from azure.identity import DefaultAzureCredential
from azure.ai.projects.models import PromptAgentDefinition, FunctionTool
from openai.types.responses.response_input_param import FunctionCallOutput, ResponseInputParam

# 参照の追加


# コンソールをクリア
os.system('cls' if os.name=='nt' else 'clear')

# .env ファイルから環境変数を読み込む
load_dotenv()
project_endpoint = os.getenv("PROJECT_ENDPOINT")
model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME")

async def connect_to_server(exit_stack: AsyncExitStack):
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"],
        env=None
    )

    # MCP サーバーを起動


    # MCP クライアント セッションを作成


    # 利用可能なツールを一覧表示


    return session

async def chat_loop(session):

    # エージェント クライアントに接続
    with (
        DefaultAzureCredential() as credential,
        AIProjectClient(endpoint=project_endpoint, credential=credential) as project_client,
        project_client.get_openai_client() as openai_client,
    ):

        # サーバーから利用可能な MCP ツールを取得
        response = await session.list_tools()
        tools = response.tools

        # 各ツールの関数を構築


        # エージェント用の FunctionTool 定義を作成


        # エージェントを作成


        # チャット セッション用のスレッドを作成
        conversation = openai_client.conversations.create()

        # モデルに送り返す関数呼び出し出力を保持する入力リストを作成
        input_list: ResponseInputParam = []

        while True:
            user_input = input("在庫エージェントへのプロンプトを入力してください。終了するには 'quit' を入力します。\nUSER: ").strip()
            if user_input.lower() == "quit":
                print("チャットを終了します。")
                break

            # エージェントにプロンプトを送信
            openai_client.conversations.items.create(
                conversation_id=conversation.id,
                items=[{"type": "message", "role": "user", "content": user_input}],
            )

            # エージェントの応答を取得（MCP サーバー ツールへの関数呼び出しが含まれる場合あり）
            response = openai_client.responses.create(
                conversation=conversation.id,
                extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}},
                input=input_list,
            )

            # 実行ステータスのエラーを確認
            if response.status == "failed":
                print(f"Response failed: {response.error}")

            # 関数呼び出しを処理


            # 関数呼び出しの出力をモデルに返して応答を取得


        # 完了後にエージェントを削除
        print("エージェントをクリーンアップしています:")
        project_client.agents.delete_version(agent_name=agent.name, agent_version=agent.version)
        print("在庫エージェントを削除しました。")


async def main():
    import sys
    exit_stack = AsyncExitStack()
    try:
        session = await connect_to_server(exit_stack)
        await chat_loop(session)
    finally:
        await exit_stack.aclose()

if __name__ == "__main__":
    asyncio.run(main())
