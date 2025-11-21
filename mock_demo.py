"""
Mock Demo - Demonstrates the multi-agent system flow without Azure OpenAI
This script shows how the system works using mock responses
"""


class MockClient:
    """Mock Azure OpenAI client for demonstration"""
    
    class Completions:
        def create(self, **kwargs):
            # Return a mock response based on the system prompt
            messages = kwargs.get('messages', [])
            
            # Get the user query
            user_message = ""
            for msg in messages:
                if msg.get('role') == 'user':
                    user_message = msg.get('content', '')
                    break
            
            # Generate mock response based on content
            if "JSON" in user_message or "type" in user_message:
                # Classification request
                if any(word in user_message.lower() for word in ['python', '実装', '技術', 'プログラミング']):
                    content = '{"type": "technical", "reasoning": "この質問は技術的な実装に関するものです"}'
                elif any(word in user_message.lower() for word in ['ビジネス', '収益', '戦略', 'スタートアップ']):
                    content = '{"type": "business", "reasoning": "この質問はビジネス戦略に関するものです"}'
                elif any(word in user_message.lower() for word in ['ai', 'エージェント']) and any(word in user_message.lower() for word in ['ビジネス', '活用']):
                    content = '{"type": "both", "reasoning": "この質問には技術とビジネスの両面が含まれます"}'
                else:
                    content = '{"type": "general", "reasoning": "一般的な質問です"}'
            elif "専門家の回答" in user_message or "統合" in user_message:
                # Synthesis request
                content = "技術面とビジネス面の両方から総合的に検討すると、AIエージェントシステムは実装可能であり、明確なビジネス価値を提供できます。技術的には適切なアーキテクチャの選択が重要であり、ビジネス的には市場ニーズと収益モデルの確立が鍵となります。"
            elif "技術" in str(kwargs.get('messages', [])):
                # Technical agent response
                content = "【技術的な回答】Pythonでマルチエージェントシステムを実装する場合、オブジェクト指向設計を採用し、各エージェントをクラスとして実装するのが効果的です。Azure OpenAI SDKを使用することで、各エージェントがLLMの能力を活用できます。オーケストレーターパターンを用いて、エージェント間の調整を行います。"
            elif "ビジネス" in str(kwargs.get('messages', [])):
                # Business agent response
                content = "【ビジネス的な回答】AIスタートアップの収益モデルとしては、SaaS型のサブスクリプションモデル、API利用量に応じた従量課金制、エンタープライズ向けカスタマイズサービスなどが考えられます。初期段階では市場浸透を優先し、その後価値に基づく価格設定に移行するのが一般的です。"
            else:
                # General response
                content = "ご質問ありがとうございます。AIエージェントシステムは、複数の専門的なAIエージェントが協調して動作することで、より高度な問題解決が可能になります。技術的な実装とビジネス価値の両面から検討することが重要です。"
            
            return MockResponse(content)
    
    class Chat:
        def __init__(self):
            self.completions = MockClient.Completions()
    
    def __init__(self):
        self.chat = MockClient.Chat()


class MockResponse:
    """Mock response object"""
    
    def __init__(self, content):
        self.choices = [MockChoice(content)]


class MockChoice:
    """Mock choice object"""
    
    def __init__(self, content):
        self.message = MockMessage(content)


class MockMessage:
    """Mock message object"""
    
    def __init__(self, content):
        self.content = content


def run_mock_demo():
    """Run the multi-agent demo with mock responses"""
    from orchestrator_agent import OrchestratorAgent
    
    print("=" * 80)
    print("マルチエージェントデモシステム (Mock Version)")
    print("Multi-Agent Demo System with Mock Responses")
    print("=" * 80)
    print("\nNote: This is a demonstration using mock responses.")
    print("For real Azure OpenAI integration, use main.py with proper credentials.\n")
    
    # Initialize mock client
    mock_client = MockClient()
    deployment_name = "gpt-4-mock"
    
    print("[システム] Mockクライアントを初期化中...")
    print(f"[システム] デプロイメント名: {deployment_name}")
    
    # Initialize orchestrator
    print("[システム] オーケストレーターを初期化中...")
    orchestrator = OrchestratorAgent(mock_client, deployment_name)
    print("[システム] 初期化完了！\n")
    
    # Demo queries
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
        
        print("\n" + "=" * 80)
        print("【最終回答】")
        print("=" * 80)
        print(result["final_response"])
        print("=" * 80)
        
        print("\n【処理の詳細】")
        print(f"- 質問タイプ: {result['classification'].get('type', 'N/A')}")
        print(f"- 使用されたエージェント: {', '.join(result['agents_used'])}")
        print(f"- 処理結果: {'成功' if result['success'] else '失敗'}")
    
    print("\n\n" + "=" * 80)
    print("デモ完了")
    print("=" * 80)
    print("\n実際のAzure OpenAI Serviceを使用するには:")
    print("1. .env.exampleを.envにコピー")
    print("2. Azure OpenAI認証情報を設定")
    print("3. python main.py を実行")
    print("=" * 80)


if __name__ == "__main__":
    try:
        run_mock_demo()
    except Exception as e:
        print(f"\nエラー: {e}")
        import traceback
        traceback.print_exc()
