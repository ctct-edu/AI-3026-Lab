# AI エージェント コース — ラボ一覧

このコースでは、Microsoft Foundry を使って AI エージェントを構築・拡張するスキルを習得します。

---

## コース全体の流れ

```
00 環境構築ガイド（共通リファレンス）

01 → 02a → 02b ─┬─ 03（独立ラボ）
                └─ 04 → 05
```

> **演習 01 で作成する Foundry プロジェクトと gpt-5-mini モデルは、演習 02a・02b・04・05 で共用します。**  
> **演習 03 のみ独立したラボです**。Foundry ポータル（`https://ai.azure.com`）で専用のプロジェクト・Azure AI Search・ストレージ アカウントを作成します。

---

## ラボ一覧

| ラボ | タイトル | 前提 | 特記事項 |
|------|----------|------|----------|
| **00** | [演習環境 構築ガイド（共通）](00-environment-setup.md) | なし | 環境の全体像を示すリファレンス。実手順は演習 01 を参照 |
| **01** | [AI エージェントでのカスタム関数の使用](01-agent-custom-tools.md) | なし | **Foundry プロジェクト/モデルはここで作成し、02a・02b・04・05 で共用（TPM は 5K で作成）** |
| **02a** | [リモート MCP サーバーによるエージェントの拡張](02a-mcp-remote-server.md) | 01 | 公開 MCP サーバー（Microsoft Learn Docs）に接続 |
| **02b** | [カスタム MCP サーバーの作成とエージェントへの接続](02b-mcp-custom-server.md) | 02a | FastMCP でローカル MCP サーバーを自作し、stdio クライアントで接続 |
| **03** | [AI エージェントと Foundry IQ の統合](03-integrate-agent-with-foundry-iq.md) | なし | 独立ラボ。ポータルで専用プロジェクト＋Azure AI Search＋ストレージ アカウントを作成。Azure AI Search のプロビジョニングが必要 |
| **04** | [Microsoft Agent Framework SDK を使用した Azure AI エージェントの開発](04-agent-framework.md) | 01 | コードファーストのエージェント |
| **05** | [Microsoft Agent Framework を使用したマルチエージェント ソリューションの開発](05-agent-framework-multi-agents.md) | 01・04 | 順次処理パイプライン（3 エージェント構成）。**既定 TPM（1000）では動作しないため、演習 01 で TPM を 5K に設定済みであることを確認**。演習 01・02a・02b・04・05 共用リソースの最終クリーンアップもここで実施 |

---

## 共通の事前準備

すべてのラボを開始する前に、以下が整っていることを確認してください（いずれも演習環境に準備済みです）。

- Visual Studio Code（最新版）
- Foundry Toolkit 拡張機能（VS Code 用）— インストール済み
- Python `3.13` 以降（推奨: `3.13.12`）
- アクティブな Azure サブスクリプション
- 各演習のスターター コード（`Labfiles/` 配下）— 配置済み。クローンは不要
