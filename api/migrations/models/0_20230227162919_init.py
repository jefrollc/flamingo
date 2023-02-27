from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "project" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "created" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "modified" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "name" VARCHAR(128) NOT NULL UNIQUE,
    "description" TEXT,
    "step" INT NOT NULL  DEFAULT 0,
    "data" JSON
) /* Project ORM */;
CREATE TABLE IF NOT EXISTS "item" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "created" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "modified" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "key" VARCHAR(512) NOT NULL UNIQUE,
    "step" INT NOT NULL  DEFAULT 0,
    "data" JSON,
    "project_id" INT REFERENCES "project" ("id") ON DELETE CASCADE
) /* Item ORM */;
CREATE INDEX IF NOT EXISTS "idx_item_project_7fa41d" ON "item" ("project_id", "key");
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
