-- Инициализация базы данных для Beauty Shop
-- Этот скрипт выполняется автоматически при старте PostgreSQL контейнера

-- Создание таблицы записей
CREATE TABLE IF NOT EXISTS records (
    date DATE PRIMARY KEY,
    srv TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Создание индекса для более быстрого поиска по датам
CREATE INDEX IF NOT EXISTS idx_records_date ON records(date);

-- Вставка примера данных (опционально, можно удалить)
-- INSERT INTO records (date, srv) VALUES 
--     ('2026-03-15'::date, '💅 Маникюр'),
--     ('2026-03-16'::date, '✂️ Стрижка');

-- Вывод информации
SELECT 'Database initialization completed successfully!' as status;
