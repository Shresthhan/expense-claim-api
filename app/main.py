from fastapi import FastAPI

from app.api.routes import auth, me, claims, users
from app.core.config import settings
from app.db.base import Base
from app.db.seed import seed_data
from app.db.session import engine, SessionLocal

app = FastAPI(title=settings.app_name)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        seed_data(db)
    finally:
        db.close()


app.include_router(auth.router)
app.include_router(me.router)
app.include_router(claims.router)
app.include_router(users.router)


@app.get("/")
def root():
    return {"message": f"{settings.app_name} is running"}