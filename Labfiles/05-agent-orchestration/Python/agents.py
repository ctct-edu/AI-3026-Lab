import asyncio
import os
from dotenv import load_dotenv

# 参照の追加


async def main():
    load_dotenv()
    project_endpoint = os.getenv("PROJECT_ENDPOINT")
    model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME")

    # エージェントの手順
    summarizer_instructions="""
    顧客のフィードバックを 1 文で要約してください。中立的かつ簡潔に保ってください。
    出力例:
    写真のアップロード中にアプリがクラッシュする。
    ユーザーがダーク モード機能を称賛している。
    """

    classifier_instructions="""
    フィードバックを次のいずれかに分類してください: Positive（肯定的）、Negative（否定的）、または Feature request（機能リクエスト）。
    """

    action_instructions="""
    要約と分類に基づいて、次のアクションを 1 文で提案してください。
    出力例:
    モバイル チームの高優先度バグとしてエスカレーション。
    デザインおよびマーケティング チームと共有するためのポジティブ フィードバックとして記録。
    製品バックログの機能拡張リクエストとして記録。
    """

    # チャット クライアントを作成


        # エージェントを作成


        # 現在のフィードバックを初期化


        # シーケンシャル オーケストレーションを構築


        # 実行して出力を収集


        # 出力を表示



if __name__ == "__main__":
    asyncio.run(main())
