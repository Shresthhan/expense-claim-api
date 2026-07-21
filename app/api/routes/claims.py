"""Claim routes."""
from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.claim import ClaimCreate, ClaimResponse, ClaimStatusUpdate
from app.services.claim_service import (
    create_claim,
    get_visible_claims,
    get_visible_claim_by_id,
    update_claim_status,
)

router = APIRouter(prefix="/claims", tags=["claims"])


@router.post("", response_model=ClaimResponse, status_code=status.HTTP_201_CREATED)
def create_claim_endpoint(
    claim_in: ClaimCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_claim(db, current_user, claim_in)


@router.get("", response_model=List[ClaimResponse])
def list_claims(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_visible_claims(db, current_user)


@router.get("/{id}", response_model=ClaimResponse)
def get_claim(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_visible_claim_by_id(db, current_user, id)


@router.patch("/{id}/status", response_model=ClaimResponse)
def update_claim_status_endpoint(
    id: int,
    status_in: ClaimStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    claim = get_visible_claim_by_id(db, current_user, id)
    return update_claim_status(db, current_user, claim, status_in.status)