from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict

# Constant for strategy ID key in additional_info
STRATEGY_ID_KEY = "strategy_id"


class StrategyTypeEnum(str, Enum):
    """Enum for Strategy types"""

    ID = "ID"
    FA = "FA"


class StrategySchema(BaseModel):
    """
    Pydantic schema for Strategy model.

    Used for API responses and data validation.
    """

    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    description: Optional[str] = None
    strategy_type: StrategyTypeEnum
    construct_strategy: str
    deconstruct_strategy: str


class StrategyCreateSchema(BaseModel):
    """Schema for creating a new Strategy"""

    description: Optional[str] = None
    strategy_type: StrategyTypeEnum
    construct_strategy: str
    deconstruct_strategy: str


class StrategyUpdateSchema(BaseModel):
    """Schema for updating a Strategy"""

    description: Optional[str] = None
    strategy_type: Optional[StrategyTypeEnum] = None
    construct_strategy: Optional[str] = None
    deconstruct_strategy: Optional[str] = None


class KeyValuePair(BaseModel):
    """
    Schema for key-value pairs used in ID/FA construction and deconstruction.

    Used by StrategyHelper to pass data for constructing and deconstructing
    ID and FA values using regex patterns and format strings.
    """

    key: str
    value: str


class Fa(BaseModel):
    """
    Schema for Financial Account (FA) data.

    Contains the FA value and associated strategy_id for construction/deconstruction.
    """

    model_config = ConfigDict(from_attributes=True)

    strategy_id: int

    def dict(self, **kwargs):
        """Return dictionary representation of the model"""
        return super().model_dump(**kwargs)
