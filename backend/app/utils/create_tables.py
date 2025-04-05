import asyncio
from app.core.database import engine, Base
from app.models import user  # ✅ import your models here

async def create():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

def main():
    asyncio.run(create())

if __name__ == '__main__':
    main()
