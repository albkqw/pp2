-- 1. поиск по шаблону
CREATE OR REPLACE FUNCTION search_pattern(pattern TEXT)
RETURNS TABLE(
    id INT,
    first_name VARCHAR,
    last_name VARCHAR,
    phone VARCHAR,
    email VARCHAR,
    address TEXT
)
AS $$
BEGIN
    RETURN QUERY
    SELECT p.id, p.first_name, p.last_name, p.phone, p.email, p.address
    FROM phonebook p
    WHERE p.first_name ILIKE '%' || pattern || '%'
       OR p.last_name ILIKE '%' || pattern || '%'
       OR p.phone ILIKE '%' || pattern || '%';
END;
$$ LANGUAGE plpgsql;


-- 2. пагинация
CREATE OR REPLACE FUNCTION get_contacts_paginated(limit_val INT, offset_val INT)
RETURNS TABLE(
    id INT,
    first_name VARCHAR,
    last_name VARCHAR,
    phone VARCHAR,
    email VARCHAR,
    address TEXT
)
AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM phonebook
    ORDER BY id
    LIMIT limit_val OFFSET offset_val;
END;
$$ LANGUAGE plpgsql;