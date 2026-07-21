"""Access control helpers."""
from fastapi import HTTPException, status

from app.models.claim import Claim
from app.models.user import User, UserRole


def can_view_claim(current_user: User, claim: Claim) -> bool:
    if current_user.role == UserRole.ADMIN:
        return True

    if current_user.role == UserRole.EMPLOYEE:
        return claim.user_id == current_user.id

    if current_user.role == UserRole.MANAGER:
        return (
            claim.user_id == current_user.id
            or claim.user.manager_id == current_user.id
        )

    return False


def ensure_can_view_claim(current_user: User, claim: Claim) -> None:
    if not can_view_claim(current_user, claim):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to access this claim",
        )


def ensure_can_update_claim_status(current_user: User, claim: Claim) -> None:
    if current_user.role not in [UserRole.MANAGER, UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only managers and admins can change claim status",
        )

    if current_user.role == UserRole.MANAGER and claim.user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Managers cannot change the status of their own claims",
        )