from typing import Any
from .base import BaseCrawler

class DanawaReviewCrawler(BaseCrawler):
    """다나와 제품 리뷰 크롤러 (Playwright 기반)"""

    async def fetch(self, url: str, **kwargs) -> str:
        """Playwright로 페이지 HTML을 비동기로 가져옴 (구현 예정)"""
        # TODO: Playwright 비동기 fetch 구현
        raise NotImplementedError

    async def parse(self, html: str, **kwargs) -> list[dict[str, Any]]:
        """BeautifulSoup로 리뷰 데이터 파싱 (구현 예정)"""
        # TODO: BeautifulSoup 파싱 구현
        raise NotImplementedError 