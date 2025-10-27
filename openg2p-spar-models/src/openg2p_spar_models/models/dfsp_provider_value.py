from typing import Optional

from openg2p_fastapi_common.context import dbengine
from openg2p_fastapi_common.models import BaseORMModelWithTimes
from sqlalchemy import ForeignKey, String, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship


class DfspProviderValue(BaseORMModelWithTimes):
    """
    DfspProviderValue model for provider details (e.g., banks, branches).
    
    Represents specific instances of providers. For BANK type, this includes
    individual banks and their branches. For EMAIL_WALLET and MOBILE_WALLET,
    these are the specific wallet providers.
    
    Attributes:
        code: Unique identifier (e.g., "ICIC", "HDFC", "BRANCH_001")
        name: Display name
        provider_type: Type of provider (BANK, EMAIL_WALLET, MOBILE_WALLET)
        parent_id: Foreign key to parent DfspProvider (for BANK branches)
        description: Optional description
        validation_regex: Optional regex pattern for validating codes
    """
    __tablename__ = "dfsp_provider_value"

    code: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    provider_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    parent_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("dfsp_provider_value.id"), nullable=True, index=True
    )
    description: Mapped[Optional[str]] = mapped_column(String(), nullable=True)
    validation_regex: Mapped[Optional[str]] = mapped_column(String(), nullable=True)

    # Self-referential relationship for parent-child (e.g., Bank -> Branch)
    parent: Mapped[Optional["DfspProviderValue"]] = relationship(
        "DfspProviderValue",
        remote_side="DfspProviderValue.id",
        foreign_keys="DfspProviderValue.parent_id",
        back_populates="children"
    )
    children: Mapped[list["DfspProviderValue"]] = relationship(
        "DfspProviderValue",
        remote_side="DfspProviderValue.parent_id",
        foreign_keys="DfspProviderValue.parent_id",
        back_populates="parent"
    )

    @classmethod
    async def get_values_by_type(cls, provider_type: str, parent_id: Optional[int] = None):
        """
        Get provider values filtered by type and optional parent.
        
        Args:
            provider_type: The provider type (BANK, EMAIL_WALLET, MOBILE_WALLET)
            parent_id: Optional parent ID (for branches under a bank)
            
        Returns:
            List of DfspProviderValue objects
        """
        session = AsyncSession(dbengine.get())
        try:
            stmt = select(cls).where(cls.provider_type == provider_type)
            
            if parent_id is not None:
                stmt = stmt.where(cls.parent_id == parent_id)
            
            stmt = stmt.order_by(cls.name.asc())
            result = await session.execute(stmt)
            return list(result.scalars())
        finally:
            await session.aclose()

    @classmethod
    async def get_value_by_code(cls, code: str):
        """
        Get a provider value by code.
        
        Args:
            code: The provider value code
            
        Returns:
            DfspProviderValue object or None if not found
        """
        session = AsyncSession(dbengine.get())
        try:
            stmt = select(cls).where(cls.code == code)
            result = await session.execute(stmt)
            return result.scalars().first()
        finally:
            await session.aclose()

    @classmethod
    async def get_children(cls, parent_id: int):
        """
        Get direct children of a provider value (e.g., branches of a bank).
        
        Args:
            parent_id: Parent provider value ID
            
        Returns:
            List of child DfspProviderValue objects
        """
        return await cls.get_values_by_type(provider_type="BANK", parent_id=parent_id)

