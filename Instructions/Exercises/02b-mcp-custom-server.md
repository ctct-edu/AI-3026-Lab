---
lab:
    title: 'カスタム MCP サーバーの作成とエージェントへの接続'
    description: '独自の Model Context Protocol (MCP) サーバー ツールを作成し、エージェントに接続する。'
    level: 300
    duration: 40
    islab: true
    status: 'released'
---

# カスタム MCP サーバーの作成とエージェントへの接続

この演習では、独自のカスタム Model Context Protocol (MCP) サーバー ツールを作成し、そのツールを検出・呼び出す MCP クライアントを実装して、AI エージェントに接続します。エージェントはカスタム サービスと対話できるようになります。

この演習の所要時間は約 **40** 分です。

> **注意**: この演習で使用する一部のテクノロジーはプレビュー中または開発中のため、予期しない動作、警告、またはエラーが発生する場合があります。

## 前提条件

この演習を開始する前に、以下を準備してください。

- ローカル コンピューターへの [Visual Studio Code](https://code.visualstudio.com/) のインストール
- アクティブな [Azure サブスクリプション](https://azure.microsoft.com/free/)
- [Python 3.13](https://www.python.org/downloads/) 以降のインストール
- [演習 02a](02a-mcp-remote-server.md) の完了

演習 02a と**同じ** `Labfiles/02-mcp-integration/Python` フォルダー、同じ `.env`、同じ仮想環境 (`labenv`) をそのまま使用します。新しいフォルダーは作成されません（フォルダー名は `02-mcp-integration` のままです）。

> \* Python 3.13 は利用可能ですが、一部の依存関係はまだそのリリース向けにコンパイルされていません。このラボは `Python 3.13.12` で正常にテスト済みです。

## スターター コードを確認する

1. 演習 02a から続けて作業している場合、VS Code のフォルダーと統合ターミナルはそのまま使用できます。`labenv` が有効になっていること（ターミナルのプロンプトに `(labenv)` と表示されていること）を確認してください。

1. VS Code や ターミナルを閉じた後に演習を再開する場合は、`Labfiles/02-mcp-integration` フォルダーを開き直し、**requirements.txt** を右クリックして統合ターミナルを開き、次のコマンドで仮想環境を再度有効化します。

    ```
    .\labenv\Scripts\Activate.ps1
    ```

    `.env` ファイルのプロジェクト エンドポイントとモデル デプロイ名は演習 02a で設定済みのため、変更の必要はありません。

## カスタム ツールを持つ MCP サーバーの作成

リモート MCP サーバーに接続するだけでなく、独自のカスタム MCP サーバー ツールを作成してエージェントに接続することもできます。Model Context Protocol (MCP) サーバーは、呼び出し可能なツールをホストするコンポーネントです。これらのツールは AI エージェントに公開できる Python 関数です。ツールに `@mcp.tool()` アノテーションが付与されると、クライアントから検出可能になり、AI エージェントが会話やタスク中に自律的に呼び出せるようになります。このタスクでは、エージェントが在庫照会と推奨事項を実行できるツールを追加します。

1. コード エディターで **server.py** ファイルを開きます。

    このコード ファイルでは、エージェントが小売店のバックエンド サービスをシミュレートするために使用できるツールを定義します。ファイルの先頭にあるサーバー セットアップ コードに注目してください。`FastMCP` を使用して "Inventory" という名前の MCP サーバー インスタンスを素早く起動します。このサーバーは定義したツールをホストし、ラボ中にエージェントからアクセスできるようにします。

1. コメント **参照の追加** の下に以下のコードを追加します。

    ```python
    # 参照の追加
    from fastmcp import FastMCP
    ```

1. コメント **MCP サーバーを作成** の下に以下のコードを追加して、新しい MCP サーバー インスタンスを作成します。

    ```python
    # MCP サーバーを作成
    mcp = FastMCP(name="Inventory")
    ```

    このコードは "Inventory" というラベルの新しい MCP サーバーを初期化します。

1. コメント **在庫確認 MCP ツールを追加** を見つけて、その下（関数定義の上）に次の1行を追加します。コメント行はスターターコードに既に含まれているため、あらためて入力する必要はありません。

    ```python
    # 在庫確認 MCP ツールを追加
    @mcp.tool()  # ← この行を追加
    def get_inventory_levels() -> dict:
       # continued...
    ```

    この辞書はサンプルの在庫を表します。`@mcp.tool()` デコレーターは関数を MCP サーバーのツールとして登録し、LLM が関数を検出できるようにします。

1. コメント **週間販売数 MCP ツールを追加** を見つけて、その下（関数定義の上）に次の1行を追加します。コメント行はスターターコードに既に含まれているため、あらためて入力する必要はありません。

    ```python
    # 週間販売数 MCP ツールを追加
    @mcp.tool()  # ← この行を追加
    def get_weekly_sales() -> dict:
       # continued...
    ```

1. コメント **MCP サーバーを起動** を見つけて、サーバーを起動する以下のコードを追加します。

    ```python
    # MCP サーバーを起動
    mcp.run(show_banner=False)
    ```

    このコードは MCP サーバーを起動し、ツールをエージェントが検出・使用できる状態にします。`show_banner=False` を設定すると、起動バナーが stdout に出力されなくなり、MCP stdio プロトコルが破損するのを防ぎます。

1. ファイルを保存します（**Ctrl+S**）。

## カスタム MCP サーバーに接続する MCP クライアントの実装

MCP クライアントは MCP サーバーに接続してツールを検出し、呼び出すコンポーネントです。エージェントとサーバー ホストの関数との橋渡し役として、ユーザーのプロンプトに応じた動的なツール使用を可能にします。

1. **client.py** ファイルに移動します。

1. コメント **参照の追加** を見つけて、クラスをインポートする以下のコードを追加します。

    ```python
    # 参照の追加
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    ```

1. **connect_to_server** メソッド内でコメント **MCP サーバーを起動** を見つけて、以下のコードを追加します。

    ```python
    # MCP サーバーを起動
    stdio_transport = await exit_stack.enter_async_context(stdio_client(server_params))
    stdio, write = stdio_transport
    ```

    標準的な本番環境のセットアップでは、サーバーはクライアントとは別に実行されます。ただし、このラボでは標準入出力トランスポートを使用してクライアントがサーバーを起動します。これにより 2 つのコンポーネント間に軽量な通信チャネルが作成され、ローカル開発のセットアップが簡略化されます。

1. コメント **MCP クライアント セッションを作成** を見つけて以下のコードを追加します。

    ```python
    # MCP クライアント セッションを作成
    session = await exit_stack.enter_async_context(ClientSession(stdio, write))
    await session.initialize()
    ```

    これにより前の手順の入出力ストリームを使用して新しいクライアント セッションが作成されます。`session.initialize` を呼び出すと、MCP サーバーに登録されているツールを検出して呼び出す準備が整います。

1. コメント **利用可能なツールを一覧表示** の下に、クライアントがサーバーに接続されていることを確認する以下のコードを追加します。

    ```python
    # 利用可能なツールを一覧表示
    response = await session.list_tools()
    tools = response.tools
    print("\nConnected to server with tools:", [tool.name for tool in tools]) 
    ```

    これで Azure AI エージェントで使用するためのクライアント セッションの準備ができました。

## MCP ツールのエージェントへの接続

このタスクでは、MCP サーバー ツールをエージェントに接続して、ユーザーのプロンプトに応じて呼び出せるようにします。

> **ヒント**: コードを追加するときは、正しいインデントを維持してください。コメントのインデント レベルを参考にしてください。

1. **chat_loop** メソッドでコメント **各ツールの関数を構築** を見つけて以下のコードを追加します。

    ```python
    # 各ツールの関数を構築
    def make_tool_func(tool_name):
        async def tool_func(**kwargs):
            result = await session.call_tool(tool_name, kwargs)
            return result
        
        tool_func.__name__ = tool_name
        return tool_func

    # 関数呼び出し処理時にアクセスしやすいよう関数を辞書に格納
    functions_dict = {tool.name: make_tool_func(tool.name) for tool in tools}
    ```

    このコードは MCP サーバーで利用可能なツールを動的にラップして、AI エージェントから呼び出せるようにします。各ツールはエージェントが呼び出せる非同期関数に変換されます。

1. コメント **エージェント用の FunctionTool 定義を作成** を見つけて以下のコードを追加します。

    ```python
    # エージェント用の FunctionTool 定義を作成
    mcp_function_tools: FunctionTool = []
    for tool in tools:
        function_tool = FunctionTool(
            name=tool.name,
            description=tool.description,
            parameters={
                "type": "object",
                "properties": {},
                "additionalProperties": False,
            },
            strict=True
        )
        mcp_function_tools.append(function_tool)
    ```

1. コメント **エージェントを作成** を見つけて以下のコードを追加します。

    ```python
    # エージェントを作成
    agent = project_client.agents.create_version(
        agent_name="inventory-agent",
        definition=PromptAgentDefinition(
            model=model_deployment,
            instructions="""
            あなたは在庫アシスタントです。以下の一般的なガイドラインに従ってください:
            - 在庫が 10 未満かつ週間販売数が 15 以上の場合は補充を推奨
            - 在庫が 20 超かつ週間販売数が 5 未満の場合はクリアランスを推奨
            """,
            tools=mcp_function_tools
        ),
    )
    ```

    これらの手順とツールにより、エージェントはツールを呼び出して在庫と販売データを取得し、その情報をもとにユーザーへの有用な応答を提供できるようになります。

1. コメント **関数呼び出しを処理** を見つけて以下のコードを追加します。

    ```python
    # 関数呼び出しを処理
    for item in response.output:
        if item.type == "function_call":
            # 対応する関数ツールを取得
            function_name = item.name
            kwargs = json.loads(item.arguments)
            required_function = functions_dict.get(function_name)

            # 関数を呼び出す
            output = await required_function(**kwargs)

            # 出力テキストを追加
            input_list.append(
               FunctionCallOutput(
                  type="function_call_output",
                  call_id=item.call_id,
                  output=output.content[0].text,
               )
            )
    ```

    このコードはエージェントの応答内の関数呼び出しを受け取り、対応するツール関数を呼び出し、エージェントに送り返す出力を準備します。

1. コメント **関数呼び出しの出力をモデルに返して応答を取得** を見つけて以下のコードを追加します。

    ```python
    # 関数呼び出しの出力をモデルに返して応答を取得
    if input_list:
        response = openai_client.responses.create(
            input=input_list,
            previous_response_id=response.id,
            extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}},
        )
    print(f"Agent response: {response.output_text}")
    ```

1. 完了したらコード ファイルを保存します（**Ctrl+S**）。

## カスタム MCP ツールとエージェントのテスト

1. 統合ターミナルで次のコマンドを入力してアプリケーションを実行します。

    ```
    python client.py
    ```

1. プロンプトが表示されたら、次のようなプロンプトを入力します。

    ```
    全製品の現在の在庫レベルを表示してください。
    ```

    > **ヒント**: レート制限を超えてアプリが失敗した場合は、数秒待ってから再試行してください。サブスクリプションで使用可能なクォータが不足している場合、モデルが応答できないことがあります。

    次のような出力が表示されます。

    ```
    MessageRole.AGENT:
    Agent response: 全製品の現在の在庫レベルは以下のとおりです:

    - Moisturizer: 6
    - Shampoo: 8
    - Body Spray: 28
    [続く...]

    補充またはクリアランスの推奨が必要ですか？週間販売数を確認してアドバイスします。
    ```

    エージェントが MCP ツールを呼び出して在庫と販売データを取得し、その情報をもとにユーザーへの有用な応答を提供できたことに注目してください。

1. 必要に応じて会話を続けることができます。スレッドは*ステートフル*であるため、会話履歴が保持されます。つまり、エージェントは各応答に対して完全なコンテキストを持ちます。

    次のようなプロンプトを試してみましょう。

    ```
    補充が必要な製品はありますか？
    ```

    ```
    処分（クリアランス）を推奨する製品はどれですか？
    ```

    ```
    今週の売れ筋商品を教えてください。
    ```

1. `quit` と入力してアプリケーションを終了します。

    ターミナルで `deactivate` を使用して Python 仮想環境を終了することもできます。

## まとめ: 演習 02a との違い

| 観点 | 02a リモート MCP | 02b カスタム MCP |
|---|---|---|
| サーバーの提供者 | 他者（Microsoft） | 自分（`server.py`） |
| ツールの登録 | 不可（利用のみ） | `@mcp.tool()` デコレーター |
| 通信方式 | Streamable HTTP（リモート） | stdio（ローカル子プロセス） |
| クライアント | Foundry サービスが内蔵 | 自分で実装（`stdio_client` + `ClientSession`） |
| ツール一覧の取得 | サービス側が自動で実施 | `session.list_tools()` を自分で呼ぶ |
| ツールの実行 | サービス側が自動で実施 | `session.call_tool()` を `FunctionTool` 経由で自分が実行 |
| コード量 | `agent.py` のみ | `server.py` + `client.py` |

演習 02a では Foundry が肩代わりしていた「ツールの発見・呼び出し」を、演習 02b では自分で書きました。同じ MCP でも、リモート接続はサービス統合で済む一方、ローカル stdio では自前のクライアント実装が必要になります。演習 01 で使った `FunctionTool` がここで再登場するのは、MCP ツールをエージェントに見せる橋渡し役として必要だからです。

## クリーンアップ

この演習で使用した Foundry プロジェクトとモデルは、**後続の演習（04・05）でも使用します。まだ削除しないでください**。

すべての演習が完了したら、[演習 05](05-agent-framework-multi-agents.md) の「クリーンアップ」に従ってリソースを削除してください。
