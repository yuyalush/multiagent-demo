"""
Multi-Agent Demo - Main Entry Point
マルチエージェントデモのメインプログラム
"""
import os
from dotenv import load_dotenv
from openai import AzureOpenAI
from orchestrator_agent import OrchestratorAgent


def initialize_client():
    """Azure OpenAI クライアントを初期化"""
    load_dotenv()
    
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
    
    if not endpoint or not api_key:
        raise ValueError(
            "環境変数が設定されていません。.envファイルを作成し、"
            "AZURE_OPENAI_ENDPOINTとAZURE_OPENAI_API_KEYを設定してください。"
        )
    
    client = AzureOpenAI(
        azure_endpoint=endpoint,
        api_key=api_key,
        api_version=api_version
    )
    
    return client


def print_separator():
    """視覚的な区切り線を表示"""
    print("\n" + "=" * 80 + "\n")


def print_result(result):
    """結果を整形して表示"""
    print_separator()
    print("【最終回答】")
    print_separator()
    print(result["final_response"])
    print_separator()
    
    print("\n【処理の詳細】")
    print(f"- 質問タイプ: {result['classification'].get('type', 'N/A')}")
    print(f"- 使用されたエージェント: {', '.join(result['agents_used'])}")
    print(f"- 処理結果: {'成功' if result['success'] else '失敗'}")
    
    if len(result['individual_responses']) > 1:
        print("\n【各エージェントの個別回答】")
        for resp in result['individual_responses']:
            print(f"\n■ {resp['agent']} ({resp['specialty']})")
            print(f"{resp['response'][:200]}..." if len(resp['response']) > 200 else resp['response'])


def run_demo():
    """デモを実行"""
    print("=" * 80)
    print("マルチエージェントデモシステム")
    print("Multi-Agent Demo System with Azure OpenAI")
    print("=" * 80)
    
    try:
        # クライアント初期化
        print("\n[システム] Azure OpenAIクライアントを初期化中...")
        client = initialize_client()
        deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4")
        print(f"[システム] デプロイメント名: {deployment_name}")
        
        # オーケストレーター初期化
        print("[システム] オーケストレーターを初期化中...")
        orchestrator = OrchestratorAgent(client, deployment_name)
        print("[システム] 初期化完了！\n")
        
        # デモ質問
        demo_queries = [
            "Pythonでマルチエージェントシステムを実装する方法を教えてください。",
            "新しいAIスタートアップの収益モデルについて教えてください。",
            "AIエージェントシステムのビジネス活用と技術アーキテクチャについて教えてください。"
        ]
        
        print("=" * 80)
        print("デモモード: 3つのサンプル質問を処理します")
        print("=" * 80)
        
        for i, query in enumerate(demo_queries, 1):
            print(f"\n\n{'#' * 80}")
            print(f"質問 {i}/{len(demo_queries)}")
            print(f"{'#' * 80}")
            print(f"\n質問: {query}")
            
            result = orchestrator.process(query)
            print_result(result)
        
        # インタラクティブモード
        print("\n\n" + "=" * 80)
        print("インタラクティブモード（'exit'または'quit'で終了）")
        print("=" * 80)
        
        while True:
            try:
                query = input("\n質問を入力してください: ").strip()
                
                if query.lower() in ['exit', 'quit', '終了']:
                    print("\nシステムを終了します。")
                    break
                
                if not query:
                    print("質問を入力してください。")
                    continue
                
                result = orchestrator.process(query)
                print_result(result)
                
            except KeyboardInterrupt:
                print("\n\nシステムを終了します。")
                break
    
    except Exception as e:
        print(f"\n[エラー] {str(e)}")
        print("\nセットアップ手順:")
        print("1. .env.exampleを.envにコピー")
        print("2. .envファイルに正しいAzure OpenAI設定を記入")
        print("3. requirements.txtから依存関係をインストール")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(run_demo())
