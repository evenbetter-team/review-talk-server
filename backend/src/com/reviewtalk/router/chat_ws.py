from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Path, status
from src.com.reviewtalk.chat.storage import ChatHistoryStorage
from src.com.reviewtalk.chat.factory import ChatServiceFactory
from src.com.reviewtalk.chat.base_service import BaseChatService
from typing import Dict
from loguru import logger

router = APIRouter(prefix="/ws/v1", tags=["Chat-WS"])

# WebSocket 연결 관리 (메모리)
active_connections: Dict[str, set[WebSocket]] = {}

@router.websocket("/users/{user_id}/chats/{chat_id}")
async def websocket_chat(
    websocket: WebSocket,
    user_id: str = Path(..., description="사용자 ID"),
    chat_id: str = Path(..., description="채팅 ID")
):
    await websocket.accept()
    if chat_id not in active_connections:
        active_connections[chat_id] = set()
    active_connections[chat_id].add(websocket)

    # 서비스 팩토리를 사용하여 서비스 인스턴스 생성
    service: BaseChatService = ChatServiceFactory.get_service()

    storage = ChatHistoryStorage()
    try:
        while True:
            data = await websocket.receive_text()
            # AI 서비스 호출
            answer = await service.get_answer(data)

            # 내역 저장
            await storage.save_message(chat_id, data, answer)

            # 사용자에게 답변 전송
            await websocket.send_text(answer)
    except WebSocketDisconnect:
        active_connections[chat_id].remove(websocket)
    except Exception as e:
        logger.debug(f"[WebSocket ERROR] Unhandled Exception in WebSocket: {e}")
        # 클라이언트에게 에러 메시지 전송 (선택 사항)
        # await websocket.send_text(f"오류 발생: {e}")
        if chat_id in active_connections and websocket in active_connections[chat_id]: # 연결 종료 시 에러 방지
            active_connections[chat_id].remove(websocket) 