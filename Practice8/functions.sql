-- Function: search by pattern (username or phone)
CREATE OR REPLACE FUNCTION search_phonebook(pattern TEXT)
RETURNS TABLE(id INT, username VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
        SELECT p.id, p.username, p.phone
        FROM phonebook p
        WHERE p.username ILIKE '%' || pattern || '%'
           OR p.phone ILIKE '%' || pattern || '%';
END;
$$ LANGUAGE plpgsql;


-- Function: get contacts with pagination (by limit and offset)
CREATE OR REPLACE FUNCTION get_phonebook_page(page_limit INT, page_offset INT)
RETURNS TABLE(id INT, username VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
        SELECT p.id, p.username, p.phone
        FROM phonebook p
        ORDER BY p.username
        LIMIT page_limit OFFSET page_offset;
END;
$$ LANGUAGE plpgsql;