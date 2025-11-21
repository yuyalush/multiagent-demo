"""
Orchestrator Agent: マルチエージェントシステムのオーケストレーター
Coordinates between sub-agents to provide comprehensive answers
"""
import json
from typing import Dict, Any, List
from technical_agent import TechnicalAgent
from business_agent import BusinessAgent


class OrchestratorAgent:
    """複数のサブエージェントを調整するオーケストレーター"""
    
    def __init__(self, client, deployment_name: str):
        self.client = client
        self.deployment_name = deployment_name
        self.name = "OrchestratorAgent"
        
        # サブエージェントの初期化
        self.technical_agent = TechnicalAgent(client, deployment_name)
        self.business_agent = BusinessAgent(client, deployment_name)
    
    def classify_query(self, query: str) -> Dict[str, Any]:
        """
        質問を分類し、どのエージェントが適切かを判断する
        
        Args:
            query: ユーザーからの質問
            
        Returns:
            分類結果を含む辞書
        """
        classification_prompt = f"""以下の質問を分析して、どのタイプの専門家が答えるべきかを判断してください。

質問: {query}

選択肢:
1. technical - 技術的な質問（プログラミング、アーキテクチャ、技術仕様など）
2. business - ビジネス関連の質問（戦略、市場分析、収益モデルなど）
3. both - 両方の観点が必要な質問
4. general - 一般的な質問（どちらでもない）

以下のJSON形式で答えてください:
{{"type": "technical/business/both/general", "reasoning": "判断理由"}}"""

        try:
            messages = [
                {"role": "system", "content": "あなたは質問を分類する専門家です。JSON形式で正確に回答してください。"},
                {"role": "user", "content": classification_prompt}
            ]
            
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=messages,
                temperature=0.3,
                max_tokens=200
            )
            
            content = response.choices[0].message.content
            # JSONパースを試みる
            try:
                result = json.loads(content)
                return result
            except (json.JSONDecodeError, ValueError):
                # JSON形式でない場合は、キーワードから判断
                content_lower = content.lower()
                if "technical" in content_lower:
                    return {"type": "technical", "reasoning": content}
                elif "business" in content_lower:
                    return {"type": "business", "reasoning": content}
                elif "both" in content_lower:
                    return {"type": "both", "reasoning": content}
                else:
                    return {"type": "general", "reasoning": content}
                    
        except Exception as e:
            return {"type": "general", "reasoning": f"分類エラー: {str(e)}"}
    
    def synthesize_responses(self, query: str, responses: List[Dict[str, Any]]) -> str:
        """
        複数のエージェントからの応答を統合する
        
        Args:
            query: 元の質問
            responses: 各エージェントからの応答リスト
            
        Returns:
            統合された応答
        """
        if len(responses) == 1:
            return responses[0]["response"]
        
        # 複数の応答を統合
        synthesis_prompt = f"""以下の質問に対して、複数の専門家から回答が得られました。
これらの回答を統合して、包括的で一貫性のある最終回答を作成してください。

質問: {query}

専門家の回答:
"""
        for resp in responses:
            synthesis_prompt += f"\n[{resp['agent']} - {resp['specialty']}]\n{resp['response']}\n"
        
        synthesis_prompt += "\n上記の専門家の意見を踏まえて、統合された包括的な回答を提供してください。"
        
        try:
            messages = [
                {"role": "system", "content": "あなたは複数の専門家の意見を統合する調整役です。"},
                {"role": "user", "content": synthesis_prompt}
            ]
            
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=messages,
                temperature=0.7,
                max_tokens=800
            )
            
            return response.choices[0].message.content
        except Exception as e:
            # エラー時は単純に結合
            combined = "\n\n".join([f"【{r['agent']}の回答】\n{r['response']}" for r in responses])
            return combined
    
    def process(self, query: str) -> Dict[str, Any]:
        """
        質問を処理し、適切なサブエージェントに振り分けて回答を生成する
        
        Args:
            query: ユーザーからの質問
            
        Returns:
            処理結果を含む辞書
        """
        print(f"\n[{self.name}] 質問を分析中...")
        
        # 質問を分類
        classification = self.classify_query(query)
        query_type = classification.get("type", "general")
        
        print(f"[{self.name}] 質問タイプ: {query_type}")
        print(f"[{self.name}] 判断理由: {classification.get('reasoning', 'N/A')}")
        
        # エージェントに振り分け
        responses = []
        
        if query_type == "technical":
            print(f"\n[{self.name}] {self.technical_agent.name}に質問を転送...")
            response = self.technical_agent.process(query)
            responses.append(response)
            
        elif query_type == "business":
            print(f"\n[{self.name}] {self.business_agent.name}に質問を転送...")
            response = self.business_agent.process(query)
            responses.append(response)
            
        elif query_type == "both":
            print(f"\n[{self.name}] 両方のエージェントに質問を転送...")
            tech_response = self.technical_agent.process(query)
            business_response = self.business_agent.process(query)
            responses.extend([tech_response, business_response])
            
        else:  # general
            print(f"\n[{self.name}] 一般的な質問として処理...")
            # オーケストレーター自身が回答
            try:
                messages = [
                    {"role": "system", "content": "あなたは親切なアシスタントです。"},
                    {"role": "user", "content": query}
                ]
                
                response = self.client.chat.completions.create(
                    model=self.deployment_name,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=500
                )
                
                responses.append({
                    "agent": self.name,
                    "specialty": "一般的な質問",
                    "response": response.choices[0].message.content,
                    "success": True
                })
            except Exception as e:
                responses.append({
                    "agent": self.name,
                    "specialty": "一般的な質問",
                    "response": f"エラーが発生しました: {str(e)}",
                    "success": False,
                    "error": str(e)
                })
        
        # 応答を統合
        print(f"\n[{self.name}] 応答を統合中...")
        final_response = self.synthesize_responses(query, responses)
        
        return {
            "orchestrator": self.name,
            "query": query,
            "classification": classification,
            "agents_used": [r["agent"] for r in responses],
            "individual_responses": responses,
            "final_response": final_response,
            "success": all(r.get("success", False) for r in responses)
        }
