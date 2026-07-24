from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import select

from bookverse.auth import Token, create_access_token, decode_token, hash_password, verify_password
from bookverse.config import settings
from bookverse.db import get_session_factory
from bookverse.models import UserProfile

router = APIRouter(prefix="/auth", tags=["auth"])
session_factory = get_session_factory()
bearer_scheme = HTTPBearer()


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=256)
    display_name: str | None = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: str
    email: str
    display_name: str | None = None


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> UserProfile:
    payload = decode_token(credentials.credentials)
    if payload is None or "sub" not in payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid_token")

    async with session_factory() as session:
        user = await session.get(UserProfile, payload["sub"])
        if user is None or not user.is_active:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid_token")
        return user


def _issue_token(user_id: str) -> Token:
    access_token = create_access_token({"sub": user_id})
    return Token(access_token=access_token, expires_in=settings.jwt_expire_minutes * 60)


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(request: RegisterRequest) -> Token:
    async with session_factory() as session:
        existing = await session.execute(select(UserProfile).where(UserProfile.email == request.email))
        if existing.scalar_one_or_none() is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="email_already_registered")

        user = UserProfile(
            email=request.email,
            hashed_password=hash_password(request.password),
            display_name=request.display_name,
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        user_id = str(user.id)

    return _issue_token(user_id)


@router.post("/login", response_model=Token)
async def login(request: LoginRequest) -> Token:
    async with session_factory() as session:
        result = await session.execute(select(UserProfile).where(UserProfile.email == request.email))
        user = result.scalar_one_or_none()

    if user is None or not user.hashed_password or not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid_credentials")

    return _issue_token(str(user.id))


@router.get("/me", response_model=UserOut)
async def me(current_user: UserProfile = Depends(get_current_user)) -> UserOut:
    return UserOut(id=str(current_user.id), email=current_user.email, display_name=current_user.display_name)
