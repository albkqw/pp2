CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(
    id INT,
    first_name VARCHAR,
    last_name VARCHAR,
    email VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT
        p.id,
        p.first_name,
        p.last_name,
        p.email
    FROM phonebook p
    LEFT JOIN phones ph
        ON ph.contact_id = p.id
    WHERE p.first_name ILIKE '%' || p_query || '%'
       OR p.last_name ILIKE '%' || p_query || '%'
       OR p.email ILIKE '%' || p_query || '%'
       OR p.phone ILIKE '%' || p_query || '%'
       OR ph.phone ILIKE '%' || p_query || '%';
END;
$$;


CREATE OR REPLACE FUNCTION get_contacts_paginated(
    limit_val INT,
    offset_val INT
)
RETURNS TABLE(
    id INT,
    first_name VARCHAR,
    last_name VARCHAR,
    email VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        p.id,
        p.first_name,
        p.last_name,
        p.email
    FROM phonebook p
    ORDER BY p.id
    LIMIT limit_val OFFSET offset_val;
END;
$$;