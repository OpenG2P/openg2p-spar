"""
Unit tests for DfspService
Tests DFSP provider management operations
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from openg2p_spar_mapper_core.services import DfspService
from openg2p_spar_models.schemas import (
    ProviderTypeEnum,
)


@pytest.mark.asyncio
async def test_get_all_providers():
    """Test getting all provider types"""
    service = DfspService()

    mock_providers = [
        MagicMock(
            id=1,
            code="BANK",
            name="Bank",
            provider_type=ProviderTypeEnum.BANK,
            description="Bank provider",
        ),
        MagicMock(
            id=2,
            code="EMAIL_WALLET",
            name="Email Wallet",
            provider_type=ProviderTypeEnum.EMAIL_WALLET,
            description="Email wallet provider",
        ),
        MagicMock(
            id=3,
            code="MOBILE_WALLET",
            name="Mobile Wallet",
            provider_type=ProviderTypeEnum.MOBILE_WALLET,
            description="Mobile wallet provider",
        ),
    ]

    with patch.object(service, "get_all_providers", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = mock_providers

        result = await service.get_all_providers()
        assert len(result) == 3
        assert result[0].code == "BANK"


@pytest.mark.asyncio
async def test_get_provider_by_type():
    """Test getting provider by type"""
    service = DfspService()

    mock_provider = MagicMock(
        id=1,
        code="BANK",
        name="Bank",
        provider_type=ProviderTypeEnum.BANK,
        description="Bank provider",
    )

    with patch.object(
        service, "get_provider_by_type", new_callable=AsyncMock
    ) as mock_get:
        mock_get.return_value = mock_provider

        result = await service.get_provider_by_type("BANK")
        assert result is not None
        assert result.code == "BANK"


@pytest.mark.asyncio
async def test_get_provider_by_type_not_found():
    """Test getting provider by type when not found"""
    service = DfspService()

    with patch.object(
        service, "get_provider_by_type", new_callable=AsyncMock
    ) as mock_get:
        mock_get.return_value = None

        result = await service.get_provider_by_type("INVALID")
        assert result is None


@pytest.mark.asyncio
async def test_get_provider_values():
    """Test getting provider values by type"""
    service = DfspService()

    mock_values = [
        MagicMock(
            id=1,
            code="ICIC",
            name="ICICI Bank",
            provider_type=ProviderTypeEnum.BANK,
            parent_id=None,
        ),
        MagicMock(
            id=2,
            code="HDFC",
            name="HDFC Bank",
            provider_type=ProviderTypeEnum.BANK,
            parent_id=None,
        ),
    ]

    with patch.object(
        service, "get_provider_values", new_callable=AsyncMock
    ) as mock_get:
        mock_get.return_value = mock_values

        result = await service.get_provider_values("BANK")
        assert len(result) == 2
        assert result[0].code == "ICIC"


@pytest.mark.asyncio
async def test_get_provider_values_with_parent():
    """Test getting provider values filtered by parent"""
    service = DfspService()

    mock_branches = [
        MagicMock(
            id=3,
            code="ICIC_DEL",
            name="ICICI Delhi Branch",
            provider_type=ProviderTypeEnum.BANK,
            parent_id=1,
        ),
        MagicMock(
            id=4,
            code="ICIC_MUM",
            name="ICICI Mumbai Branch",
            provider_type=ProviderTypeEnum.BANK,
            parent_id=1,
        ),
    ]

    with patch.object(
        service, "get_provider_values", new_callable=AsyncMock
    ) as mock_get:
        mock_get.return_value = mock_branches

        result = await service.get_provider_values("BANK", parent_id=1)
        assert len(result) == 2
        assert all(v.parent_id == 1 for v in result)


@pytest.mark.asyncio
async def test_get_provider_value_by_code():
    """Test getting provider value by code"""
    service = DfspService()

    mock_value = MagicMock(
        id=1,
        code="ICIC",
        name="ICICI Bank",
        provider_type=ProviderTypeEnum.BANK,
        parent_id=None,
    )

    with patch.object(
        service, "get_provider_value_by_code", new_callable=AsyncMock
    ) as mock_get:
        mock_get.return_value = mock_value

        result = await service.get_provider_value_by_code("ICIC")
        assert result is not None
        assert result.code == "ICIC"


@pytest.mark.asyncio
async def test_get_provider_value_by_code_not_found():
    """Test getting provider value by code when not found"""
    service = DfspService()

    with patch.object(
        service, "get_provider_value_by_code", new_callable=AsyncMock
    ) as mock_get:
        mock_get.return_value = None

        result = await service.get_provider_value_by_code("INVALID")
        assert result is None


@pytest.mark.asyncio
async def test_get_children():
    """Test getting children of a provider value"""
    service = DfspService()

    mock_children = [
        MagicMock(
            id=3,
            code="ICIC_DEL",
            name="ICICI Delhi Branch",
            provider_type=ProviderTypeEnum.BANK,
            parent_id=1,
        ),
        MagicMock(
            id=4,
            code="ICIC_MUM",
            name="ICICI Mumbai Branch",
            provider_type=ProviderTypeEnum.BANK,
            parent_id=1,
        ),
    ]

    with patch.object(service, "get_children", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = mock_children

        result = await service.get_children(1)
        assert len(result) == 2
        assert all(c.parent_id == 1 for c in result)


@pytest.mark.asyncio
async def test_get_children_empty():
    """Test getting children when none exist"""
    service = DfspService()

    with patch.object(service, "get_children", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = []

        result = await service.get_children(999)
        assert len(result) == 0


@pytest.mark.asyncio
async def test_provider_hierarchy():
    """Test provider hierarchy (BANK -> BRANCH)"""
    service = DfspService()

    # Mock bank
    mock_bank = MagicMock(
        id=1,
        code="ICIC",
        name="ICICI Bank",
        provider_type=ProviderTypeEnum.BANK,
        parent_id=None,
    )

    # Mock branches
    mock_branches = [
        MagicMock(
            id=3,
            code="ICIC_DEL",
            name="ICICI Delhi Branch",
            provider_type=ProviderTypeEnum.BANK,
            parent_id=1,
        ),
        MagicMock(
            id=4,
            code="ICIC_MUM",
            name="ICICI Mumbai Branch",
            provider_type=ProviderTypeEnum.BANK,
            parent_id=1,
        ),
    ]

    with patch.object(
        service, "get_provider_value_by_code", new_callable=AsyncMock
    ) as mock_get_code:
        with patch.object(
            service, "get_children", new_callable=AsyncMock
        ) as mock_get_children:
            mock_get_code.return_value = mock_bank
            mock_get_children.return_value = mock_branches

            # Get bank
            bank = await service.get_provider_value_by_code("ICIC")
            assert bank.id == 1

            # Get branches
            branches = await service.get_children(bank.id)
            assert len(branches) == 2
            assert all(b.parent_id == bank.id for b in branches)
