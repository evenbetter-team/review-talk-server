from fastapi import APIRouter, Depends, status, HTTPException, Path
from src.com.reviewtalk.chat.schemas import ChatRequest, ChatResponse
from src.com.reviewtalk.chat.storage import ChatHistoryStorage
from src.com.reviewtalk.chat.factory import ChatServiceFactory
from src.com.reviewtalk.chat.base_service import BaseChatService
from typing import List
from loguru import logger

router = APIRouter(prefix="/api/v1", tags=["Chat"])

# 의존성 주입용 인스턴스 생성 함수 (팩토리 사용)
def get_chat_service() -> BaseChatService:
    return ChatServiceFactory.get_service()

def get_chat_storage() -> ChatHistoryStorage:
    return ChatHistoryStorage()

@router.get("/users/{user_id}/chats/{chat_id}", response_model=List[ChatResponse], status_code=status.HTTP_200_OK)
async def get_chat_history(
    user_id: str = Path(..., description="사용자 ID"),
    chat_id: str = Path(..., description="채팅 ID"),
    storage: ChatHistoryStorage = Depends(get_chat_storage)
) -> List[ChatResponse]:
    
    """특정 상품의 채팅 내역 조회"""
    logger.debug("-" * 30)
    logger.debug(f"[INFO] get_chat_history: {chat_id}")
    logger.debug("-" * 30)
    return await storage.get_history(chat_id)

@router.post("/users/{user_id}/chats/{chat_id}", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def chat_with_bot(
    user_id: str = Path(..., description="사용자 ID"),
    chat_id: str = Path(..., description="채팅 ID"),
    req: ChatRequest = ...,
    service: BaseChatService = Depends(get_chat_service),
    storage: ChatHistoryStorage = Depends(get_chat_storage)
) -> ChatResponse:
    """메시지 전송 및 답변 반환, 내역 저장"""
    try:
        
        logger.debug("-" * 30)
        logger.debug(f"[INFO] chat_with_bot: {chat_id}")
        logger.debug("-" * 30)
        
        answer = await service.get_answer(req.message)
        logger.debug("-" * 30)
        logger.debug(f"[INFO] answer: {answer}")
        logger.debug("-" * 30)
        
        await storage.save_message(chat_id, req.message, answer)
        logger.debug("-" * 30)
        logger.debug(f"[INFO] save_message: {chat_id}")
        logger.debug("-" * 30)
        
        return ChatResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"챗봇 서비스 오류 발생") 