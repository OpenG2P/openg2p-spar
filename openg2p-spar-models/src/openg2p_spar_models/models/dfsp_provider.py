from enum import Enum
from typing import Optional

from openg2p_fastapi_common.context import dbengine
from openg2p_fastapi_common.models import BaseORMModelWithTimes
from sqlalchemy import String, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column


class ProviderType(str, Enum):
    """Enum for DFSP provider types"""

    BANK = "BANK"
    EMAIL_WALLET = "EMAIL_WALLET"
    MOBILE_WALLET = "MOBILE_WALLET"


class DfspProvider(BaseORMModelWithTimes):
    """
    DfspProvider model for top-level provider types.

    Represents the main provider categories: BANK, EMAIL_WALLET, MOBILE_WALLET.

    Attributes:
        code: Unique identifier (e.g., "BANK", "EMAIL_WALLET", "MOBILE_WALLET")
        name: Display name
        provider_type: Type of provider (BANK, EMAIL_WALLET, MOBILE_WALLET)
        description: Optional description
        validation_regex: Optional regex pattern for validating codes
    """

    __tablename__ = "dfsp_provider"

    code: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True, index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    provider_type: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True, index=True
    )
    description: Mapped[Optional[str]] = mapped_column(String(), nullable=True)
    validation_regex: Mapped[Optional[str]] = mapped_column(String(), nullable=True)

    @classmethod
    async def get_all_providers(cls):
        """
        Get all providers.

        Returns:
            List of DfspProvider objects
        """
        session = AsyncSession(dbengine.get())
        try:
            stmt = select(cls).order_by(cls.name.asc())
            result = await session.execute(stmt)
            return list(result.scalars())
        finally:
            await session.aclose()

    @classmethod
    async def get_provider_by_type(cls, provider_type: str):
        """
        Get a provider by type.

        Args:
            provider_type: The provider type (BANK, EMAIL_WALLET, MOBILE_WALLET)

        Returns:
            DfspProvider object or None if not found
        """
        session = AsyncSession(dbengine.get())
        try:
            stmt = select(cls).where(cls.provider_type == provider_type)
            result = await session.execute(stmt)
            return result.scalars().first()
        finally:
            await session.aclose()

    @classmethod
    async def get_provider_by_code(cls, code: str):
        """
        Get a provider by code.

        Args:
            code: The provider code

        Returns:
            DfspProvider object or None if not found
        """
        session = AsyncSession(dbengine.get())
        try:
            stmt = select(cls).where(cls.code == code)
            result = await session.execute(stmt)
            return result.scalars().first()
        finally:
            await session.aclose()
