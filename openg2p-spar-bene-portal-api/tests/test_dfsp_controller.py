"""
Unit tests for DfspController
Tests DFSP provider API endpoints
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from openg2p_spar_bene_portal_api.controllers import DfspController
from openg2p_spar_models.schemas import (
    ProviderTypeEnum,
)


@pytest.mark.asyncio
@patch(
    "openg2p_spar_bene_portal_api.controllers.dfsp_controller.DfspService.get_component"
)
async def test_get_all_providers(mock_dfsp_service):
    """Test get all providers endpoint"""
    # Setup mock
    mock_service_instance = MagicMock()
    mock_service_instance.get_all_providers = AsyncMock()
    mock_dfsp_service.return_value = mock_service_instance

    # Create controller
    controller = DfspController()

    # Mock response
    mock_providers = [
        MagicMock(id=1, code="BANK", name="Bank", provider_type=ProviderTypeEnum.BANK),
        MagicMock(
            id=2,
            code="EMAIL_WALLET",
            name="Email Wallet",
            provider_type=ProviderTypeEnum.EMAIL_WALLET,
        ),
        MagicMock(
            id=3,
            code="MOBILE_WALLET",
            name="Mobile Wallet",
            provider_type=ProviderTypeEnum.MOBILE_WALLET,
        ),
    ]
    mock_service_instance.get_all_providers.return_value = mock_providers

    # Call endpoint
    result = await controller.get_all_providers()

    # Verify
    assert len(result) == 3
    assert result[0].code == "BANK"
    mock_service_instance.get_all_providers.assert_called_once()


@pytest.mark.asyncio
@patch(
    "openg2p_spar_bene_portal_api.controllers.dfsp_controller.DfspService.get_component"
)
async def test_get_provider_by_type(mock_dfsp_service):
    """Test get provider by type endpoint"""
    # Setup mock
    mock_service_instance = MagicMock()
    mock_service_instance.get_provider_by_type = AsyncMock()
    mock_dfsp_service.return_value = mock_service_instance

    # Create controller
    controller = DfspController()

    # Mock response
    mock_provider = MagicMock(
        id=1, code="BANK", name="Bank", provider_type=ProviderTypeEnum.BANK
    )
    mock_service_instance.get_provider_by_type.return_value = mock_provider

    # Call endpoint
    result = await controller.get_provider_by_type("BANK")

    # Verify
    assert result is not None
    assert result.code == "BANK"
    mock_service_instance.get_provider_by_type.assert_called_once_with("BANK")


@pytest.mark.asyncio
@patch(
    "openg2p_spar_bene_portal_api.controllers.dfsp_controller.DfspService.get_component"
)
async def test_get_provider_values(mock_dfsp_service):
    """Test get provider values endpoint"""
    # Setup mock
    mock_service_instance = MagicMock()
    mock_service_instance.get_provider_values = AsyncMock()
    mock_dfsp_service.return_value = mock_service_instance

    # Create controller
    controller = DfspController()

    # Mock response
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
    mock_service_instance.get_provider_values.return_value = mock_values

    # Call endpoint
    result = await controller.get_provider_values("BANK", parent_id=None)

    # Verify
    assert len(result) == 2
    assert result[0].code == "ICIC"
    mock_service_instance.get_provider_values.assert_called_once()


@pytest.mark.asyncio
@patch(
    "openg2p_spar_bene_portal_api.controllers.dfsp_controller.DfspService.get_component"
)
async def test_get_provider_values_with_parent(mock_dfsp_service):
    """Test get provider values with parent filter"""
    # Setup mock
    mock_service_instance = MagicMock()
    mock_service_instance.get_provider_values = AsyncMock()
    mock_dfsp_service.return_value = mock_service_instance

    # Create controller
    controller = DfspController()

    # Mock response - branches
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
    mock_service_instance.get_provider_values.return_value = mock_branches

    # Call endpoint
    result = await controller.get_provider_values("BANK", parent_id=1)

    # Verify
    assert len(result) == 2
    assert all(v.parent_id == 1 for v in result)


@pytest.mark.asyncio
@patch(
    "openg2p_spar_bene_portal_api.controllers.dfsp_controller.DfspService.get_component"
)
async def test_get_provider_value_by_code(mock_dfsp_service):
    """Test get provider value by code endpoint"""
    # Setup mock
    mock_service_instance = MagicMock()
    mock_service_instance.get_provider_value_by_code = AsyncMock()
    mock_dfsp_service.return_value = mock_service_instance

    # Create controller
    controller = DfspController()

    # Mock response
    mock_value = MagicMock(
        id=1,
        code="ICIC",
        name="ICICI Bank",
        provider_type=ProviderTypeEnum.BANK,
        parent_id=None,
    )
    mock_service_instance.get_provider_value_by_code.return_value = mock_value

    # Call endpoint
    result = await controller.get_provider_value_by_code("ICIC")

    # Verify
    assert result is not None
    assert result.code == "ICIC"
    mock_service_instance.get_provider_value_by_code.assert_called_once_with("ICIC")


@pytest.mark.asyncio
@patch(
    "openg2p_spar_bene_portal_api.controllers.dfsp_controller.DfspService.get_component"
)
async def test_get_children(mock_dfsp_service):
    """Test get children endpoint"""
    # Setup mock
    mock_service_instance = MagicMock()
    mock_service_instance.get_children = AsyncMock()
    mock_dfsp_service.return_value = mock_service_instance

    # Create controller
    controller = DfspController()

    # Mock response
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
    mock_service_instance.get_children.return_value = mock_children

    # Call endpoint
    result = await controller.get_children(1)

    # Verify
    assert len(result) == 2
    assert all(c.parent_id == 1 for c in result)
    mock_service_instance.get_children.assert_called_once_with(1)


@pytest.mark.asyncio
@patch(
    "openg2p_spar_bene_portal_api.controllers.dfsp_controller.DfspService.get_component"
)
async def test_get_children_empty(mock_dfsp_service):
    """Test get children when none exist"""
    # Setup mock
    mock_service_instance = MagicMock()
    mock_service_instance.get_children = AsyncMock()
    mock_dfsp_service.return_value = mock_service_instance

    # Create controller
    controller = DfspController()

    # Mock response - empty
    mock_service_instance.get_children.return_value = []

    # Call endpoint
    result = await controller.get_children(999)

    # Verify
    assert len(result) == 0
    mock_service_instance.get_children.assert_called_once_with(999)
