CREATE OR REPLACE FUNCTION get_contacts_by_pattern(p_pattern TEXT)
RETURNS TABLE(first_name VARCHAR, last_name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT c.first_name, c.last_name, c.phone
    FROM phonebook c
    WHERE c.first_name ILIKE '%' || p_pattern || '%'
       OR c.last_name ILIKE '%' || p_pattern || '%'
       OR c.phone ILIKE '%' || p_pattern || '%';
END;
$$ LANGUAGE plpgsql;
