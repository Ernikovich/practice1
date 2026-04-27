CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone        VARCHAR,
    p_type         VARCHAR   -- 'home' | 'work' | 'mobile'
)
LANGUAGE plpgsql
AS $$
DECLARE --создаём переменную:
    v_contact_id INTEGER; --временно хранит id контакта
BEGIN
    SELECT id INTO v_contact_id
    FROM contacts
    WHERE first_name ILIKE p_contact_name
       OR (first_name || ' ' || COALESCE(last_name,'')) ILIKE p_contact_name
    LIMIT 1; --берём только 1 контакт
    --склеиваем имя + фамилию  если фамилии нет → ставим пустую строку

    -- COALESCE(last_name, '')
    -- 👉 значит:
    -- если last_name есть → бери его
    -- если нет (NULL) → бери пустую строку ''

    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact "%" not found', p_contact_name;
    END IF;

    INSERT INTO phones(contact_id, phone, type) --если контакт найден → добавляем ему номер
    VALUES (v_contact_id, p_phone, p_type);
END;
$$;



CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name   VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_contact_id INTEGER; --храним id контакта и группы
    v_group_id   INTEGER;
BEGIN
    SELECT id INTO v_group_id FROM groups WHERE name ILIKE p_group_name;
    IF v_group_id IS NULL THEN
        INSERT INTO groups(name) VALUES (p_group_name) RETURNING id INTO v_group_id;
        --создаём новую группу и сразу получаем её id
    END IF;

    SELECT id INTO v_contact_id
    FROM contacts
    WHERE first_name ILIKE p_contact_name
       OR (first_name || ' ' || COALESCE(last_name,'')) ILIKE p_contact_name
    LIMIT 1;

    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact "%" not found', p_contact_name;
    END IF;

    UPDATE contacts SET group_id = v_group_id WHERE id = v_contact_id; --у найденного человека меняется группа
END;
$$;


CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE( --верни мне как таблицу: id, имя, email и т.д.
    id         INTEGER,
    first_name VARCHAR,
    last_name  VARCHAR,
    email      VARCHAR,
    birthday   DATE,
    group_name VARCHAR,
    phones     TEXT       
)
AS $$
BEGIN
    RETURN QUERY --возьми результат этого SELECT и верни его как результат функции
    SELECT --берём данные из таблицы contacts
        c.id,
        c.first_name,
        c.last_name,
        c.email,
        c.birthday,
        g.name AS group_name,
        STRING_AGG(ph.phone || '(' || COALESCE(ph.type,'?') || ')', ', ') AS phones
        -- собери много строк в одну строку через запятую  777(mobile), 888(?)
    FROM contacts c
    LEFT JOIN groups g  ON g.id  = c.group_id
    LEFT JOIN phones ph ON ph.contact_id = c.id
    WHERE
        c.first_name ILIKE '%' || p_query || '%'
        OR c.last_name  ILIKE '%' || p_query || '%'
        OR c.email      ILIKE '%' || p_query || '%'
        OR ph.phone     ILIKE '%' || p_query || '%'
    GROUP BY c.id, c.first_name, c.last_name, c.email, c.birthday, g.name; --собери данные по каждому человеку отдельно
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_contacts_page(
    p_limit  INTEGER, --сколько строк показать
    p_offset INTEGER --с какой строки начать
)
RETURNS TABLE(
    id         INTEGER,
    first_name VARCHAR,
    last_name  VARCHAR,
    email      VARCHAR,
    birthday   DATE,
    group_name VARCHAR,
    phones     TEXT
)
AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.id,
        c.first_name,
        c.last_name,
        c.email,
        c.birthday,
        g.name AS group_name,
        STRING_AGG(ph.phone || '(' || COALESCE(ph.type,'?') || ')', ', ') AS phones
    FROM contacts c
    LEFT JOIN groups g  ON g.id  = c.group_id
    LEFT JOIN phones ph ON ph.contact_id = c.id
    GROUP BY c.id, c.first_name, c.last_name, c.email, c.birthday, g.name
    ORDER BY c.first_name, c.last_name
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;

-- GROUP BY собирает все строки одного контакта в одну “карточку”, чтобы можно было склеить его телефоны и данные