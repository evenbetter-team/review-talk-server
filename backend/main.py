import os
import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
import sys
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

# 로그 디렉토리 생성
def setup_logging():
    """로깅 설정 및 디렉토리 생성"""
    
    # 로그 디렉토리 생성
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        print(f"로그 디렉토리 생성: {os.path.abspath(log_dir)}")
    
    # 로거 설정
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # 기존 핸들러 제거 (중복 방지)
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # 포맷터 설정
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 1. 콘솔 핸들러 (기존처럼 터미널에도 출력)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # 2. 일반 로그 파일 핸들러 (크기별 로테이션)
    file_handler = RotatingFileHandler(
        filename=os.path.join(log_dir, "app.log"),
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,          # 최대 5개 파일 보관
        encoding='utf-8'
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # 3. 에러 전용 로그 파일 핸들러
    error_handler = RotatingFileHandler(
        filename=os.path.join(log_dir, "error.log"),
        maxBytes=10*1024*1024,  # 10MB
        backupCount=10,         # 에러는 더 많이 보관
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    logger.addHandler(error_handler)
    
    # 4. 일별 로그 파일 핸들러 (선택사항)
    daily_handler = TimedRotatingFileHandler(
        filename=os.path.join(log_dir, "daily.log"),
        when='midnight',
        interval=1,
        backupCount=30,  # 30일간 보관
        encoding='utf-8'
    )
    daily_handler.setLevel(logging.INFO)
    daily_handler.setFormatter(formatter)
    logger.addHandler(daily_handler)
    
    return logger

# 1. 환경 변수 로딩
load_dotenv()


# 로깅 설정 실행
logger = setup_logging()

# 로그 파일 경로 정보 출력
current_dir = os.getcwd()
log_paths = {
    "app.log": os.path.join(current_dir, "logs", "app.log"),
    "error.log": os.path.join(current_dir, "logs", "error.log"),
    "daily.log": os.path.join(current_dir, "logs", "daily.log")
}

print("\n=== 로그 파일 경로 ===")
for log_type, path in log_paths.items():
    print(f"{log_type}: {path}")
print("====================\n")


logger.debug(f"DEBUG env var: {os.getenv('DEBUG')}")
logger.debug(f"AI_TYPE env var: {os.getenv('AI_TYPE')}")
logger.debug(f"OPENAI_API_KEY env var (first few chars): {os.getenv('OPENAI_API_KEY')[:5] if os.getenv('OPENAI_API_KEY') else 'None'}")
logger.debug(f"GEMINI_API_KEY env var (first few chars): {os.getenv('GEMINI_API_KEY')[:5] if os.getenv('GEMINI_API_KEY') else 'None'}")

# 3. FastAPI 앱 생성
app = FastAPI(
    title="ReviewTalk Backend", 
    version="0.1.0")

# CORS 미들웨어 추가
origins = [
    "http://localhost:5173", # 프론트엔드 개발 서버 주소
    # 필요한 경우 여기에 다른 오리진을 추가
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # 모든 HTTP 메소드 허용 (GET, POST, OPTIONS 등)
    allow_headers=["*"], # 모든 헤더 허용
)

# router 디렉토리의 REST/WS 라우터 등록
from src.com.reviewtalk.router.chat import router as chat_router
from src.com.reviewtalk.router.chat_ws import router as chat_ws_router
app.include_router(chat_router)
app.include_router(chat_ws_router)

# 4. 예외 처리 예시 (상세 오류 포함)
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # print("--------------------------------") # print 대신 logger.debug 사용
    logger.debug("-" * 30)
    # print(f"[ERROR] Unhandled Exception: {exc}") # print 대신 logger.debug 사용
    logger.debug(f"[ERROR] Unhandled Exception: {exc}")
    logger.error(f"Unhandled error: {exc}", exc_info=True) # 트레이스백 로깅 유지

    # 환경 변수를 확인하여 개발 모드일 때 상세 오류 반환
    if os.getenv("DEBUG", "False").lower() == "true":
        content = {
            "detail": "Internal Server Error",
            "error": type(exc).__name__,
            "message": str(exc),
        }
    else:
        content = {"detail": "Internal Server Error"}

    return JSONResponse(status_code=500, content=content)

# 5. 기본 라우터
@app.get("/ping", tags=["Health"])
async def ping():
    """헬스 체크 엔드포인트"""
    return {"message": "pong"}

# 6. Playwright 설치 안내 (최초 1회만 필요)
# 터미널에서 아래 명령어 실행:
# uv run playwright install chromium

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


