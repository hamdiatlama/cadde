from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.user.schemas import (
    UserCreate, UserLogin, UserUpdate, ChangePassword,
    UserResponse, TokenResponse,
)
from src.modules.user.service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(data: UserCreate, db: AsyncSession = Depends(get_db)):
    svc = AuthService(db)
    try:
        result = await svc.register(data.email, data.password, data.full_name, data.role, data.phone)
        await db.commit()
        await db.refresh(result["user"])
        return TokenResponse(
            access_token=result["access_token"],
            user=UserResponse.model_validate(result["user"]),
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=TokenResponse)
async def login(data: UserLogin, db: AsyncSession = Depends(get_db)):
    svc = AuthService(db)
    try:
        result = await svc.login(data.email, data.password)
        return TokenResponse(
            access_token=result["access_token"],
            user=UserResponse.model_validate(result["user"]),
        )
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return UserResponse.model_validate(current_user)


@router.put("/me", response_model=UserResponse)
async def update_profile(
    data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = AuthService(db)
    try:
        user = await svc.update_profile(current_user.id, data.model_dump(exclude_unset=True))
        await db.commit()
        await db.refresh(user)
        return UserResponse.model_validate(user)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/change-password", response_model=dict)
async def change_password(
    data: ChangePassword,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = AuthService(db)
    try:
        result = await svc.change_password(current_user.id, data.old_password, data.new_password)
        await db.commit()
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
