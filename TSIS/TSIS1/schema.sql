DROP TABLE IF EXISTS phones   CASCADE;
DROP TABLE IF EXISTS contacts CASCADE;
DROP TABLE IF EXISTS groups   CASCADE;
-- CASCADE означает: удалить ВСЁ, что зависит от таблицы

CREATE TABLE groups (
    id   SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);


INSERT INTO groups (name) VALUES
    ('Family'),
    ('Work'),
    ('Friend'),
    ('Other');
--я хочу вставить данные ТОЛЬКО в колонку name

CREATE TABLE contacts (
    id         SERIAL PRIMARY KEY,
    first_name VARCHAR(50)  NOT NULL,
    last_name  VARCHAR(50),
    email      VARCHAR(100),
    birthday   DATE,
    group_id   INTEGER REFERENCES groups(id), --это FOREIGN KEY
    created_at TIMESTAMP DEFAULT NOW() --автоматически ставится текущее время
);

CREATE TABLE phones (
    id         SERIAL PRIMARY KEY,
    contact_id INTEGER REFERENCES contacts(id) ON DELETE CASCADE, --если удалить контакт → удалятся все его телефоны
    phone      VARCHAR(20) NOT NULL,
    type       VARCHAR(10) CHECK (type IN ('home', 'work', 'mobile')) --только эти 3 значения
);

SELECT table_name FROM information_schema.tables --information_schema.tables Это системная таблица PostgreSQL
WHERE table_schema = 'public' --покажи только таблицы из основной базы
ORDER BY table_name;