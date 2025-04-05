from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.utils.deps import get_current_user
from app.schemas.user import UserPublic, UserUpdate
from app.models.user import User
from passlib.context import CryptContext

router = APIRouter(prefix="/profile", tags=["Profile"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.get("/", response_model=UserPublic)
async def get_profile(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/", response_model=UserPublic)
async def update_profile(data: UserUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    if data.password:
        data.password = pwd_context.hash(data.password)

    for field, value in data.dict(exclude_unset=True).items():
        if field == "password":
            setattr(current_user, "hashed_password", value)
        else:
            setattr(current_user, field, value)

    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)
    return current_user
