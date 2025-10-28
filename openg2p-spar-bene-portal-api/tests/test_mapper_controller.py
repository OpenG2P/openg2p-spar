"""
Unit tests for MapperController
Tests API endpoints for Link, Resolve, Update, and Unlink operations
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from openg2p_fastapi_auth_models.schemas import AuthCredentials
from openg2p_spar_bene_portal_api.controllers import MapperController
from openg2p_spar_models.schemas import StatusEnum


@pytest.mark.asyncio
async def test_link_endpoint():
    """Test link API endpoint with ID construction from auth credentials"""
    controller = MapperController()

    # Create mock auth credentials
    mock_auth = MagicMock(spec=AuthCredentials)
    mock_auth.iss = "test_issuer"
    mock_auth.sub = "test_subject"
    mock_auth.model_dump.return_value = {"iss": "test_issuer", "sub": "test_subject"}

    # Create mock request with link_request items
    mock_request = MagicMock()
    mock_single_link_request = MagicMock()
    mock_single_link_request.id = "original_id"
    mock_single_link_request.fa = "test_fa"
    mock_request.request_body.request_payload.link_request = [mock_single_link_request]

    # Mock the service and helper methods
    with patch.object(controller.service, "link", new_callable=AsyncMock) as mock_service_link, \
         patch("openg2p_spar_bene_portal_api.controllers.mapper_controller.RequestValidation") as mock_validation, \
         patch("openg2p_spar_bene_portal_api.controllers.mapper_controller.StrategyHelper") as mock_strategy_helper, \
         patch("openg2p_spar_bene_portal_api.controllers.mapper_controller.ResponseHelper") as mock_response_helper:

        # Setup mocks
        mock_validation.get_component.return_value.validate_request.return_value = None
        mock_strategy_helper_instance = MagicMock()
        mock_strategy_helper_instance.construct_id = AsyncMock(return_value="constructed_id_123")
        mock_strategy_helper.return_value.get_component.return_value = mock_strategy_helper_instance

        mock_response = MagicMock()
        mock_response_helper.get_component.return_value.construct_link_response.return_value = mock_response
        mock_service_link.return_value = [MagicMock(reference_id="ref123", status=StatusEnum.succ)]

        # Call the endpoint
        result = await controller.link(mock_request, mock_auth)

        # Verify ID was replaced with constructed ID
        assert mock_single_link_request.id == "constructed_id_123"
        assert result is not None
        mock_service_link.assert_called_once()


@pytest.mark.asyncio
async def test_resolve_endpoint():
    """Test resolve API endpoint with ID construction from auth credentials"""
    controller = MapperController()

    # Create mock auth credentials
    mock_auth = MagicMock(spec=AuthCredentials)
    mock_auth.iss = "test_issuer"
    mock_auth.sub = "test_subject"
    mock_auth.model_dump.return_value = {"iss": "test_issuer", "sub": "test_subject"}

    # Create mock request with resolve_request items
    mock_request = MagicMock()
    mock_single_resolve_request = MagicMock()
    mock_single_resolve_request.id = ""  # Empty ID should be replaced
    mock_single_resolve_request.fa = "test_fa"
    mock_request.request_body.request_payload.resolve_request = [mock_single_resolve_request]

    # Mock the service and helper methods
    with patch.object(controller.service, "resolve", new_callable=AsyncMock) as mock_service_resolve, \
         patch("openg2p_spar_bene_portal_api.controllers.mapper_controller.RequestValidation") as mock_validation, \
         patch("openg2p_spar_bene_portal_api.controllers.mapper_controller.StrategyHelper") as mock_strategy_helper, \
         patch("openg2p_spar_bene_portal_api.controllers.mapper_controller.ResponseHelper") as mock_response_helper:

        # Setup mocks
        mock_validation.get_component.return_value.validate_request.return_value = None
        mock_strategy_helper_instance = MagicMock()
        mock_strategy_helper_instance.construct_id = AsyncMock(return_value="constructed_id_456")
        mock_strategy_helper.return_value.get_component.return_value = mock_strategy_helper_instance

        mock_response = MagicMock()
        mock_response_helper.get_component.return_value.construct_resolve_response.return_value = mock_response
        mock_service_resolve.return_value = [MagicMock(reference_id="ref123", fa="FA456", status=StatusEnum.succ)]

        # Call the endpoint
        result = await controller.resolve(mock_request, mock_auth)

        # Verify ID was replaced with constructed ID
        assert mock_single_resolve_request.id == "constructed_id_456"
        assert result is not None
        mock_service_resolve.assert_called_once()


@pytest.mark.asyncio
async def test_update_endpoint():
    """Test update API endpoint with ID construction from auth credentials"""
    controller = MapperController()

    # Create mock auth credentials
    mock_auth = MagicMock(spec=AuthCredentials)
    mock_auth.iss = "test_issuer"
    mock_auth.sub = "test_subject"
    mock_auth.model_dump.return_value = {"iss": "test_issuer", "sub": "test_subject"}

    # Create mock request with update_request items
    mock_request = MagicMock()
    mock_single_update_request = MagicMock()
    mock_single_update_request.id = "original_id"
    mock_single_update_request.fa = "test_fa"
    mock_request.request_body.request_payload.update_request = [mock_single_update_request]

    # Mock the service and helper methods
    with patch.object(controller.service, "update", new_callable=AsyncMock) as mock_service_update, \
         patch("openg2p_spar_bene_portal_api.controllers.mapper_controller.RequestValidation") as mock_validation, \
         patch("openg2p_spar_bene_portal_api.controllers.mapper_controller.StrategyHelper") as mock_strategy_helper, \
         patch("openg2p_spar_bene_portal_api.controllers.mapper_controller.ResponseHelper") as mock_response_helper:

        # Setup mocks
        mock_validation.get_component.return_value.validate_request.return_value = None
        mock_strategy_helper_instance = MagicMock()
        mock_strategy_helper_instance.construct_id = AsyncMock(return_value="constructed_id_789")
        mock_strategy_helper.return_value.get_component.return_value = mock_strategy_helper_instance

        mock_response = MagicMock()
        mock_response_helper.get_component.return_value.construct_update_response.return_value = mock_response
        mock_service_update.return_value = [MagicMock(reference_id="ref123", status=StatusEnum.succ)]

        # Call the endpoint
        result = await controller.update(mock_request, mock_auth)

        # Verify ID was replaced with constructed ID
        assert mock_single_update_request.id == "constructed_id_789"
        assert result is not None
        mock_service_update.assert_called_once()


@pytest.mark.asyncio
async def test_unlink_endpoint():
    """Test unlink API endpoint with ID construction from auth credentials"""
    controller = MapperController()

    # Create mock auth credentials
    mock_auth = MagicMock(spec=AuthCredentials)
    mock_auth.iss = "test_issuer"
    mock_auth.sub = "test_subject"
    mock_auth.model_dump.return_value = {"iss": "test_issuer", "sub": "test_subject"}

    # Create mock request with unlink_request items
    mock_request = MagicMock()
    mock_single_unlink_request = MagicMock()
    mock_single_unlink_request.id = "original_id"
    mock_single_unlink_request.fa = "test_fa"
    mock_request.request_body.request_payload.unlink_request = [mock_single_unlink_request]

    # Mock the service and helper methods
    with patch.object(controller.service, "unlink", new_callable=AsyncMock) as mock_service_unlink, \
         patch("openg2p_spar_bene_portal_api.controllers.mapper_controller.RequestValidation") as mock_validation, \
         patch("openg2p_spar_bene_portal_api.controllers.mapper_controller.StrategyHelper") as mock_strategy_helper, \
         patch("openg2p_spar_bene_portal_api.controllers.mapper_controller.ResponseHelper") as mock_response_helper:

        # Setup mocks
        mock_validation.get_component.return_value.validate_request.return_value = None
        mock_strategy_helper_instance = MagicMock()
        mock_strategy_helper_instance.construct_id = AsyncMock(return_value="constructed_id_101")
        mock_strategy_helper.return_value.get_component.return_value = mock_strategy_helper_instance

        mock_response = MagicMock()
        mock_response_helper.get_component.return_value.construct_unlink_response.return_value = mock_response
        mock_service_unlink.return_value = [MagicMock(reference_id="ref123", status=StatusEnum.succ)]

        # Call the endpoint
        result = await controller.unlink(mock_request, mock_auth)

        # Verify ID was replaced with constructed ID
        assert mock_single_unlink_request.id == "constructed_id_101"
        assert result is not None
        mock_service_unlink.assert_called_once()


@pytest.mark.asyncio
async def test_link_error_handling():
    """Test link endpoint error handling when StrategyHelper fails"""
    controller = MapperController()

    # Create mock auth credentials
    mock_auth = MagicMock(spec=AuthCredentials)
    mock_auth.iss = "test_issuer"
    mock_auth.model_dump.return_value = {"iss": "test_issuer"}

    # Create mock request
    mock_request = MagicMock()
    mock_request.request_body.request_payload.link_request = []

    # Mock the service and helper methods
    with patch("openg2p_spar_bene_portal_api.controllers.mapper_controller.RequestValidation") as mock_validation, \
         patch("openg2p_spar_bene_portal_api.controllers.mapper_controller.StrategyHelper") as mock_strategy_helper, \
         patch("openg2p_spar_bene_portal_api.controllers.mapper_controller.ResponseHelper") as mock_response_helper:

        # Setup mocks
        mock_validation.get_component.return_value.validate_request.return_value = None
        mock_strategy_helper_instance = MagicMock()
        mock_strategy_helper_instance.construct_id = AsyncMock(side_effect=RuntimeError("Service error"))
        mock_strategy_helper.return_value.get_component.return_value = mock_strategy_helper_instance

        mock_response_helper.get_component.return_value.construct_error_response.return_value = MagicMock()

        # Call the endpoint - should handle error gracefully
        result = await controller.link(mock_request, mock_auth)
        assert result is not None


@pytest.mark.asyncio
async def test_resolve_error_handling():
    """Test resolve endpoint error handling when StrategyHelper fails"""
    controller = MapperController()

    # Create mock auth credentials
    mock_auth = MagicMock(spec=AuthCredentials)
    mock_auth.iss = "test_issuer"
    mock_auth.model_dump.return_value = {"iss": "test_issuer"}

    # Create mock request
    mock_request = MagicMock()
    mock_request.request_body.request_payload.resolve_request = []

    # Mock the service and helper methods
    with patch("openg2p_spar_bene_portal_api.controllers.mapper_controller.RequestValidation") as mock_validation, \
         patch("openg2p_spar_bene_portal_api.controllers.mapper_controller.StrategyHelper") as mock_strategy_helper, \
         patch("openg2p_spar_bene_portal_api.controllers.mapper_controller.ResponseHelper") as mock_response_helper:

        # Setup mocks
        mock_validation.get_component.return_value.validate_request.return_value = None
        mock_strategy_helper_instance = MagicMock()
        mock_strategy_helper_instance.construct_id = AsyncMock(side_effect=RuntimeError("Service error"))
        mock_strategy_helper.return_value.get_component.return_value = mock_strategy_helper_instance

        mock_response_helper.get_component.return_value.construct_error_response.return_value = MagicMock()

        # Call the endpoint - should handle error gracefully
        result = await controller.resolve(mock_request, mock_auth)
        assert result is not None


@pytest.mark.asyncio
async def test_controller_initialization():
    """Test MapperController initialization"""
    controller = MapperController()
    assert controller is not None
    assert hasattr(controller, "link")
    assert hasattr(controller, "resolve")
    assert hasattr(controller, "update")
    assert hasattr(controller, "unlink")
