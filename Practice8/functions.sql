-- Function: search by pattern (username or phone)
CREATE OR REPLACE FUNCTION search_phonebook(pattern TEXT)
RETURNS TABLE(id INT, username VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
        SELECT p.id, p.username, p.phone
        FROM phonebook p
        WHERE p.username ILIKE '%' || pattern || '%'    -- || means concat in SQL
           OR p.phone LIKE pattern || '%';
           -- ILIKE = case-insensitive search
           -- % before and after = match anything around the pattern
END;
$$ LANGUAGE plpgsql;


-- Function: get contacts with pagination (by limit and offset)
-- page_limit = how many rows to show, page_offset = how many rows to skip
CREATE OR REPLACE FUNCTION get_phonebook_page(page_limit INT, page_offset INT)
RETURNS TABLE(id INT, username VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
        SELECT p.id, p.username, p.phone
        FROM phonebook p
        ORDER BY p.username     -- sort alphabetically
        LIMIT page_limit        -- take only this many rows
        OFFSET page_offset;     -- skip this many rows from the start
END;
$$ LANGUAGE plpgsql;