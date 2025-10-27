import logging
from typing import List, Optional

from fastapi import Query
from openg2p_fastapi_common.controller import BaseController
from openg2p_spar_mapper_core.services import DfspService
from openg2p_spar_models.schemas import (
    DfspProviderSchema,
    DfspProviderValueSchema,
    ProviderTypeEnum,
)
from ..config import Settings

_config = Settings.get_config()
_logger = logging.getLogger(_config.logging_default_logger_name)


class DfspController(BaseController):
    """
    Controller for DFSP (Digital Financial Service Provider) endpoints.
    
    Provides API endpoints for querying provider types and their values.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.router.tags += ["DFSP"]
        self.router.prefix = "/dfsp"
        self.service = DfspService.get_component()

        # Provider endpoints
        self.router.add_api_route(
            "/providers",
            self.get_all_providers,
            responses={200: {"model": List[DfspProviderSchema]}},
            methods=["GET"],
            summary="Get all provider types",
            description="Returns all available provider types (BANK, EMAIL_WALLET, MOBILE_WALLET)",
        )

        self.router.add_api_route(
            "/providers/{provider_type}",
            self.get_provider_by_type,
            responses={200: {"model": DfspProviderSchema}},
            methods=["GET"],
            summary="Get provider by type",
            description="Returns a specific provider type configuration",
        )

        # Provider values endpoints
        self.router.add_api_route(
            "/providers/{provider_type}/values",
            self.get_provider_values,
            responses={200: {"model": List[DfspProviderValueSchema]}},
            methods=["GET"],
            summary="Get provider values",
            description="Returns provider values (e.g., banks, branches, wallets) filtered by type and optional parent",
        )

        self.router.add_api_route(
            "/values/{code}",
            self.get_provider_value_by_code,
            responses={200: {"model": DfspProviderValueSchema}},
            methods=["GET"],
            summary="Get provider value by code",
            description="Returns a specific provider value by its code",
        )

        self.router.add_api_route(
            "/values/{parent_id}/children",
            self.get_children,
            responses={200: {"model": List[DfspProviderValueSchema]}},
            methods=["GET"],
            summary="Get children of a provider value",
            description="Returns direct children of a provider value (e.g., branches of a bank)",
        )

    async def get_all_providers(self) -> List[DfspProviderSchema]:
        """
        Get all provider types.
        
        Returns:
            List of all provider types
        """
        try:
            _logger.debug("Fetching all provider types")
            providers = await self.service.get_all_providers()
            _logger.debug(f"Found {len(providers)} provider types")
            return providers
        except Exception as e:
            _logger.error(f"Error fetching providers: {str(e)}")
            raise

    async def get_provider_by_type(self, provider_type: str) -> DfspProviderSchema:
        """
        Get a provider by type.
        
        Args:
            provider_type: The provider type (BANK, EMAIL_WALLET, MOBILE_WALLET)
            
        Returns:
            DfspProviderSchema for the requested type
        """
        try:
            _logger.debug(f"Fetching provider type: {provider_type}")
            provider = await self.service.get_provider_by_type(provider_type)
            if not provider:
                _logger.warning(f"Provider type not found: {provider_type}")
                return {"error": f"Provider type '{provider_type}' not found"}
            return provider
        except Exception as e:
            _logger.error(f"Error fetching provider type {provider_type}: {str(e)}")
            raise

    async def get_provider_values(
        self,
        provider_type: str,
        parent_id: Optional[int] = Query(None, description="Optional parent ID for filtering"),
    ) -> List[DfspProviderValueSchema]:
        """
        Get provider values filtered by type and optional parent.
        
        Args:
            provider_type: The provider type (BANK, EMAIL_WALLET, MOBILE_WALLET)
            parent_id: Optional parent ID (for branches under a bank)
            
        Returns:
            List of provider values matching the criteria
        """
        try:
            _logger.debug(
                f"Fetching provider values for type: {provider_type}, parent_id: {parent_id}"
            )
            values = await self.service.get_provider_values(
                provider_type=provider_type, parent_id=parent_id
            )
            _logger.debug(f"Found {len(values)} provider values")
            return values
        except Exception as e:
            _logger.error(
                f"Error fetching provider values for {provider_type}: {str(e)}"
            )
            raise

    async def get_provider_value_by_code(self, code: str) -> DfspProviderValueSchema:
        """
        Get a provider value by code.
        
        Args:
            code: The provider value code
            
        Returns:
            DfspProviderValueSchema for the requested code
        """
        try:
            _logger.debug(f"Fetching provider value by code: {code}")
            value = await self.service.get_provider_value_by_code(code)
            if not value:
                _logger.warning(f"Provider value not found: {code}")
                return {"error": f"Provider value '{code}' not found"}
            return value
        except Exception as e:
            _logger.error(f"Error fetching provider value {code}: {str(e)}")
            raise

    async def get_children(self, parent_id: int) -> List[DfspProviderValueSchema]:
        """
        Get direct children of a provider value.
        
        Args:
            parent_id: Parent provider value ID
            
        Returns:
            List of child provider values
        """
        try:
            _logger.debug(f"Fetching children for parent_id: {parent_id}")
            children = await self.service.get_children(parent_id)
            _logger.debug(f"Found {len(children)} children")
            return children
        except Exception as e:
            _logger.error(f"Error fetching children for {parent_id}: {str(e)}")
            raise

