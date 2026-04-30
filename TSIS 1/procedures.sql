CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone VARCHAR,
    p_type VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    c_id INT;
BEGIN
    SELECT id INTO c_id
    FROM phonebook
    WHERE first_name = p_contact_name;

    IF c_id IS NULL THEN
        RAISE EXCEPTION 'Contact not found';
    END IF;

    INSERT INTO phones(contact_id, phone, type)
    VALUES (c_id, p_phone, p_type);
END;
$$;


CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    g_id INT;
BEGIN
    SELECT id INTO g_id
    FROM groups
    WHERE name = p_group_name;

    IF g_id IS NULL THEN
        INSERT INTO groups(name)
        VALUES (p_group_name)
        RETURNING id INTO g_id;
    END IF;

    UPDATE phonebook
    SET group_id = g_id
    WHERE first_name = p_contact_name;
END;
$$;