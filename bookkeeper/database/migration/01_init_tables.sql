-- up
CREATE TABLE IF NOT EXISTS expense (
    "amount" INTEGER NOT NULL CHECK("amount" >= 0),
    "category" INTEGER,
    "expense_date" TEXT NOT NULL,
    "added_date" TEXT NOT NULL,
    "comment" TEXT CHECK(length("comment") <= 100)
);

CREATE TABLE IF NOT EXISTS budget (
    "amount" INTEGER NOT NULL CHECK("amount" >= 0),
    "category" INTEGER,
    "period" TEXT NOT NULL DEFAULT 'D' CHECK("period" IN ('D', 'W', 'M'))
);

CREATE TABLE IF NOT EXISTS category (
    "name" TEXT NOT NULL CHECK(length("name") < 30),
    "parent_id" INTEGER NOT NULL CHECK("amount" >= 0)
);

-- down
DROP TABLE IF EXISTS expense;
DROP TABLE IF EXISTS budget;
DROP TABLE IF EXISTS category;