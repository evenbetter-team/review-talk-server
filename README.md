# 리뷰톡 ReviewTalk

제품에 대한 URL만 입력하면, 챗봇이 수많은 리뷰를 분석해 간결한 답변을 제공해주는 AI 리뷰 요약 시스템입니다.

이 프로젝트는 **Flutter 기반의 모바일 앱(Frontend)** 과 **FastAPI 기반의 백엔드 API 서버(Backend)** 로 구성되어 있으며, 각 파트는 독립적인 프로젝트 구조를 따릅니다.

---

## 프로젝트 구조

```
review-talk/
├── frontend/ # Flutter 앱 (모바일 UI, 챗봇 인터페이스)
├── backend/ # FastAPI 서버 (크롤링, 리뷰 처리, 챗봇 API)
├── README.md # 메인 프로젝트 설명 파일 (현재 문서)

```

## 프론트엔드 (Flutter)

- URL 입력 및 갤러리/챗봇 UI 구현
- 제품별 챗봇 인터페이스
- 캐비넷 기능 (사용자 상품 정리)
- 백엔드 API와 연동

> 위치: `frontend/`

---

## 백엔드 (FastAPI)

- URL 기반 제품 정보 및 리뷰 크롤링
- 리뷰 데이터 임베딩 및 pgvector 저장
- 유사도 기반 리뷰 검색 및 응답 생성 (LangChain 기반 RAG)
- 챗봇 세션 및 사용자 히스토리 관리

> 위치: `backend/`

---

## 기술 스택

### Frontend
- Flutter
- Dart
- Firebase (옵션: 인증 및 배포)

### Backend
- FastAPI
- PostgreSQL (Supabase + pgvector)
- LangChain, FAISS
- OpenAI API

---

## 실행 방법

각 디렉토리(`frontend/`, `backend/`) 내부의 README 또는 실행 가이드를 참고하세요. 
멀티 프로젝트 구조로 구성되어 있으므로, Flutter 앱과 FastAPI 서버는 각각 독립적으로 실행/배포됩니다.

---

## 라이선스
이 프로젝트는 내부 부트캠프용으로 진행되며, 외부 배포 전 별도 고지가 필요합니다.
