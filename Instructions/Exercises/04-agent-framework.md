---
lab:
    title: 'Microsoft Agent Framework SDK を使用した Azure AI エージェントの開発'
    description: 'Microsoft Agent Framework SDK を使用して Azure AI チャット エージェントを作成・使用する方法を学ぶ。'
    level: 300
    duration: 30
    islab: true
    status: 'released'
---

# Microsoft Agent Framework SDK を使用した Azure AI チャット エージェントの開発

この演習では、Azure AI Agent Service と Microsoft Agent Framework を使用して、経費請求を処理する AI エージェントを作成します。

この演習の所要時間は約 **30** 分です。

> **注意**: この演習で使用する一部のテクノロジーはプレビュー中または開発中のため、予期しない動作、警告、またはエラーが発生する場合があります。

## 前提条件

この演習を開始する前に、以下を準備してください。

- ローカル コンピューターへの [Visual Studio Code](https://code.visualstudio.com/) のインストール
- アクティブな [Azure サブスクリプション](https://azure.microsoft.com/free/)
- [Python 3.13](https://www.python.org/downloads/) 以降のインストール
- [演習 01](01-agent-custom-tools.md) の完了（Foundry プロジェクトと gpt-5-mini モデルをこの演習でも使用します）

> \* Python 3.13 は利用可能ですが、一部の依存関係はまだそのリリース向けにコンパイルされていません。このラボは `Python 3.13.12` で正常にテスト済みです。

## Foundry プロジェクトとモデルの確認

この演習では、**演習 01 で作成した Foundry プロジェクトと gpt-5-mini モデルをそのまま使用します**。新しく作成する必要はありません。

1. Visual Studio Code のサイドバーで **Foundry Toolkit** アイコンを選択します。
1. **[MY RESOURCES]** の下に、演習 01 で作成したプロジェクトが表示されていることを確認します。プロジェクトの配下には **Models**・**Agents**・**Tools**・**Knowledge**・**Evaluations** のツリーが表示されます。

    ![Foundry Toolkit サイドバーのプロジェクト ツリー。MY RESOURCES 配下にプロジェクトと Models / Agents / Tools / Knowledge / Evaluations が表示されている。](../Media/vs-code-endpoint.png)

1. **Models** を展開し、`gpt-5-mini` のデプロイが **Success** になっていることを確認します。
1. プロジェクト デプロイの名前を右クリックし、**[プロジェクト エンドポイントのコピー]** を選択します。この URL を次の手順で `.env` に設定します。

> **注意**: 演習 01 を実施していない場合は、先に [演習 01](01-agent-custom-tools.md) の「Foundry プロジェクトの作成」「モデルのデプロイ」を完了してください。

## スターター コードを開く

この演習では、Foundry プロジェクトに接続して経費データを処理できるエージェントを作成するためのスターター コードを使用します。
1. VS Code で **[ファイル] > [フォルダーを開く]** を選択し、配置済みの `Labfiles/04-agent-framework` フォルダーを開きます。

1. エクスプローラー ペインで **Python** フォルダーを展開して、この演習のコード ファイルを表示します。

1. **requirements.txt** ファイルを右クリックし、**[統合ターミナルで開く]** を選択します。

1. ターミナルで次のコマンドを入力して、演習用にあらかじめ構築済みの仮想環境 (`labenv`) を有効化します。

    ```
    .\labenv\Scripts\Activate.ps1
    ```

    > **注意**: 必要な Python パッケージは `labenv` に事前インストール済みです。`pip install` を再実行する必要はありません。

1. `.env` ファイルを開き、`your_project_endpoint` プレースホルダーをプロジェクトのエンドポイント（Foundry Toolkit 拡張機能のプロジェクト デプロイ リソースからコピーしたもの）に置き換え、MODEL_DEPLOYMENT_NAME 変数がモデルのデプロイ名に設定されていることを確認します。変更後に **Ctrl+S** キーを押してファイルを保存します。

カスタム ツールを使用して経費データを処理する AI エージェントを作成する準備ができました。

## カスタム ツールを持つエージェントの作成

> **ヒント**: コードを追加するときは、正しいインデントを維持してください。既存のコメントをガイドとして使用し、同じインデント レベルで新しいコードを入力してください。

1. コード エディターで **agent-framework.py** ファイルを開きます。

1. ファイルのコードを確認します。以下が含まれています。
    - 一般的に使用される名前空間への参照を追加する **import** 文
    - 経費データを含むファイルを読み込み、ユーザーに指示を求め、その後呼び出す *main* 関数
    - コードを作成してエージェントを使用するための **process_expenses_data** 関数

1. ファイルの先頭で既存の **import** 文の後にコメント **参照の追加** を見つけて、エージェントを実装するために必要なライブラリの名前空間を参照する以下のコードを追加します。

    ```python
    # 参照の追加
    from agent_framework import tool, Agent
    from agent_framework_foundry import FoundryChatClient
    from azure.identity import AzureCliCredential
    from pydantic import Field
    from typing import Annotated
    ```

1. ファイルの下の方でコメント **メール機能のツール関数を作成** を見つけて、エージェントがメールを送信するために使用する関数を定義する以下のコードを追加します（ツールはエージェントにカスタム機能を追加する方法です）。

    ```python
    # メール機能のツール関数を作成
    @tool(approval_mode="never_require")
    def submit_claim(
        to: Annotated[str, Field(description="Who to send the email to")],
        subject: Annotated[str, Field(description="The subject of the email.")],
        body: Annotated[str, Field(description="The text body of the email.")]):
            print("\nTo:", to)
            print("Subject:", subject)
            print(body, "\n")
    ```

    > **注意**: この関数はメールをコンソールに出力することで送信を*シミュレート*します。実際のアプリケーションでは、SMTP サービスなどを使用してメールを実際に送信します。

1. **send_email** コードの上に戻り、**process_expenses_data** 関数内でコメント **クライアントを作成し、ツールと手順でエージェントを初期化** を見つけて、以下のコードを追加します。

    （インデント レベルを維持してください）

    ```python
    # クライアントを作成し、ツールと手順でエージェントを初期化
    credential = AzureCliCredential()
    async with (
         Agent(
             client=FoundryChatClient(
                 credential=credential,
                 model=model_deployment,
                 project_endpoint=project_endpoint,
             ),
             instructions="""あなたは経費請求提出のための AI アシスタントです。
                         ユーザーのリクエストに応じて経費請求書を作成し、プラグイン関数を使用して件名「Expense Claim」、本文に明細と合計を含むメールを expenses@contoso.com に送信してください。
                         送信後はユーザーに完了を確認してください。ユーザーに追加情報を求めず、提供されたデータだけを使用してメールを作成してください。""",
             tools=[submit_claim],
         ) as agent,
     ):
    ```

    **AzureCliCredential** オブジェクトはコードが Azure アカウントに認証できるようにします。**FoundryChatClient** オブジェクトには .env 設定からの Foundry プロジェクト設定が含まれます。**Agent** オブジェクトはクライアント、エージェントへの手順、メール送信のために定義したツール関数で初期化されます。

1. コメント **エージェントを使用して経費データを処理** を見つけて、エージェントが実行するスレッドを作成してチャット メッセージで呼び出す以下のコードを追加します。

    （インデント レベルを維持してください）:

    ```python
    # エージェントを使用して経費データを処理
    try:
        # 送信するメッセージのリストに入力プロンプトを追加
        prompt_messages = [f"{prompt}: {expenses_data}"]
        # メッセージを使用してエージェントを呼び出す
        response = await agent.run(prompt_messages)
        # 応答を表示
        print(f"\n# Agent:\n{response}")
    except Exception as e:
        # エラーが発生しました
        print (e)
    ```

1. エージェントの完成したコードを確認します。コメントを参考に各コード ブロックの役割を理解し、コードの変更を保存します（**Ctrl+S**）。

## アプリケーションのテスト

1. 統合ターミナルで次のコマンドを入力してアプリケーションを実行します。

    ```
    az login
    ```

    ```
    python agent-framework.py
    ```

1. 経費データをどう処理するかを尋ねられたら、以下のプロンプトを入力します。

    ```
    経費請求を提出してください
    ```

1. アプリケーションが完了したら出力を確認します。エージェントは提供されたデータに基づいて経費請求のメールを作成しているはずです。

    > **ヒント**: レート制限を超えてアプリが失敗した場合は、数秒待ってから再試行してください。サブスクリプションで使用可能なクォータが不足している場合、モデルが応答できないことがあります。

1. 完了したら、ターミナルで `deactivate` を入力して Python 仮想環境を終了します。

## クリーンアップ

この演習で使用した Foundry プロジェクトとモデルは、**後続の演習（05）でも使用します。まだ削除しないでください**。

すべての演習が完了したら、[演習 05](05-agent-framework-multi-agents.md) の「クリーンアップ」に従ってリソースを削除してください。
