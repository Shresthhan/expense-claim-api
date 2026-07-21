"""Auth routes."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.security import hash_password, verify_password, create_access_token
from app.db.session import get_db
from app.models.user import User, UserRole
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.user import UserCreate, UserResponse
from fastapi import APIRouter, Depends, HTTPException, Request, status
from app.core.rate_limit import record_failed_attempt, clear_failed_attempts

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    user = User(
        email=user_in.email,
        password_hash=hash_password(user_in.password),
        role=UserRole.EMPLOYEE,
        manager_id=None,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.post("/login", response_model=TokenResponse)
def login(
    login_in: LoginRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    client_ip = request.client.host if request.client else "unknown"

    user = db.query(User).filter(User.email == login_in.email).first()

    if not user or not verify_password(login_in.password, user.password_hash):
        failed_count = record_failed_attempt(client_ip)

        if failed_count >= 6:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many failed login attempts. Please try again later.",
            )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    clear_failed_attempts(client_ip)

    access_token = create_access_token(subject=str(user.id))
    return TokenResponse(access_token=access_token)