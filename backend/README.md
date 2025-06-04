# ReviewTalk - 제품 리뷰 기반 AI 챗봇 백엔드

ReviewTalk 백엔드는 FastAPI를 기반으로 하며, 사용자 질문에 대해 제품 리뷰 데이터를 활용하여 AI(LLM) 기반의 답변을 제공하고 채팅 내역을 관리합니다.

## 주요 기술 스택

-   **웹 프레임워크**: FastAPI
-   **비동기 서버**: Uvicorn
-   **데이터베이스**: Supabase (PostgreSQL + pgvector)
-   **AI 연동**: OpenAI, Google Gemini (LangChain)
-   **웹 크롤링**: Playwright, BeautifulSoup (크롤링 기능 분리)
-   **패키지 관리**: uv
-   **환경 설정**: python-dotenv
-   **로깅**: loguru (기본 로깅 사용)
-   **기타**: httpx, asyncpg, sqlalchemy, pydantic, tqdm 등

---

## 프로젝트 구조

```
backend/
├── src/com/reviewtalk/
│   ├── chat/            # 채팅 서비스 및 로직 (OpenAI/Gemini 서비스, 저장소, 팩토리)
│   │   ├── __init__.py
│   │   ├── base_service.py
│   │   ├── factory.py
│   │   ├── gemini_service.py
│   │   ├── openai_service.py
│   │   ├── schemas.py
│   │   └── storage.py
│   ├── router/          # API 라우터 정의 (RESTful, WebSocket)
│   │   ├── __init__.py
│   │   ├── chat.py
│   │   └── chat_ws.py
│   ├── ... (기타 도메인/모듈)
│   ├── crawl/             # 웹 크롤링 전용 모듈
│   ├── __init__.py
│   ├── base.py
│   └── danawa_review_crawler.py
├── main.py            # FastAPI 앱 진입점 및 기본 설정
├── .env.example       # 환경 변수 예시 
├── pyproject.toml     # uv 의존성 관리 파일
├── README.md          # 프로젝트 설명
└── ... (ignore 파일 및 배포 관련 파일)
```

---

## 설치 및 실행

이 프로젝트는 `uv`를 사용하여 패키지를 관리합니다. Python 3.11 이상 버전을 권장합니다.

### 1. 의존성 설치

```bash
cd backend
uv sync
```

### 2. Playwright 브라우저 엔진 설치 (최초 1회)

크롤링 기능을 사용하려면 Playwright 브라우저 엔진이 필요합니다.

```bash
cd backend
uv run playwright install chromium
```

### 3. 환경 변수 설정

`backend/` 디렉토리에 `.env` 파일을 생성하고 `.env.example`을 참고하여 필요한 환경 변수를 설정합니다.

```dotenv
# backend/.env
DATABASE_URL=postgresql+asyncpg://user:password@host:port/dbname
OPENAI_API_KEY=your_openai_key # OpenAI API 키
GEMINI_API_KEY=your_gemini_key # Gemini API 키
AI_TYPE=openai # 사용하려는 AI 모델 ('openai' 또는 'gemini')
LOG_LEVEL=INFO # 로깅 레벨 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
DEBUG=True # 개발 모드 설정 (상세 에러 메시지 활성화)
# 기타 필요한 환경 변수...
```

**주의**: `.env` 파일은 `.gitignore`에 의해 Git 추적에서 제외됩니다. 민감한 정보는 `.env` 파일에 저장하고, `.env.example`은 구조만 제공합니다.

### 4. FastAPI 서버 실행

```bash
cd backend
uv run main.py
```

서버는 기본적으로 `http://0.0.0.0:8000`에서 실행됩니다.

---

## API 엔드포인트

-   **헬스 체크**: `GET /ping`
-   **채팅 (RESTful)**:
    -   채팅 내역 조회: `GET /api/v1/users/{user_id}/chats/{chat_id}`
    -   메시지 전송 및 답변: `POST /api/v1/users/{user_id}/chats/{chat_id}`
-   **채팅 (WebSocket)**:
    -   실시간 채팅 연결: `ws://.../ws/v1/users/{user_id}/chats/{chat_id}`

---

## 주요 기능 구현 현황

-   FastAPI 앱 초기 설정 (환경 변수, 로깅, 예외 처리)
-   CORS 미들웨어 설정
-   채팅 서비스 추상화 및 OpenAI/Gemini 서비스 분리 (Factory 패턴 적용)
-   RESTful 및 WebSocket 채팅 API 구현
-   상품별 채팅 내역 임시 저장소 구현 (메모리 기반)
-   웹 크롤링 모듈 구조 분리 (구현 예정)

---

## 향후 계획

-   Supabase를 활용한 채팅 내역 영구 저장 구현
-   사용자 인증 및 권한 부여 기능 구현
-   제품 리뷰 데이터 기반 RAG (Retrieval-Augmented Generation) 로직 구현
-   Playwright를 사용한 웹 크롤링 기능 완성
-   CI/CD 파이프라인 구축

---

📜 라이선스
MIT License © 2025 오히려좋아 Community
