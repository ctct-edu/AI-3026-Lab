import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

# 環境変数を読み込む
load_dotenv()
project_endpoint = os.getenv("PROJECT_ENDPOINT")
agent_name = os.getenv("AGENT_NAME")

# 設定を検証
if not project_endpoint or not agent_name:
    raise ValueError("PROJECT_ENDPOINT と AGENT_NAME を .env ファイルに設定してください")

print(f"プロジェクトに接続中: {project_endpoint}")
print(f"使用するエージェント: {agent_name}\n")

# TODO: プロジェクトに接続して会話を作成
# 以下のコードを追加してください:
# 1. DefaultAzureCredential を作成
# 2. エンドポイントを指定して AIProjectClient を作成
# 3. OpenAI クライアントを取得
# 4. 名前でエージェントを取得
# 5. 新しい会話を作成


# 会話履歴（クライアント側での追跡）
conversation_history = []


def send_message_to_agent(user_message):
    """
    エージェントにメッセージを送信し、conversations API を使用して応答を処理します。
    """
    try:
        print("\nAgent: ", end="", flush=True)

        # TODO: 会話にユーザー メッセージを追加して応答を取得
        # 以下のコードを追加してください:
        # 1. conversations.items.create() を使用して会話にユーザー メッセージを追加
        # 2. エージェント参照を指定して responses.create() で応答を作成
        # 3. 応答テキストを抽出して表示
        # 4. 引用情報があれば確認して表示
        # ここにコードを記述してください




        # 応答テキストを抽出
        if response and response.output_text:
            response_text = response.output_text

            print(f"{response_text}\n")

            # 引用情報がある場合は確認して表示
            if hasattr(response, 'citations') and response.citations:
                print("\n出典:")
                for citation in response.citations:
                    print(f"  - {citation.content if hasattr(citation, 'content') else 'ナレッジ ベース'}")

            # 会話履歴に保存（クライアント側）
            conversation_history.append({
                "role": "assistant",
                "content": response_text
            })

            return response_text
        else:
            print("応答がありませんでした。\n")
            return None
    except Exception as e:
        print(f"\n\nエラー: {str(e)}\n")
        return None


def display_conversation_history():
    """
    会話履歴の全内容を表示します。
    """
    print("\n" + "="*60)
    print("会話履歴")
    print("="*60 + "\n")

    for turn in conversation_history:
        role = turn["role"].upper()
        content = turn["content"]
        print(f"{role}: {content}\n")

    print("="*60 + "\n")


def main():
    """
    メインの対話ループ。
    """
    print("Contoso 製品エキスパート エージェント")
    print("アウトドアやキャンプ用品について質問してください。")
    print("'history' を入力すると会話履歴を表示します。'quit' を入力すると終了します。\n")

    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() == 'quit':
                print("\n会話を終了します...")
                break

            if user_input.lower() == 'history':
                display_conversation_history()
                continue

            # メッセージを送信して応答を取得
            send_message_to_agent(user_input)

        except KeyboardInterrupt:
            print("\n\nユーザーによって中断されました。")
            break
        except Exception as e:
            print(f"\n予期しないエラー: {str(e)}\n")

    print("\n会話が終了しました。")


if __name__ == "__main__":
    main()
