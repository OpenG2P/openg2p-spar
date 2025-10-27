from typing import List, Optional

from openg2p_fastapi_common.service import BaseService
from openg2p_spar_models.models import DfspProvider, DfspProviderValue
from openg2p_spar_models.schemas import (
    DfspProviderSchema,
    DfspProviderValueSchema,
)


class DfspService(BaseService):
    """
    Service for managing DFSP (Digital Financial Service Provider) data.

    Handles queries for provider types and their values (e.g., banks, branches, wallets).
    """

    async def get_all_providers(self) -> List[DfspProviderSchema]:
        """
        Get all provider types.

        Returns:
            List of DfspProviderSchema objects
        """
        providers = await DfspProvider.get_all_providers()
        return [DfspProviderSchema.model_validate(p.__dict__) for p in providers]

    async def get_provider_by_type(
        self, provider_type: str
    ) -> Optional[DfspProviderSchema]:
        """
        Get a provider by type.

        Args:
            provider_type: The provider type (BANK, EMAIL_WALLET, MOBILE_WALLET)

        Returns:
            DfspProviderSchema or None if not found
        """
        provider = await DfspProvider.get_provider_by_type(provider_type)
        if provider:
            return DfspProviderSchema.model_validate(provider.__dict__)
        return None

    async def get_provider_by_code(self, code: str) -> Optional[DfspProviderSchema]:
        """
        Get a provider by code.

        Args:
            code: The provider code

        Returns:
            DfspProviderSchema or None if not found
        """
        provider = await DfspProvider.get_provider_by_code(code)
        if provider:
            return DfspProviderSchema.model_validate(provider.__dict__)
        return None

    async def get_provider_values(
        self,
        provider_type: str,
        parent_id: Optional[int] = None,
    ) -> List[DfspProviderValueSchema]:
        """
        Get provider values filtered by type and optional parent.

        Args:
            provider_type: The provider type (BANK, EMAIL_WALLET, MOBILE_WALLET)
            parent_id: Optional parent ID (for branches under a bank)

        Returns:
            List of DfspProviderValueSchema objects
        """
        values = await DfspProviderValue.get_values_by_type(
            provider_type=provider_type, parent_id=parent_id
        )
        return [DfspProviderValueSchema.model_validate(v.__dict__) for v in values]

    async def get_provider_value_by_code(
        self, code: str
    ) -> Optional[DfspProviderValueSchema]:
        """
        Get a provider value by code.

        Args:
            code: The provider value code

        Returns:
            DfspProviderValueSchema or None if not found
        """
        value = await DfspProviderValue.get_value_by_code(code)
        if value:
            return DfspProviderValueSchema.model_validate(value.__dict__)
        return None

    async def get_children(self, parent_id: int) -> List[DfspProviderValueSchema]:
        """
        Get direct children of a provider value (e.g., branches of a bank).

        Args:
            parent_id: Parent provider value ID

        Returns:
            List of child DfspProviderValueSchema objects
        """
        children = await DfspProviderValue.get_children(parent_id)
        return [DfspProviderValueSchema.model_validate(c.__dict__) for c in children]

    async def get_root_providers(
        self, provider_type: str
    ) -> List[DfspProviderValueSchema]:
        """
        Get root-level provider values (those without a parent).

        Args:
            provider_type: The provider type (BANK, EMAIL_WALLET, MOBILE_WALLET)

        Returns:
            List of root DfspProviderValueSchema objects
        """
        return await self.get_provider_values(
            provider_type=provider_type, parent_id=None
        )
