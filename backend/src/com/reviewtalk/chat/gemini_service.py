import os
from typing import Any
import google.generativeai as genai # 추후 주석 해제 및 설치 필요
from .base_service import BaseChatService
from loguru import logger # loguru 임포트

class GeminiChatService(BaseChatService):
    
    """Gemini 기반 챗봇 서비스"""
    def __init__(self, api_key: str | None = None):
        
        try:
            # 환경변수에서 키 가져오기
            self.api_key = api_key or os.getenv("GEMINI_API_KEY")
            logger.debug(f"[Gemini] Key is None:{self.api_key is None} ")
            if not self.api_key:
                logger.error("GEMINI_API_KEY 환경 변수가 설정되지 않았습니다.")
                raise ValueError("GEMINI_API_KEY가 필요합니다. .env 파일에 설정해주세요.")
            
            # API 키 설정
            genai.configure(api_key=self.api_key) # 추후 주석 해제
            
            # 모델 초기화
            self.model = genai.GenerativeModel('gemini-2.0-flash') # 추후 주석 해제
        except Exception as e:
            logger.error(f"Gemini 초기화 중 오류 발생: {str(e)}")
            logger.error(f"상세 에러: {traceback.format_exc()}")
            raise
        
    async def get_answer(self, user_message: str) -> str:
        """사용자 메시지와 custom_context를 결합해 Gemini에 질의"""
        custom_context = "나는 상담가야."
        
        # TODO: Gemini API 호출 구현
        # 예시:
        try:
            if self.model is None:
                logger.warning("Gemini 모델이 초기화되지 않았습니다. API 키를 확인해주세요.")
            
            logger.debug(f"[Gemini Service] Generating content: {custom_context}\n사용자: {user_message}\n상담가:")
            response = await self.model.generate_content_async(
                f"{custom_context}\n사용자: {user_message}\n상담가:"
            )
            return response.text.strip()
        except Exception as e:
            logger.error(f"[Gemini Service ERROR] API call failed: {type(e).__name__} - {e}")
            raise RuntimeError(f"Gemini API 호출 실패: {e}") from e
        
        # 임시 구현: 어떤 메시지가 왔는지 반환
        # print(f"[Gemini Service] Received message: {user_message}")
        # return f"[Gemini 응답 - 구현 예정] {user_message}" 