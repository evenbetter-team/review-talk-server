from abc import ABC, abstractmethod
from typing import Any

class BaseCrawler(ABC):
    """크롤러 베이스 클래스 (공통 인터페이스 정의)"""

    @abstractmethod
    async def fetch(self, url: str, **kwargs) -> Any:
        """URL에서 데이터를 비동기로 가져옴"""
        pass

    @abstractmethod
    async def parse(self, html: str, **kwargs) -> Any:
        """HTML 파싱 및 데이터 추출"""
        pass 