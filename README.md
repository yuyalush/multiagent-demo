# マルチエージェントデモ (Multi-Agent Demo)

Azure OpenAI ServiceとAI Agent Frameworkを利用した、マルチエージェントシステムのデモンストレーション。

## 概要

このプロジェクトは、1つのオーケストレーターと2つのサブエージェントが協調して動作し、ユーザーの質問に対して適切な回答を提供するマルチエージェントシステムの最小限の実装です。

## システム仕様

### アーキテクチャ

```
┌─────────────────────────────────────────┐
│         Orchestrator Agent              │
│      (オーケストレーター)                 │
│  - 質問の分類                            │
│  - エージェントの選択                     │
│  - 応答の統合                            │
└──────────┬──────────────────────────────┘
           │
           ├───────────────┬───────────────┐
           │               │               │
           ▼               ▼               ▼
    ┌───────────┐  ┌───────────┐  ┌───────────┐
    │ Technical │  │ Business  │  │  General  │
    │   Agent   │  │   Agent   │  │  Response │
    └───────────┘  └───────────┘  └───────────┘
         │               │               │
         └───────────────┴───────────────┘
                     │
                     ▼
              統合された回答
```

### エージェント構成

#### 1. Orchestrator Agent（オーケストレーター）
- **役割**: システム全体の調整役
- **機能**:
  - ユーザーの質問を分析し、適切なエージェントを選択
  - 複数のサブエージェントからの回答を統合
  - 最終的な包括的回答を生成

#### 2. Technical Agent（技術仕様エージェント）
- **専門分野**: プログラミング、アーキテクチャ、技術仕様
- **役割**: 技術的な質問に特化した回答を提供

#### 3. Business Agent（ビジネス分析エージェント）
- **専門分野**: ビジネス戦略、市場分析、収益モデル
- **役割**: ビジネス関連の質問に特化した回答を提供

## セットアップ手順

### 前提条件

- Python 3.8以上
- Azure OpenAI Serviceのアクセス権限
- Azure OpenAI Serviceのデプロイ済みモデル（GPT-4推奨）

### 1. リポジトリのクローン

```bash
git clone https://github.com/yuyalush/multiagent-demo.git
cd multiagent-demo
```

### 2. 仮想環境の作成と有効化

```bash
# 仮想環境の作成
python -m venv venv

# 仮想環境の有効化
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

### 4. 環境変数の設定

`.env.example`を`.env`にコピーし、Azure OpenAI Serviceの設定を記入します：

```bash
cp .env.example .env
```

`.env`ファイルを編集して、以下の情報を設定：

```env
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

**設定項目の取得方法**:
- `AZURE_OPENAI_ENDPOINT`: Azure PortalのAzure OpenAIリソースから取得
- `AZURE_OPENAI_API_KEY`: Azure PortalのAzure OpenAIリソースの「キーとエンドポイント」から取得
- `AZURE_OPENAI_DEPLOYMENT_NAME`: デプロイしたモデルの名前
- `AZURE_OPENAI_API_VERSION`: 使用するAPIバージョン

## 使用方法

### デモモードの実行

```bash
python main.py
```

プログラムを実行すると、以下のように動作します：

1. **デモモード**: 3つのサンプル質問が自動的に処理されます
   - 技術的な質問の例
   - ビジネス関連の質問の例
   - 両方の観点が必要な質問の例

2. **インタラクティブモード**: デモ終了後、自由に質問を入力できます
   - 質問を入力してEnterキーを押すと、システムが回答を生成します
   - `exit`または`quit`と入力すると終了します

### 実行例

```
================================================================================
マルチエージェントデモシステム
Multi-Agent Demo System with Azure OpenAI
================================================================================

[システム] Azure OpenAIクライアントを初期化中...
[システム] デプロイメント名: gpt-4
[システム] オーケストレーターを初期化中...
[システム] 初期化完了！

================================================================================
デモモード: 3つのサンプル質問を処理します
================================================================================

################################################################################
質問 1/3
################################################################################

質問: Pythonでマルチエージェントシステムを実装する方法を教えてください。

[OrchestratorAgent] 質問を分析中...
[OrchestratorAgent] 質問タイプ: technical
[OrchestratorAgent] 判断理由: この質問は技術的な実装に関するものです

[OrchestratorAgent] TechnicalAgentに質問を転送...
[OrchestratorAgent] 応答を統合中...

================================================================================

【最終回答】

================================================================================
[Technical Agentからの回答が表示されます]
================================================================================
```

## プロジェクト構造

```
multiagent-demo/
├── README.md                  # このファイル
├── requirements.txt           # Pythonパッケージの依存関係
├── .env.example              # 環境変数のテンプレート
├── .gitignore                # Git除外設定
├── main.py                   # メインエントリーポイント
├── orchestrator_agent.py     # オーケストレーターエージェント
├── technical_agent.py        # 技術仕様エージェント
└── business_agent.py         # ビジネス分析エージェント
```

## 動作の仕組み

1. **質問の受付**: ユーザーから質問を受け取ります

2. **質問の分類**: Orchestrator Agentが質問を分析し、以下のカテゴリに分類します
   - `technical`: 技術的な質問
   - `business`: ビジネス関連の質問
   - `both`: 両方の観点が必要な質問
   - `general`: 一般的な質問

3. **エージェントの選択**: 分類に基づいて適切なサブエージェントを選択
   - Technical Agent: 技術的な質問を処理
   - Business Agent: ビジネス関連の質問を処理
   - 両方: 複数のエージェントが並行して処理

4. **応答の生成**: 各エージェントがAzure OpenAI Serviceを使用して回答を生成

5. **応答の統合**: Orchestrator Agentが複数の回答を統合し、包括的な最終回答を生成

6. **結果の表示**: ユーザーに統合された回答と処理の詳細を表示

## カスタマイズ

### 新しいエージェントの追加

1. 新しいエージェントクラスを作成（例: `marketing_agent.py`）
2. `orchestrator_agent.py`にインポートと初期化を追加
3. `classify_query`メソッドを更新して新しいカテゴリを追加
4. `process`メソッドに新しいエージェントへのルーティングロジックを追加

### システムプロンプトのカスタマイズ

各エージェントの`get_system_prompt()`メソッドを編集して、エージェントの振る舞いをカスタマイズできます。

## トラブルシューティング

### エラー: 環境変数が設定されていません

- `.env`ファイルが正しく作成されているか確認
- `.env`ファイルの内容が正しいか確認
- 環境変数名にタイプミスがないか確認

### エラー: APIキーが無効です

- Azure PortalでAPIキーを再確認
- APIキーに余分なスペースや改行がないか確認

### エラー: デプロイメントが見つかりません

- Azure Portalでモデルのデプロイメント名を確認
- `AZURE_OPENAI_DEPLOYMENT_NAME`が正しいか確認

## ライセンス

このプロジェクトはデモンストレーション目的で作成されています。

## 作成者

yuyalush

## 参考資料

- [Azure OpenAI Service Documentation](https://learn.microsoft.com/azure/cognitive-services/openai/)
- [OpenAI Python SDK](https://github.com/openai/openai-python)
