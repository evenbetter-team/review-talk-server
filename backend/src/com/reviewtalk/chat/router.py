from fastapi import APIRouter, Depends, status, HTTPException
from .schemas import ChatRequest, ChatResponse
from .service import ChatService

router = APIRouter(prefix="/api/v1/chat", tags=["Chat"])

# 의존성 주입용 인스턴스 생성 함수
def get_chat_service() -> ChatService:
    return ChatService()

@router.post("/", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def chat_with_bot(
    req: ChatRequest,
    service: ChatService = Depends(get_chat_service)
) -> ChatResponse:
    """Flutter 클라이언트와 통신하는 챗봇 API"""
    try:
        answer = await service.get_answer(req.message)
        return ChatResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API 오류: {e}") 