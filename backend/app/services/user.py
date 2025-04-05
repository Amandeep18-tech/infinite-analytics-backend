
from sqlalchemy.future import select
from app.models.user import User
from app.core.database import get_db_session

async def get_or_create_google_user(profile: dict):
    async with get_db_session() as session:
        stmt = select(User).where(User.email == profile["email"])
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if user:
            return user

        user = User(
            email=profile["email"],
            name=profile.get("name")
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user
