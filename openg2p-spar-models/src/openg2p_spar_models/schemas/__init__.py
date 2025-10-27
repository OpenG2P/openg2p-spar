
from .link import (
    StatusEnum,
    LinkStatusReasonCode,
    SingleLinkRequest,
    LinkRequestPayload,
    LinkRequestBody,
    SingleLinkResponse,
    LinkResponsePayload,
    LinkResponseBody,
    LinkRequest,
    LinkResponse,
)
from .resolve import (
    ResolveScope,
    ResolveStatusReasonCode,
    SingleResolveRequest,
    ResolveRequestPayload,
    ResolveRequestBody,
    AccountProviderInfo,
    SingleResolveResponse,
    ResolveResponsePayload,
    ResolveResponseBody,
    ResolveRequest,
    ResolveResponse,
)
from .unlink import (
    UnlinkStatusReasonCode,
    SingleUnlinkRequest,
    UnlinkRequestPayload,
    UnlinkRequestBody,
    SingleUnlinkResponse,
    UnlinkResponsePayload,
    UnlinkResponseBody,
    UnlinkRequest,
    UnlinkResponse,
)
from .update import (
    UpdateStatusReasonCode,
    SingleUpdateRequest,
    UpdateRequestPayload,
    UpdateRequestBody,
    SingleUpdateResponse,
    UpdateResponsePayload,
    UpdateResponseBody,
    UpdateRequest,
    UpdateResponse,
)
from .strategy import (
    StrategyTypeEnum,
    StrategySchema,
    StrategyCreateSchema,
    StrategyUpdateSchema,
    KeyValuePair,
    Fa,
    STRATEGY_ID_KEY,
)
from .dfsp import (
    ProviderTypeEnum,
    DfspProviderSchema,
    DfspProviderCreateSchema,
    DfspProviderUpdateSchema,
    DfspProviderValueSchema,
    DfspProviderValueCreateSchema,
    DfspProviderValueUpdateSchema,
)
from enum import Enum


class StatusReasonCodeEnum(Enum):
    rjct_action_not_supported = "rjct.action.not_supported"
    rjct_jwt_invalid = "rjct.jwt.invalid"
    rjct_signature_invalid = "rjct.signature.invalid"
    rjct_permission_denied = "rjct.permission.denied"
    rjct_internal_error = "rjct.internal.error"

