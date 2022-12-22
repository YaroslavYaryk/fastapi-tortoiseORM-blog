from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "postcomment" ADD "parent_id" INT NOT NULL;
        ALTER TABLE "postcomment" ADD CONSTRAINT "fk_postcomm_postcomm_fe8a4660" FOREIGN KEY ("parent_id") REFERENCES "postcomment" ("id") ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "postcomment" DROP CONSTRAINT "fk_postcomm_postcomm_fe8a4660";
        ALTER TABLE "postcomment" DROP COLUMN "parent_id";"""
