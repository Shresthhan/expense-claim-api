"""Claim service."""
from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.models.claim import Claim, ClaimStatus
from app.models.user import User, UserRole
from app.schemas.claim import ClaimCreate
from app.services.access_control import ensure_can_view_claim, ensure_can_update_claim_status


def create_claim(db: Session, current_user: User, claim_in: ClaimCreate) -> Claim:
    if current_user.role != UserRole.EMPLOYEE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only employees can create claims",
        )

    claim = Claim(
        user_id=current_user.id,
        title=claim_in.title,
        amount=claim_in.amount,
        status=ClaimStatus.PENDING,
    )

    db.add(claim)
    db.commit()
    db.refresh(claim)
    return claim


def get_visible_claims(db: Session, current_user: User):
    query = db.query(Claim).options(joinedload(Claim.user))

    if current_user.role == UserRole.ADMIN:
        return query.all()

    if current_user.role == UserRole.EMPLOYEE:
        return query.filter(Claim.user_id == current_user.id).all()

    if current_user.role == UserRole.MANAGER:
        return query.join(Claim.user).filter(
            (Claim.user_id == current_user.id) |
            (User.manager_id == current_user.id)
        ).all()

    return []


def get_claim_by_id(db: Session, claim_id: int) -> Claim:
    claim = (
        db.query(Claim)
        .options(joinedload(Claim.user))
        .filter(Claim.id == claim_id)
        .first()
    )

    if not claim:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Claim not found",
        )

    return claim


def get_visible_claim_by_id(db: Session, current_user: User, claim_id: int) -> Claim:
    claim = get_claim_by_id(db, claim_id)
    ensure_can_view_claim(current_user, claim)
    return claim


def update_claim_status(
    db: Session,
    current_user: User,
    claim: Claim,
    new_status: ClaimStatus,
) -> Claim:
    ensure_can_update_claim_status(current_user, claim)

    if new_status not in [ClaimStatus.APPROVED, ClaimStatus.REJECTED]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Status must be APPROVED or REJECTED",
        )

    if claim.status != ClaimStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only pending claims can be updated",
        )

    claim.status = new_status
    db.commit()
    db.refresh(claim)
    return claim