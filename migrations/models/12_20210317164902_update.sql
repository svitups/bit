-- upgrade --
CREATE TABLE IF NOT EXISTS "codes" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "key" VARCHAR(255) NOT NULL,
    "time_create" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
-- downgrade --
DROP TABLE IF EXISTS "codes";