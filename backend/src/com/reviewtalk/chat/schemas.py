from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    message: str = Field(..., description="사용자 입력 메시지")

class ChatResponse(BaseModel):
    answer: str = Field(..., description="챗봇 답변") 