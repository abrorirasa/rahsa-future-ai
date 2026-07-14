import os
from dotenv import load_dotenv
import asyncpg
import asyncio

load_dotenv()

async def test():
    conn = await asyncpg.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=int(os.getenv("POSTGRES_PORT")),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        ssl="require",
    )
    version = await conn.fetchval("SELECT version();")
    print("BERHASIL connect ke database!")
    print(version)
    await conn.close()

asyncio.run(test())
