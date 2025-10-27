from datetime import datetime
from openg2p_spar_models.schemas import (
    LinkRequest, LinkResponse, SingleLinkResponse, StatusEnum,
    LinkResponsePayload, LinkResponseBody,
    UpdateRequest, UpdateResponse, SingleUpdateResponse,
    UpdateResponsePayload, UpdateResponseBody,
    ResolveRequest, ResolveResponse, SingleResolveResponse,
    ResolveResponsePayload, ResolveResponseBody,
    UnlinkRequest, UnlinkResponse, SingleUnlinkResponse,
    UnlinkResponsePayload, UnlinkResponseBody
)
from ..exceptions import RequestValidationException
from openg2p_fastapi_common.service import BaseService
from openg2p_fastapi_common.schemas import (
    G2PResponse, G2PResponseHeader, G2PResponseBody, G2PResponseStatus
)

class ResponseHelper(BaseService):
    @staticmethod
    def construct_link_response(
        link_request: LinkRequest,
        single_link_responses: list[SingleLinkResponse],
    ) -> LinkResponse:
        link_request_payload = link_request.request_body.request_payload
        link_response_payload = LinkResponsePayload(
            transaction_id=link_request_payload.transaction_id,
            correlation_id=None,
            link_response=single_link_responses,
        )
        link_response_body = LinkResponseBody(response_payload=link_response_payload)

        # Create response header
        response_header = G2PResponseHeader(
            request_id=link_request.request_header.request_id,
            response_status=G2PResponseStatus.SUCCESS,
            response_error_code=None,
            response_error_message=None,
            response_timestamp=datetime.now()
        )

        return LinkResponse(
            response_header=response_header,
            response_body=link_response_body
        )

    @staticmethod
    def construct_update_response(
        update_request: UpdateRequest,
        single_update_responses: list[SingleUpdateResponse],
    ) -> UpdateResponse:
        update_request_payload = update_request.request_body.request_payload
        update_response_payload = UpdateResponsePayload(
            transaction_id=update_request_payload.transaction_id,
            correlation_id=None,
            update_response=single_update_responses,
        )
        update_response_body = UpdateResponseBody(response_payload=update_response_payload)

        # Create response header
        response_header = G2PResponseHeader(
            request_id=update_request.request_header.request_id,
            response_status=G2PResponseStatus.SUCCESS,
            response_error_code=None,
            response_error_message=None,
            response_timestamp=datetime.now()
        )

        return UpdateResponse(
            response_header=response_header,
            response_body=update_response_body
        )

    @staticmethod
    def construct_resolve_response(
        resolve_request: ResolveRequest,
        single_resolve_responses: list[SingleResolveResponse],
    ) -> ResolveResponse:
        resolve_request_payload = resolve_request.request_body.request_payload
        resolve_response_payload = ResolveResponsePayload(
            transaction_id=resolve_request_payload.transaction_id,
            correlation_id=None,
            resolve_response=single_resolve_responses,
        )
        resolve_response_body = ResolveResponseBody(response_payload=resolve_response_payload)

        # Create response header
        response_header = G2PResponseHeader(
            request_id=resolve_request.request_header.request_id,
            response_status=G2PResponseStatus.SUCCESS,
            response_error_code=None,
            response_error_message=None,
            response_timestamp=datetime.now()
        )

        return ResolveResponse(
            response_header=response_header,
            response_body=resolve_response_body
        )

    @staticmethod
    def construct_unlink_response(
        unlink_request: UnlinkRequest,
        single_unlink_responses: list[SingleUnlinkResponse],
    ) -> UnlinkResponse:
        unlink_request_payload = unlink_request.request_body.request_payload
        unlink_response_payload = UnlinkResponsePayload(
            transaction_id=unlink_request_payload.transaction_id,
            correlation_id=None,
            unlink_response=single_unlink_responses,
        )
        unlink_response_body = UnlinkResponseBody(response_payload=unlink_response_payload)

        # Create response header
        response_header = G2PResponseHeader(
            request_id=unlink_request.request_header.request_id,
            response_status=G2PResponseStatus.SUCCESS,
            response_error_code=None,
            response_error_message=None,
            response_timestamp=datetime.now()
        )

        return UnlinkResponse(
            response_header=response_header,
            response_body=unlink_response_body
        )

    @staticmethod
    def construct_error_response(request, exception: Exception, error_code: str = None, error_message: str = None) -> G2PResponse:
        """
        Construct a G2PResponse error response following the G2PResponse schema
        """
        # Extract request_id from request header if available
        request_id = getattr(request.request_header, 'request_id', 'unknown') if hasattr(request, 'request_header') else 'unknown'
        
        # Use provided error details or extract from exception
        final_error_code = error_code or getattr(exception, 'validation_error_type', 'rjct.internal.error')
        final_error_message = error_message or getattr(exception, 'message', str(exception))
        
        # Create response header with error status
        response_header = G2PResponseHeader(
            request_id=request_id,
            response_status=G2PResponseStatus.ERROR,
            response_error_code=final_error_code,
            response_error_message=final_error_message,
            response_timestamp=datetime.now()
        )
        
        # Create response body with null payload
        response_body = G2PResponseBody(response_payload=None)
        
        # Return G2PResponse
        return G2PResponse(
            response_header=response_header,
            response_body=response_body
        )
