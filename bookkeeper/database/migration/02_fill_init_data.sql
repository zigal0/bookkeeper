-- up
INSERT INTO category (name, parent_id) VALUES
    ('Продукты', NULL),
    ('Мясо', 1),
    ('Сырое мясо', 2),
    ('Мясные продукты', 2),
    ('Сладости', 1),
    ('Книги', NULL),
    ('Одежда', NULL),
    ('Электроника', NULL),
    ('Обувь', 7),
    ('Молочные продукты', NULL);


INSERT INTO expense (amount, category_id, expense_date, added_date, comment) VALUES
    (1588.89, 7, DATE('now', '-2 days'), DATETIME('now'), NULL),
    (3819.69, 6, DATE('now'), DATETIME('now'), NULL),
    (3515.41, 7, DATE('now', '-4 days'), DATETIME('now'), NULL),
    (777.89, 8, DATE('now', '-3 days'), DATETIME('now'), NULL),
    (746.13, 3, DATE('now', '-10 days'), DATETIME('now'), 'какой-то комментарий'),
    (1438.42, 5, DATE('now', '-17 days'), DATETIME('now'), 'какой-то комментарий'),
    (4620.71, 1, DATE('now', '-20 days'), DATETIME('now'), 'какой-то комментарий'),
    (4251.21, 5, DATE('now', '-2 months'), DATETIME('now'), NULL),
    (3129.36, 5, DATE('now', '-5 months'), DATETIME('now'), 'какой-то комментарий'),
    (4288.73, 6, DATE('now', '-1 months'), DATETIME('now'), 'какой-то комментарий'),
    (392.01, 2, DATE('now', '-2 months'), DATETIME('now'), NULL),
    (2447.93, 3, DATE('now'), DATETIME('now'), NULL),
    (198.75, 6, DATE('now'), DATETIME('now'), NULL),
    (235.57, 2, DATE('now', '-1 days'), DATETIME('now'), 'какой-то комментарий'),
    (3469.4, 8, DATE('now'), DATETIME('now'), NULL),
    (4521.62, 6, DATE('now', '-5 days'), DATETIME('now'), 'какой-то комментарий'),
    (3860.12, 5, DATE('now', '-25 days'), DATETIME('now'), NULL),
    (420.37, 1, DATE('now', '-2 years'), DATETIME('now'), NULL),
    (1211.79, 2, DATE('now', '-5 years'), DATETIME('now'), 'какой-то комментарий'),
    (4599.25, 3, DATE('now', '-3 years'), DATETIME('now'), NULL);

INSERT INTO budget (amount, period) VALUES
    (1000, 'День'),
    (10000, 'Неделя'),
    (100000, 'Месяц'),
    (1000000, 'Год');


-- down
DELETE FROM budget;
DELETE FROM expense;
DELETE FROM category;