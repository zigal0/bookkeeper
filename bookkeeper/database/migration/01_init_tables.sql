-- up
CREATE TABLE IF NOT EXISTS category (
    pk INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL CHECK(length(name) < 20),
    parent_id INTEGER,
    FOREIGN KEY (parent_id) REFERENCES category (pk) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS expense (
    pk INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL NOT NULL CHECK(amount >= 0.0),
    category_id INTEGER,
    expense_date TEXT NOT NULL,
    added_date TEXT NOT NULL,
    comment TEXT CHECK(length(comment) <= 20),
	FOREIGN KEY (category_id) REFERENCES category (pk) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS budget (
    pk INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL NOT NULL CHECK(amount >= 0.0),
    period TEXT NOT NULL DEFAULT 'День' CHECK(period IN ('День', 'Неделя', 'Месяц', 'Год'))
);

-- down
DROP TABLE IF EXISTS budget;
DROP TABLE IF EXISTS expense;
DROP TABLE IF EXISTS category;