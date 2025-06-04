import os
import openai
from typing import Any

class ChatService:
    """OpenAI 기반 챗봇 서비스"""
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        openai.api_key = self.api_key

    async def get_answer(self, user_message: str) -> str:
        """사용자 메시지와 custom_context를 결합해 OpenAI에 질의"""
        custom_context = "나는 상담가야."
        prompt = f"{custom_context}\n사용자: {user_message}\n상담가:"  # 단순 프롬프트
        # OpenAI Chat API 호출 (gpt-3.5-turbo 예시)
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": custom_context},
                {"role": "user", "content": user_message},
            ],
            max_tokens=512,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip() 