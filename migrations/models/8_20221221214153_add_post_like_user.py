from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "postlike" ADD "user_id" INT NOT NULL;
        ALTER TABLE "postlike" ADD CONSTRAINT "fk_postlike_user_4491f3b9" FOREIGN KEY ("user_id") REFERENCES "user" ("id") ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "postlike" DROP CONSTRAINT "fk_postlike_user_4491f3b9";
        ALTER TABLE "postlike" DROP COLUMN "user_id";"""
