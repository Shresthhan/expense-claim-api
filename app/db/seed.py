"""Database seed helpers."""
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.claim import Claim, ClaimStatus
from app.models.user import User, UserRole


def seed_data(db: Session) -> None:
    admin = db.query(User).filter(User.email == "admin@test.com").first()
    if not admin:
        admin = User(
            email="admin@test.com",
            password_hash=hash_password("Admin@123"),
            role=UserRole.ADMIN,
            manager_id=None,
        )
        db.add(admin)

    manager = db.query(User).filter(User.email == "manager@test.com").first()
    if not manager:
        manager = User(
            email="manager@test.com",
            password_hash=hash_password("Manager@123"),
            role=UserRole.MANAGER,
            manager_id=None,
        )
        db.add(manager)

    db.commit()

    manager = db.query(User).filter(User.email == "manager@test.com").first()

    employees = [
        ("emp1@test.com", "Emp@123", manager.id),
        ("emp2@test.com", "Emp@123", manager.id),
        ("emp3@test.com", "Emp@123", None),
    ]

    for email, password, manager_id in employees:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            user = User(
                email=email,
                password_hash=hash_password(password),
                role=UserRole.EMPLOYEE,
                manager_id=manager_id,
            )
            db.add(user)

    db.commit()

    employee_users = (
        db.query(User)
        .filter(User.role == UserRole.EMPLOYEE)
        .all()
    )

    for employee in employee_users:
        existing_claim = db.query(Claim).filter(Claim.user_id == employee.id).first()
        if not existing_claim:
            claim = Claim(
                user_id=employee.id,
                title=f"Seed claim for {employee.email}",
                amount=100.00,
                status=ClaimStatus.PENDING,
            )
            db.add(claim)

    db.commit()