-- Создание базы данных football_ai
CREATE DATABASE football_ai;

-- Подключение к созданной базе данных
\c football_ai;

-- Создание простой таблицы для тестирования
CREATE TABLE IF NOT EXISTS test_table (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Вставка тестовых данных
INSERT INTO test_table (name) VALUES ('Test Entry 1'), ('Test Entry 2'); 