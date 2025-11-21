"""
Sub-Agent 1: 技術仕様エージェント
Technical Specification Agent - Handles technical questions and specifications
"""
from typing import Dict, Any


class TechnicalAgent:
    """技術的な質問に特化したサブエージェント"""
    
    def __init__(self, client, deployment_name: str):
        self.client = client
        self.deployment_name = deployment_name
        self.name = "TechnicalAgent"
        self.specialty = "技術仕様と実装の詳細"
    
    def get_system_prompt(self) -> str:
        """エージェントのシステムプロンプトを返す"""
        return """あなたは技術的な質問に特化したアシスタントです。
プログラミング、アーキテクチャ、技術仕様に関する質問に答えます。
簡潔で正確な技術情報を提供してください。"""
    
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
