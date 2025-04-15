from typing import Any, Dict, List, Optional, TypeVar, Generic
from src.core.database.connection import prisma_connection

T = TypeVar("T")


class BaseRepository(Generic[T]):
    """
    기본 Repository 클래스로 Prisma ORM을 사용한 CRUD 작업을 제공합니다.
    """

    def __init__(self, model_name: str):
        self.prisma = prisma_connection.prisma
        self.model = getattr(self.prisma, model_name)

    async def find_many(
        self,
        where: Optional[Dict[str, Any]] = None,
        order: Optional[Dict[str, str]] = None,
        include: Optional[Dict[str, bool]] = None,
        skip: Optional[int] = None,
        take: Optional[int] = None,
    ) -> List[T]:
        """
        여러 레코드를 조회합니다.
        """
        return await self.model.find_many(
            where=where, order=order, include=include, skip=skip, take=take
        )

    async def find_unique(
        self, where: Dict[str, Any], include: Optional[Dict[str, bool]] = None
    ) -> Optional[T]:
        """
        고유 조건으로 단일 레코드를 조회합니다.
        """
        return await self.model.find_unique(where=where, include=include)

    async def find_first(
        self, where: Dict[str, Any], include: Optional[Dict[str, bool]] = None
    ) -> Optional[T]:
        """
        조건에 맞는 첫 번째 레코드를 조회합니다.
        """
        return await self.model.find_first(where=where, include=include)

    async def create(
        self, data: Dict[str, Any], include: Optional[Dict[str, bool]] = None
    ) -> T:
        """
        새 레코드를 생성합니다.
        """
        return await self.model.create(data=data, include=include)

    async def update(
        self,
        where: Dict[str, Any],
        data: Dict[str, Any],
        include: Optional[Dict[str, bool]] = None,
    ) -> T:
        """
        레코드를 업데이트합니다.
        """
        return await self.model.update(where=where, data=data, include=include)

    async def delete(self, where: Dict[str, Any]) -> T:
        """
        레코드를 삭제합니다.
        """
        return await self.model.delete(where=where)

    async def count(self, where: Optional[Dict[str, Any]] = None) -> int:
        """
        조건에 맞는 레코드 수를 반환합니다.
        """
        return await self.model.count(where=where)
