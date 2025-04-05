from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.context import CryptContext
from fastapi.responses import RedirectResponse

from app.schemas.user import UserCreate, UserLogin, UserPublic
from app.models.user import User
from app.core.database import get_db
from app.utils.jwt import create_access_token
from app.core.oauth import oauth
from app.services.user import get_or_create_google_user

router = APIRouter(prefix="/auth", tags=["Auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register", response_model=UserPublic)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user.email))
    if result.scalar():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pw = pwd_context.hash(user.password)
    new_user = User(email=user.email, hashed_password=hashed_pw)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@router.post("/login")
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user.email))
    db_user = result.scalar()
    if not db_user or not pwd_context.verify(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(db_user.id)})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/login/google")
async def login_with_google(request: Request):
    redirect_uri = request.url_for('google_callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/callback/google")
async def google_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user_data = await oauth.google.get("userinfo", token=token)
    profile = user_data.json()

    user = await get_or_create_google_user(profile)
    jwt = create_access_token({"sub": str(user.id)})
    return {"access_token": jwt, "token_type": "bearer"}

@router.post("/logout")
async def logout():
    return {"message": "Successfully signed out. Please delete token on client side."}
