import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv

# 参照の追加



async def main():
    # .env ファイルの設定を読み込む
    load_dotenv()
    
    # コンソールをクリア
    os.system('cls' if os.name=='nt' else 'clear')

    # 経費データ ファイルを読み込む
    script_dir = Path(__file__).parent
    file_path = script_dir / 'data.txt'
    with file_path.open('r') as file:
        data = file.read() + "\n"

    # プロンプトを入力してもらう
    user_prompt = input(f"ファイル内の経費データは次のとおりです:\n\n{data}\n\nどのように処理しますか?\n\n")

    # 非同期エージェント コードを実行
    await process_expenses_data(user_prompt, data)

async def process_expenses_data(prompt, expenses_data):
    project_endpoint = os.getenv("PROJECT_ENDPOINT")
    model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME")

    # クライアントを作成し、ツールと手順でエージェントを初期化


        # エージェントを使用して経費データを処理



# メール機能のツール関数を作成



if __name__ == "__main__":
    asyncio.run(main())
