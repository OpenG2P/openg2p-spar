"""
Unit tests for MapperController
Tests API endpoints for Link, Resolve, Update, and Unlink operations
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from openg2p_spar_bene_portal_api.controllers import MapperController
from openg2p_spar_models.schemas import StatusEnum


@pytest.mark.asyncio
async def test_link_endpoint():
    """Test link API endpoint"""
    controller = MapperController()

    with patch.object(controller, "link", new_callable=AsyncMock) as mock_link:
        mock_response = MagicMock()
        mock_response.response_body.response_payload.link_response = [
            MagicMock(reference_id="ref123", status=StatusEnum.succ)
        ]
        mock_link.return_value = mock_response

        mock_request = MagicMock()
        result = await controller.link(mock_request)

        assert result is not None
        mock_link.assert_called_once()


@pytest.mark.asyncio
async def test_resolve_endpoint():
    """Test resolve API endpoint"""
    controller = MapperController()

    with patch.object(controller, "resolve", new_callable=AsyncMock) as mock_resolve:
        mock_response = MagicMock()
        mock_response.response_body.response_payload.resolve_response = [
            MagicMock(reference_id="ref123", fa="FA456", status=StatusEnum.succ)
        ]
        mock_resolve.return_value = mock_response

        mock_request = MagicMock()
        result = await controller.resolve(mock_request)

        assert result is not None
        mock_resolve.assert_called_once()


@pytest.mark.asyncio
async def test_update_endpoint():
    """Test update API endpoint"""
    controller = MapperController()

    with patch.object(controller, "update", new_callable=AsyncMock) as mock_update:
        mock_response = MagicMock()
        mock_response.response_body.response_payload.update_response = [
            MagicMock(reference_id="ref123", status=StatusEnum.succ)
        ]
        mock_update.return_value = mock_response

        mock_request = MagicMock()
        result = await controller.update(mock_request)

        assert result is not None
        mock_update.assert_called_once()


@pytest.mark.asyncio
async def test_unlink_endpoint():
    """Test unlink API endpoint"""
    controller = MapperController()

    with patch.object(controller, "unlink", new_callable=AsyncMock) as mock_unlink:
        mock_response = MagicMock()
        mock_response.response_body.response_payload.unlink_response = [
            MagicMock(reference_id="ref123", status=StatusEnum.succ)
        ]
        mock_unlink.return_value = mock_response

        mock_request = MagicMock()
        result = await controller.unlink(mock_request)

        assert result is not None
        mock_unlink.assert_called_once()


@pytest.mark.asyncio
async def test_link_error_handling():
    """Test link endpoint error handling"""
    controller = MapperController()

    with patch.object(controller, "link", new_callable=AsyncMock) as mock_link:
        mock_link.side_effect = RuntimeError("Service error")

        mock_request = MagicMock()

        with pytest.raises(RuntimeError):
            await controller.link(mock_request)


@pytest.mark.asyncio
async def test_resolve_error_handling():
    """Test resolve endpoint error handling"""
    controller = MapperController()

    with patch.object(controller, "resolve", new_callable=AsyncMock) as mock_resolve:
        mock_resolve.side_effect = RuntimeError("Service error")

        mock_request = MagicMock()

        with pytest.raises(RuntimeError):
            await controller.resolve(mock_request)


@pytest.mark.asyncio
async def test_controller_initialization():
    """Test MapperController initialization"""
    controller = MapperController()
    assert controller is not None
    assert hasattr(controller, "link")
    assert hasattr(controller, "resolve")
    assert hasattr(controller, "update")
    assert hasattr(controller, "unlink")
