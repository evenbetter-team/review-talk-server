from abc import ABC, abstractmethod

class BaseChatService(ABC):
    """채팅 서비스 추상 베이스 클래스"""

    @abstractmethod
    async def get_answer(self, user_message: str) -> str:
        """사용자 메시지에 대한 답변을 생성하여 반환"""
        pass 