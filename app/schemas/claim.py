"""Claim schemas."""
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from app.models.claim import ClaimStatus


class ClaimCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    amount: Decimal = Field(..., gt=0)


class ClaimStatusUpdate(BaseModel):
    status: ClaimStatus


class ClaimResponse(BaseModel):
    id: int
    user_id: int
    title: str
    amount: Decimal
    status: ClaimStatus
    created_at: datetime

    class Config:
        from_attributes = True