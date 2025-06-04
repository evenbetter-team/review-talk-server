import os
from typing import Literal
from .base_service import BaseChatService
from .openai_service import OpenAIChatService
from .gemini_service import GeminiChatService

AIType = Literal["openai", "gemini"]

class ChatServiceFactory:
    """AI 서비스 팩토리"""

    @staticmethod
    def get_service(ai_type: str | None = None) -> BaseChatService:
        """환경 변수 AI_TYPE에 따라 적절한 ChatService 인스턴스 반환"""
        # 환경 변수에서 AI_TYPE 읽기 (기본값: openai)
        selected_ai_type = (ai_type or os.getenv("AI_TYPE", "openai")).lower()

        if selected_ai_type == "gemini":
            return GeminiChatService()
        elif selected_ai_type == "openai":
            return OpenAIChatService()
        else:
            raise ValueError(f"지원하지 않는 AI 타입: {selected_ai_type}. 'openai' 또는 'gemini' 중 선택해주세요.") 