from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ProviderTypeEnum(str, Enum):
    """Enum for DFSP provider types"""

    BANK = "BANK"
    EMAIL_WALLET = "EMAIL_WALLET"
    MOBILE_WALLET = "MOBILE_WALLET"


class DfspProviderSchema(BaseModel):
    """
    Pydantic schema for DfspProvider model.

    Represents a top-level provider type.
    """

    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    code: str
    name: str
    provider_type: ProviderTypeEnum
    description: Optional[str] = None
    validation_regex: Optional[str] = None


class DfspProviderCreateSchema(BaseModel):
    """Schema for creating a new DfspProvider"""

    code: str
    name: str
    provider_type: ProviderTypeEnum
    description: Optional[str] = None
    validation_regex: Optional[str] = None


class DfspProviderUpdateSchema(BaseModel):
    """Schema for updating a DfspProvider"""

    code: Optional[str] = None
    name: Optional[str] = None
    provider_type: Optional[ProviderTypeEnum] = None
    description: Optional[str] = None
    validation_regex: Optional[str] = None


class DfspProviderValueSchema(BaseModel):
    """
    Pydantic schema for DfspProviderValue model.

    Represents a specific provider instance (e.g., a bank, branch, or wallet).
    """

    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    code: str
    name: str
    provider_type: ProviderTypeEnum
    parent_id: Optional[int] = None
    description: Optional[str] = None
    validation_regex: Optional[str] = None


class DfspProviderValueCreateSchema(BaseModel):
    """Schema for creating a new DfspProviderValue"""

    code: str
    name: str
    provider_type: ProviderTypeEnum
    parent_id: Optional[int] = None
    description: Optional[str] = None
    validation_regex: Optional[str] = None


class DfspProviderValueUpdateSchema(BaseModel):
    """Schema for updating a DfspProviderValue"""

    code: Optional[str] = None
    name: Optional[str] = None
    provider_type: Optional[ProviderTypeEnum] = None
    parent_id: Optional[int] = None
    description: Optional[str] = None
    validation_regex: Optional[str] = None
