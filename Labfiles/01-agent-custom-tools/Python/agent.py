import os
import json
from dotenv import load_dotenv

# 参照の追加


def main():
    # コンソールをクリア
    os.system('cls' if os.name=='nt' else 'clear')

    # .env ファイルから環境変数を読み込む
    load_dotenv()
    project_endpoint = os.getenv("PROJECT_ENDPOINT")
    model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME")

    # プロジェクト クライアントに接続


        # イベント関数ツールを定義


        # 観測コスト計算関数ツールを定義


        # 観測レポート生成関数ツールを定義


        # 関数ツールを使用して新しいエージェントを作成


        # チャット セッション用のスレッドを作成


        # エージェントに送り返す関数呼び出し出力のリストを作成


        while True:
            user_input = input("天文学エージェントへのプロンプトを入力してください。終了するには 'quit' を入力します。\nUSER: ").strip()
            if user_input.lower() == "quit":
                print("チャットを終了します。")
                break

            # エージェントにプロンプトを送信


            # エージェントの応答を取得（関数呼び出しが含まれる場合あり）


            # 関数呼び出しを処理


            # 関数呼び出しの出力をモデルに返して応答を取得


        # 完了後にエージェントを削除


if __name__ == '__main__':
    main()
