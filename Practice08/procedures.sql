CREATE OR REPLACE PROCEDURE upsert_contact(
    p_first_name VARCHAR,
    p_last_name VARCHAR,
    p_phone VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- если контакт уже есть, обновляем телефон
    IF EXISTS (
        SELECT 1 FROM phonebook
        WHERE first_name = p_first_name AND last_name = p_last_name
    ) THEN
        UPDATE phonebook
        SET phone = p_phone
        WHERE first_name = p_first_name AND last_name = p_last_name;
    ELSE
        -- иначе добавляем новый
        INSERT INTO phonebook(first_name, last_name, phone)
        VALUES (p_first_name, p_last_name, p_phone);
    END IF;
END;
$$;


CREATE OR REPLACE PROCEDURE delete_contact(
    p_first_name VARCHAR,
    p_last_name VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM phonebook
    WHERE first_name = p_first_name AND last_name = p_last_name;
END;
$$;
