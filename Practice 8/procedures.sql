-- 1. добавить или обновить пользователя
CREATE OR REPLACE PROCEDURE insert_or_update_user(
    p_first_name VARCHAR,
    p_last_name VARCHAR,
    p_phone VARCHAR,
    p_email VARCHAR,
    p_address TEXT
)
AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE phone = p_phone) THEN
        UPDATE phonebook
        SET first_name = p_first_name,
            last_name = p_last_name,
            email = p_email,
            address = p_address
        WHERE phone = p_phone;
    ELSE
        INSERT INTO phonebook(first_name, last_name, phone, email, address)
        VALUES (p_first_name, p_last_name, p_phone, p_email, p_address);
    END IF;
END;
$$ LANGUAGE plpgsql;


-- 2. массовая вставка с проверкой
CREATE OR REPLACE PROCEDURE insert_many_users(
    names TEXT[],
    phones TEXT[]
)
AS $$
DECLARE
    i INT;
    invalid_data TEXT := '';
BEGIN
    FOR i IN 1..array_length(names, 1) LOOP

        IF phones[i] ~ '^[0-9]{10,}$' THEN
            INSERT INTO phonebook(first_name, phone)
            VALUES (names[i], phones[i])
            ON CONFLICT (phone) DO NOTHING;
        ELSE
            invalid_data := invalid_data || names[i] || ':' || phones[i] || E'\n';
        END IF;

    END LOOP;

    RAISE NOTICE 'Invalid data: %', invalid_data;
END;
$$ LANGUAGE plpgsql;


-- 3. удаление по имени или телефону
CREATE OR REPLACE PROCEDURE delete_user(p_value TEXT)
AS $$
BEGIN
    DELETE FROM phonebook
    WHERE first_name = p_value
       OR last_name = p_value
       OR phone = p_value;
END;
$$ LANGUAGE plpgsql;