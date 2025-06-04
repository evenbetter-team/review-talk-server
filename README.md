# 리뷰톡 ReviewTalk

제품에 대한 URL만 입력하면, 챗봇이 수많은 리뷰를 분석해 간결한 답변을 제공해주는 AI 리뷰 요약 시스템입니다.

이 프로젝트는 **Vue.js 기반의 어드민 클라이언트(front-admin)** 와 **FastAPI 기반의 백엔드 API 서버(backend)** 로 구성되어 있으며, 각 파트는 독립적인 프로젝트 구조를 따릅니다.

---

## 프로젝트 구조

```
review-talk/
├── front-admin/ # Vue.js 기반 어드민 클라이언트 (채팅 화면 등)
├── backend/ # FastAPI 서버 (크롤링, 리뷰 처리, 챗봇 API, 사용자 관리 등)
├── README.md # 메인 프로젝트 설명 파일 (현재 문서)

```

## 프론트엔드 (Vue.js Admin)

-   URL 기반 채팅 세션 시작 및 관리
-   사용자/챗봇 메시지 실시간 표시
-   채팅 내역 조회 및 메시지 전송
-   백엔드 API 및 WebSocket과 연동

> 위치: `front-admin/`

---

## 백엔드 (FastAPI)

-   URL 기반 제품 정보 및 리뷰 크롤링 (구현 예정)
-   리뷰 데이터 처리 및 저장 (구현 예정)
-   AI(OpenAI/Gemini)를 활용한 리뷰 기반 답변 생성 (구현 중)
-   사용자별 채팅 세션 및 내역 관리 (구현 중)
-   RESTful API 및 WebSocket 엔드포인트 제공

> 위치: `backend/`

---

## 기술 스택

### Frontend (front-admin)
-   Vue.js 3
-   Vite
-   Axios (HTTP 통신)
-   WebSocket

### Backend
-   FastAPI
-   Python 3.11+
-   uv (패키지 관리)
-   Supabase (PostgreSQL + pgvector) (예정)
-   LangChain (예정)
-   OpenAI API / Google Gemini API
-   Playwright, BeautifulSoup (크롤링, 예정)
-   loguru (로깅)
-   python-dotenv (환경 변수)

---

## 실행 방법

각 디렉토리(`front-admin/`, `backend/`) 내부의 README 파일을 참고하세요. 
각 파트는 독립적으로 실행/배포됩니다.

---

## 라이선스
이 프로젝트는 내부 부트캠프용으로 진행되며, 외부 배포 전 별도 고지가 필요합니다.
