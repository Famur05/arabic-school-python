import asyncio
from queries.user import create_tables

if __name__ == "__main__":
    asyncio.run(create_tables())