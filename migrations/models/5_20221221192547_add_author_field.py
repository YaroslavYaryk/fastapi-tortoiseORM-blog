from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "post" ADD "author_id" INT;
        ALTER TABLE "post" ADD CONSTRAINT "fk_post_user_4fc8b4bc" FOREIGN KEY ("author_id") REFERENCES "user" ("id") ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "post" DROP CONSTRAINT "fk_post_user_4fc8b4bc";
        ALTER TABLE "post" DROP COLUMN "author_id";"""
