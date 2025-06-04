import os
import openai
from typing import Any
from .base_service import BaseChatService # Import the base class
from loguru import logger # loguru 임포트

class OpenAIChatService(BaseChatService):
    """OpenAI 기반 챗봇 서비스"""
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        logger.debug(f"[OpenAI] Key is None:{self.api_key is None} ")
        if not self.api_key:
             raise ValueError("OPENAI_API_KEY environment variable not set")
        openai.api_key = self.api_key

    async def get_answer(self, user_message: str) -> str:
        """사용자 메시지와 custom_context를 결합해 OpenAI에 질의"""
        custom_context = "나는 상담가야."
        # OpenAI Chat API 호출 (gpt-3.5-turbo 예시)
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4.0-mini",
                messages=[
                    {"role": "system", "content": custom_context},
                    {"role": "user", "content": user_message},
                ],
                max_tokens=512,
                temperature=0.7,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            # OpenAI API 호출 실패 시 예외 발생
            raise RuntimeError(f"OpenAI API 호출 실패: {e}") from e 