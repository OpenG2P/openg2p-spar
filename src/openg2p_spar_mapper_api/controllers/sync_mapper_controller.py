from typing import Annotated

from fastapi import Depends
from openg2p_fastapi_common.controller import BaseController
from openg2p_g2pconnect_common_lib.jwt_signature_validator import JWTSignatureValidator
from openg2p_g2pconnect_mapper_lib.schemas import (
    LinkRequest,
    LinkResponse,
    ResolveRequest,
    ResolveResponse,
    SingleLinkResponse,
    SingleResolveResponse,
    SingleUpdateResponse,
    UnlinkRequest,
    UnlinkResponse,
    UpdateRequest,
    UpdateResponse,
)

from ..services import (
    MapperService,
    RequestValidation,
    RequestValidationException,
    SyncResponseHelper,
)


class SyncMapperController(BaseController):
    mapper_service: MapperService = MapperService.get_cached_component()
    request_validation: RequestValidation = RequestValidation.get_cached_component()
    sync_response_helper: SyncResponseHelper = SyncResponseHelper.get_cached_component()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.router.prefix += "/sync"
        self.router.tags += ["G2PConnect Mapper Sync"]

        self.router.add_api_route(
            "/link",
            self.link_sync,
            responses={200: {"model": LinkResponse}},
            methods=["POST"],
        )
        self.router.add_api_route(
            "/update",
            self.update_sync,
            responses={200: {"model": UpdateResponse}},
            methods=["POST"],
        )
        self.router.add_api_route(
            "/resolve",
            self.resolve_sync,
            responses={200: {"model": ResolveResponse}},
            methods=["POST"],
        )
        self.router.add_api_route(
            "/unlink",
            self.unlink_sync,
            responses={200: {"model": UnlinkResponse}},
            methods=["POST"],
        )

    async def link_sync(
        self,
        link_request: LinkRequest,
        is_signature_valid: Annotated[bool, Depends(JWTSignatureValidator())],
    ):
        try:
            self.request_validation.validate_signature(is_signature_valid)
            self.request_validation.validate_request(link_request)
            self.request_validation.validate_link_request_header(link_request)
        except RequestValidationException as e:
            error_response = self.sync_response_helper.construct_error_sync_response(link_request, e)
            return error_response

        single_link_responses: list[SingleLinkResponse] = await self.mapper_service.link(link_request)
        return self.sync_response_helper.construct_success_sync_link_response(
            link_request,
            single_link_responses,
        )

    async def update_sync(
        self,
        update_request: UpdateRequest,
        is_signature_valid: Annotated[bool, Depends(JWTSignatureValidator())],
    ):
        try:
            self.request_validation.validate_signature(is_signature_valid)
            self.request_validation.validate_request(update_request)
            self.request_validation.validate_update_request_header(update_request)
        except RequestValidationException as e:
            error_response = self.sync_response_helper.construct_error_sync_response(update_request, e)
            return error_response

        single_update_responses: list[SingleUpdateResponse] = await self.mapper_service.update(update_request)
        return self.sync_response_helper.construct_success_sync_update_response(
            update_request,
            single_update_responses,
        )

    async def resolve_sync(
        self,
        resolve_request: ResolveRequest,
        is_signature_valid: Annotated[bool, Depends(JWTSignatureValidator())],
    ):
        try:
            self.request_validation.validate_signature(is_signature_valid)
            self.request_validation.validate_request(resolve_request)
            self.request_validation.validate_resolve_request_header(resolve_request)
        except RequestValidationException as e:
            error_response = self.sync_response_helper.construct_error_sync_response(resolve_request, e)
            return error_response

        single_resolve_responses: list[SingleResolveResponse] = await self.mapper_service.resolve(
            resolve_request
        )
        return self.sync_response_helper.construct_success_sync_resolve_response(
            resolve_request,
            single_resolve_responses,
        )

    async def unlink_sync(
        self,
        unlink_request: UnlinkRequest,
        is_signature_valid: Annotated[bool, Depends(JWTSignatureValidator())],
    ):
        try:
            self.request_validation.validate_signature(is_signature_valid)
            self.request_validation.validate_request(unlink_request)
            self.request_validation.validate_unlink_request_header(unlink_request)
        except RequestValidationException as e:
            error_response = self.sync_response_helper.construct_error_sync_response(unlink_request, e)
            return error_response

        single_unlink_responses: list[SingleResolveResponse] = await self.mapper_service.unlink(
            unlink_request
        )
        return self.sync_response_helper.construct_success_sync_unlink_response(
            unlink_request,
            single_unlink_responses,
        )
