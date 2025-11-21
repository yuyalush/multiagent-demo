"""
Sub-Agent 2: ビジネス分析エージェント
Business Analysis Agent - Handles business and strategy questions
"""
from typing import Dict, Any


class BusinessAgent:
    """ビジネスと戦略の質問に特化したサブエージェント"""
    
    def __init__(self, client, deployment_name: str):
        self.client = client
        self.deployment_name = deployment_name
        self.name = "BusinessAgent"
        self.specialty = "ビジネス戦略と市場分析"
    
    def get_system_prompt(self) -> str:
        """エージェントのシステムプロンプトを返す"""
        return """あなたはビジネス分析に特化したアシスタントです。
ビジネス戦略、市場分析、収益モデルに関する質問に答えます。
実践的なビジネスアドバイスを提供してください。"""
    
    def process(self, query: str) -> Dict[str, Any]:
        """
        クエリを処理して応答を返す
        
        Args:
            query: ユーザーからの質問
            
        Returns:
            エージェントの応答を含む辞書
        """
        try:
            messages = [
                {"role": "system", "content": self.get_system_prompt()},
                {"role": "user", "content": query}
            ]
            
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            
            return {
                "agent": self.name,
                "specialty": self.specialty,
                "response": response.choices[0].message.content,
                "success": True
            }
        except Exception as e:
            return {
                "agent": self.name,
                "specialty": self.specialty,
                "response": f"エラーが発生しました: {str(e)}",
                "success": False,
                "error": str(e)
            }
