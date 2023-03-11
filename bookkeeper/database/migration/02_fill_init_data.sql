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
    (1588.89, 7, '2022-04-30', DATETIME('now'), NULL),
    (3819.69, 6, '2022-07-15', DATETIME('now'), NULL),
    (3515.41, 7, '2023-01-14', DATETIME('now'), NULL),
    (777.89, 8, '2022-08-15', DATETIME('now'), NULL),
    (746.13, 3, '2022-07-30', DATETIME('now'), 'какой-то комментарий'),
    (1438.42, 5, '2023-01-25', DATETIME('now'), 'какой-то комментарий'),
    (4620.71, 1, '2022-10-26', DATETIME('now'), 'какой-то комментарий'),
    (4251.21, 5, '2022-06-07', DATETIME('now'), NULL),
    (3129.36, 5, '2023-01-10', DATETIME('now'), 'какой-то комментарий'),
    (4288.73, 6, '2022-07-09', DATETIME('now'), 'какой-то комментарий'),
    (392.01, 2, '2022-10-24', DATETIME('now'), NULL),
    (2447.93, 3, '2022-12-07', DATETIME('now'), NULL),
    (198.75, 6, '2023-02-15', DATETIME('now'), NULL),
    (235.57, 2, '2022-06-19', DATETIME('now'), 'какой-то комментарий'),
    (3469.4, 8, '2022-05-28', DATETIME('now'), NULL),
    (4521.62, 6, '2022-07-01', DATETIME('now'), 'какой-то комментарий'),
    (3860.12, 5, '2022-11-27', DATETIME('now'), NULL),
    (420.37, 1, '2022-03-28', DATETIME('now'), NULL),
    (1211.79, 2, '2022-07-10', DATETIME('now'), 'какой-то комментарий'),
    (4599.25, 3, '2022-07-28', DATETIME('now'), NULL);

INSERT INTO budget (amount, period) VALUES
    (100, 'День'),
    (1000, 'Неделя'),
    (10000, 'Месяц');


-- down
DELETE FROM budget;
DELETE FROM expense;
DELETE FROM category;