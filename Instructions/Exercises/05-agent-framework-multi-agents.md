---
lab:
    title: 'Microsoft Agent Framework を使用したマルチエージェント ソリューションの開発'
    description: 'Microsoft Agent Framework SDK を使用して複数のエージェントを連携させる方法を学ぶ。'
    level: 300
    duration: 30
    islab: true
    status: 'released'
---

# Microsoft Agent Framework を使用したマルチエージェント ソリューションの開発

この演習では、Microsoft Agent Framework SDK のシーケンシャル オーケストレーション パターンを練習します。顧客フィードバックを処理して次のステップを提案するために連携する 3 つのエージェントのシンプルなパイプラインを作成します。以下のエージェントを作成します。

- サマライザー エージェントは、生のフィードバックを短く中立的な文に要約します。
- クラシファイアー エージェントは、フィードバックを「肯定的」「否定的」「機能リクエスト」に分類します。
- 最後に、推奨アクション エージェントが適切なフォローアップ手順を推奨します。

Microsoft Agent Framework SDK を使用して問題を分解し、適切なエージェントにルーティングして、実用的な結果を生成する方法を学びます。

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

### モデルのレート制限（TPM）の確認

> **重要**: このマルチエージェント演習では、サマライザー・クラシファイアー・推奨アクションの 3 つのエージェントが順番に応答を生成するため、既定の **1 分あたりのトークン数（TPM）1000** のままでは結果が出力されません。演習 01 でのモデル デプロイ時に TPM を **5K（5000）** に設定済みのはずなので、ここで念のため確認してください。まだ 1000 のままの場合は、演習を始める前に以下の手順で 5K に引き上げてください。

1. Foundry Toolkit の **[モデル]** セクションで `gpt-5-mini` デプロイを右クリックし、デプロイの編集（**[Edit deployment]**）を選択して、**[Tokens per Minute]** が **5K（5000）** になっていることを確認します。
1. まだ 1000 のままの場合は、**[Tokens per Minute]** のスライダーまたは入力欄で **5K（5000）** を指定します。
1. 変更した場合は保存し、デプロイの状態が **Success** に戻るまで待ちます。

> **注意**: サブスクリプションのリージョン クォータに空きがない場合は 5K に上げられないことがあります。その場合は Foundry ポータル（`https://ai.azure.com`）のクォータ画面で空き状況を確認してください。

## スターター コードを開く

この演習では、Foundry プロジェクトに接続して顧客フィードバックを処理するマルチエージェント ソリューションを作成するためのスターター コードを使用します。

1. VS Code で **[ファイル] > [フォルダーを開く]** を選択し、配置済みの `Labfiles/05-agent-orchestration` フォルダーを開きます。

1. エクスプローラー ペインで **Python** フォルダーを展開して、この演習のコード ファイルを表示します。

1. **requirements.txt** ファイルを右クリックし、**[統合ターミナルで開く]** を選択します。

1. ターミナルで次のコマンドを入力して、演習用にあらかじめ構築済みの仮想環境 (`labenv`) を有効化します。

    ```
    .\labenv\Scripts\Activate.ps1
    ```

    > **注意**: 必要な Python パッケージは `labenv` に事前インストール済みです。`pip install` を再実行する必要はありません。

1. `.env` ファイルを開き、`your_project_endpoint` プレースホルダーをプロジェクトのエンドポイント（Foundry Toolkit 拡張機能のプロジェクト デプロイ リソースからコピーしたもの）に置き換え、MODEL_DEPLOYMENT_NAME 変数がモデルのデプロイ名に設定されていることを確認します。変更後に **Ctrl+S** キーを押してファイルを保存します。

## AI エージェントの作成

マルチエージェント ソリューション用のエージェントを作成する準備ができました。

1. コード エディターで **agents.py** ファイルを開きます。

1. ファイルの先頭でコメント **参照の追加** の下に、エージェントを実装するために必要なライブラリの名前空間を参照する以下のコードを追加します。

    ```python
    # 参照の追加
    import asyncio
    from agent_framework import Message
    from agent_framework_foundry import FoundryChatClient
    from agent_framework.orchestrations import SequentialBuilder
    from azure.identity import AzureCliCredential
    ```

1. **main** 関数でエージェントの手順を確認します。これらの手順はオーケストレーション内の各エージェントの動作を定義します。

1. コメント **チャット クライアントを作成** の下に以下のコードを追加します。

    ```python
    # チャット クライアントを作成
    credential = AzureCliCredential()
    chat_client = FoundryChatClient(
        credential=credential,
        project_endpoint=project_endpoint,
        model=model_deployment,
    )
    ```

    **AzureCliCredential** オブジェクトはコードが Azure アカウントに認証できるようにします。**FoundryChatClient** オブジェクトは .env 設定（`AZURE_AI_PROJECT_ENDPOINT` / `AZURE_AI_MODEL_DEPLOYMENT_NAME`）から読み込んだ Foundry プロジェクト設定を含めます。**FoundryChatClient** は非同期コンテキスト マネージャーをサポートしていないため、`async with` は使用せず、通常のオブジェクトとしてインスタンス化します。

1. コメント **エージェントを作成** の下に以下のコードを追加します。

    （インデント レベルを維持してください）

    ```python
    # エージェントを作成
    summarizer = chat_client.as_agent(
        instructions=summarizer_instructions,
        name="summarizer",
    )

    classifier = chat_client.as_agent(
        instructions=classifier_instructions,
        name="classifier",
    )

    action = chat_client.as_agent(
        instructions=action_instructions,
        name="action",
    )
    ```

## シーケンシャル オーケストレーションの作成

1. **main** 関数でコメント **現在のフィードバックを初期化** を見つけて以下のコードを追加します。

    （インデント レベルを維持してください）

    ```python
    # 現在のフィードバックを初期化
    feedback="""
    I use the dashboard every day to monitor metrics, and it works well overall. 
    But when I'm working late at night, the bright screen is really harsh on my eyes. 
    If you added a dark mode option, it would make the experience much more comfortable.
    """
    ```

1. コメント **シーケンシャル オーケストレーションを構築** の下に、定義したエージェントでシーケンシャル オーケストレーションを定義する以下のコードを追加します。

    ```python
    # シーケンシャル オーケストレーションを構築
    workflow = SequentialBuilder(participants=[summarizer, classifier, action], output_from="all").build()
    ```

    エージェントはオーケストレーションに追加された順序でフィードバックを処理します。`output_from="all"` を指定しない場合、既定では最後の参加者（この例では `action`）の出力しか `"output"` イベントとして受け取れないため、全エージェントの出力を収集するにはこの指定が必要です。

1. コメント **実行して出力を収集** の下に以下のコードを追加します。

    ```python
    # 実行して出力を収集
    result = await workflow.run(f"Customer feedback: {feedback}")
    outputs: list[Message] = []
    for response in result.get_outputs():
        outputs.extend(response.messages)
    ```

    `workflow.run(...)` は既定（非ストリーミング）では `Awaitable[WorkflowRunResult]` を返すため、`await` で結果を取得します。`WorkflowRunResult.get_outputs()` は `"output"` イベントのデータ（各エージェントの `AgentResponse`）のみを抽出して返すので、その `.messages` を集約すれば全エージェントの発言内容が得られます。

1. コメント **出力を表示** の下に以下のコードを追加します。

    ```python
    # 出力を表示
    if outputs:
        for i, msg in enumerate(outputs, start=1):
            name = msg.author_name or ("assistant" if msg.role == "assistant" else "user")
            print(f"{'-' * 60}\n{i:02d} [{name}]\n{msg.text}")
    ```

    このコードはオーケストレーションから収集したワークフロー出力のメッセージをフォーマットして表示します。

1. **Ctrl+S** コマンドを使用してコード ファイルへの変更を保存します。

## アプリケーションのテスト

コードを実行して AI エージェントの連携を確認します。

1. 統合ターミナルで次のコマンドを入力してアプリケーションを実行します。

    ```
    az login
    ```

    ```
    python agents.py
    ```

1. 次のような出力が表示されます。

    ```output
    ------------------------------------------------------------
    01 [user]
    顧客フィードバック:
        ダッシュボードは毎日使っており、全体的にはよく機能しています。
        ただ、夜間に作業するとき、画面の明るさが目に強く感じます。
        ダーク モード オプションがあれば、使い心地がずっと良くなると思います。

    ------------------------------------------------------------
    02 [summarizer]
    ユーザーが夜間の使い勝手向上のためにダーク モードを要望しています。
    ------------------------------------------------------------
    03 [classifier]
    機能リクエスト
    ------------------------------------------------------------
    04 [action]
    製品バックログの機能拡張リクエストとして記録する。
    ```

    > **ヒント**: レート制限を超えてアプリが失敗した場合は、数秒待ってから再試行してください。TPM が 5K になっていない場合、3 つのエージェントが順に実行されるこの演習では応答が空になることがあります。上記の「モデルのレート制限（TPM）の確認」の手順を確認してください。

1. 必要に応じて、別のフィードバック入力を使用してコードを実行することもできます。

    ```output
    昨日、アカウントにアクセスできなかったためカスタマー サポートに連絡しました。担当者はほぼ即座に応答し、礼儀正しくプロフェッショナルで、数分以内に問題を解決してくれました。正直、これまでで最高のサポート体験の一つでした。
    ```

1. 完了したら、ターミナルで `deactivate` を入力して Python 仮想環境を終了します。

## クリーンアップ

Azure AI Agent Service の探索が完了したら、この演習で作成したリソースを削除して不要な Azure コストが発生しないようにします。

演習 01・02・04・05 では **同じ Foundry プロジェクトとモデルを共用**してきました。以下のクリーンアップは、共用プロジェクトを使用する全演習が終わった後に **1 回だけ**実施してください。

### モデルの削除

1. VS Code で **[Azure リソース]** ビューを更新します。

1. **[モデル]** サブセクションを展開します。

1. デプロイされたモデルを右クリックし、**[削除]** を選択します。

### リソース グループの削除

1. [Azure ポータル](https://portal.azure.com) を開きます。

1. Microsoft Foundry リソースが含まれているリソース グループに移動します。

1. **[リソース グループの削除]** を選択して削除を確認します。
