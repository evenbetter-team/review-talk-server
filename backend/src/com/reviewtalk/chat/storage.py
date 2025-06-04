import asyncio
from typing import List
from .schemas import ChatResponse

class ChatHistoryStorage:
    """채팅 내역 임시 저장소 (product_id별)"""
    _history: dict[str, list[ChatResponse]] = {}
    _lock = asyncio.Lock()

    async def save_message(self, product_id: str, user_message: str, answer: str) -> None:
        async with self._lock:
            if product_id not in self._history:
                self._history[product_id] = []
            self._history[product_id].append(ChatResponse(answer=answer))

    async def get_history(self, product_id: str) -> List[ChatResponse]:
        async with self._lock:
            return list(self._history.get(product_id, [])) 