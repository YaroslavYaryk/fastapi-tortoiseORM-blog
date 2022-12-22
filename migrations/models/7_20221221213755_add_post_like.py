from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "postlike" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "post_id" INT NOT NULL REFERENCES "post" ("id") ON DELETE CASCADE
);;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "postlike";"""
