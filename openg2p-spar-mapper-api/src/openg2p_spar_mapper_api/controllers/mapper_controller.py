import logging
from typing import Annotated

from fastapi import Depends
from openg2p_fastapi_common.controller import BaseController
from openg2p_fastapi_partner_auth.jwt_signature_validator import JWTSignatureValidator
from openg2p_spar_mapper_core.exceptions import (
    LinkValidationException,
    RequestValidationException,
    ResolveValidationException,
    UnlinkValidationException,
    UpdateValidationException,
)
from openg2p_spar_mapper_core.services import (
    MapperService,
    RequestValidation,
    ResponseHelper,
)
from openg2p_spar_models.schemas import (
    LinkRequest,
    LinkResponse,
    ResolveRequest,
    ResolveResponse,
    UnlinkRequest,
    UnlinkResponse,
    UpdateRequest,
    UpdateResponse,
)

from ..config import Settings

_config = Settings.get_config()
_logger = logging.getLogger(_config.logging_default_logger_name)


class MapperController(BaseController):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.router.tags += ["SPAR Mapper"]
        self.router.prefix = "/mapper"
        self.service = MapperService.get_component()

        self.router.add_api_route(
            "/link",
            self.link,
            responses={200: {"model": LinkResponse}},
            methods=["POST"],
        )
        self.router.add_api_route(
            "/resolve",
            self.resolve,
            responses={200: {"model": ResolveResponse}},
            methods=["POST"],
        )
        self.router.add_api_route(
            "/unlink",
            self.unlink,
            responses={200: {"model": UnlinkResponse}},
            methods=["POST"],
        )
        self.router.add_api_route(
            "/update",
            self.update,
            responses={200: {"model": UpdateResponse}},
            methods=["POST"],
        )

    async def link(
        self,
        link_request: LinkRequest,
        is_signature_valid: Annotated[bool, Depends(JWTSignatureValidator())],
    ) -> LinkResponse:
        """
        Link ID to Financial Address
        """
        try:
            RequestValidation.get_component().validate_signature(is_signature_valid)

            # Validate request structure
            RequestValidation.get_component().validate_request(link_request)

            # Process link request
            single_link_responses = await self.service.link(link_request)
            _logger.debug(f"Single Link Responses: {single_link_responses}")
            # Construct response
            link_response: LinkResponse = (
                ResponseHelper.get_component().construct_link_response(
                    link_request, single_link_responses
                )
            )
            return link_response

        except RequestValidationException as e:
            return ResponseHelper.get_component().construct_error_response(
                link_request, e, "rjct.request.validation", str(e)
            )
        except LinkValidationException as e:
            return ResponseHelper.get_component().construct_error_response(
                link_request, e, e.validation_error_type, e.message
            )
        except Exception as e:
            _logger.error(f"Internal server error during link operation: {str(e)}")
            return ResponseHelper.get_component().construct_error_response(
                link_request, e, "rjct.internal.error", "Internal server error"
            )

    async def resolve(
        self,
        resolve_request: ResolveRequest,
        is_signature_valid: Annotated[bool, Depends(JWTSignatureValidator())],
    ) -> ResolveResponse:
        """
        Resolve ID to Financial Address
        """
        try:
            RequestValidation.get_component().validate_signature(is_signature_valid)

            # Validate request structure
            RequestValidation.get_component().validate_request(resolve_request)

            # Process resolve request
            single_resolve_responses = await self.service.resolve(resolve_request)

            # Construct response
            resolve_response: ResolveResponse = (
                ResponseHelper.get_component().construct_resolve_response(
                    resolve_request, single_resolve_responses
                )
            )
            return resolve_response

        except RequestValidationException as e:
            return ResponseHelper.get_component().construct_error_response(
                resolve_request, e, "rjct.request.validation", str(e)
            )
        except ResolveValidationException as e:
            return ResponseHelper.get_component().construct_error_response(
                resolve_request, e, e.validation_error_type, e.message
            )
        except Exception as e:
            _logger.error(f"Internal server error during resolve operation: {str(e)}")
            return ResponseHelper.get_component().construct_error_response(
                resolve_request, e, "rjct.internal.error", "Internal server error"
            )

    async def unlink(
        self,
        unlink_request: UnlinkRequest,
        is_signature_valid: Annotated[bool, Depends(JWTSignatureValidator())],
    ) -> UnlinkResponse:
        """
        Unlink ID from Financial Address
        """
        try:
            RequestValidation.get_component().validate_signature(is_signature_valid)

            # Validate request structure
            RequestValidation.get_component().validate_request(unlink_request)

            # Process unlink request
            single_unlink_responses = await self.service.unlink(unlink_request)

            # Construct response
            unlink_response: UnlinkResponse = (
                ResponseHelper.get_component().construct_unlink_response(
                    unlink_request, single_unlink_responses
                )
            )
            return unlink_response

        except RequestValidationException as e:
            return ResponseHelper.get_component().construct_error_response(
                unlink_request, e, "rjct.request.validation", str(e)
            )
        except UnlinkValidationException as e:
            return ResponseHelper.get_component().construct_error_response(
                unlink_request, e, e.validation_error_type, e.message
            )
        except Exception as e:
            _logger.error(f"Internal server error during unlink operation: {str(e)}")
            return ResponseHelper.get_component().construct_error_response(
                unlink_request, e, "rjct.internal.error", "Internal server error"
            )

    async def update(
        self,
        update_request: UpdateRequest,
        is_signature_valid: Annotated[bool, Depends(JWTSignatureValidator())],
    ) -> UpdateResponse:
        """
        Update ID to Financial Address mapping
        """
        try:
            RequestValidation.get_component().validate_signature(is_signature_valid)

            # Validate request structure
            RequestValidation.get_component().validate_request(update_request)

            # Process update request
            single_update_responses = await self.service.update(update_request)

            # Construct response
            update_response: UpdateResponse = (
                ResponseHelper.get_component().construct_update_response(
                    update_request, single_update_responses
                )
            )
            return update_response

        except RequestValidationException as e:
            return ResponseHelper.get_component().construct_error_response(
                update_request, e, "rjct.request.validation", str(e)
            )
        except UpdateValidationException as e:
            return ResponseHelper.get_component().construct_error_response(
                update_request, e, e.validation_error_type, e.message
            )
        except Exception as e:
            _logger.error(f"Internal server error during update operation: {str(e)}")
            return ResponseHelper.get_component().construct_error_response(
                update_request, e, "rjct.internal.error", "Internal server error"
            )
