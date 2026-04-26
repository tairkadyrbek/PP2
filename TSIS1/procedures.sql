-- Function: search contacts (extended to search all fields + phones)
CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(
    id INT,
    username VARCHAR,
    email VARCHAR,
    birthday DATE,
    group_name VARCHAR,
    phone VARCHAR,
    phone_type VARCHAR
)
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT
        c.id,
        c.username,
        c.email,
        c.birthday,
        g.name AS group_name,
        p.phone,
        p.type AS phone_type
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    LEFT JOIN phones p ON c.id = p.contact_id
    WHERE 
        c.username ILIKE '%' || p_query || '%'
        OR c.email ILIKE '%' || p_query || '%'
        OR p.phone ILIKE '%' || p_query || '%'
    ORDER BY c.username;
END;
$$;


-- Procedure: insert or update a single contact
CREATE OR REPLACE PROCEDURE upsert_contact(
    p_username VARCHAR, 
    p_email VARCHAR DEFAULT NULL, 
    p_birthday DATE DEFAULT NULL,
    p_group_name VARCHAR DEFAULT 'Other'
)
LANGUAGE plpgsql AS $$
DECLARE
    v_group_id INT;
BEGIN
    -- Get or create group
    SELECT id INTO v_group_id FROM groups WHERE name = p_group_name;
    
    IF v_group_id IS NULL THEN
        INSERT INTO groups(name) VALUES (p_group_name) RETURNING id INTO v_group_id;
    END IF;
    
    -- Upsert contact
    INSERT INTO contacts(username, email, birthday, group_id)
    VALUES (p_username, p_email, p_birthday, v_group_id)
    ON CONFLICT (username)
    DO UPDATE SET 
        email = COALESCE(EXCLUDED.email, contacts.email),
        birthday = COALESCE(EXCLUDED.birthday, contacts.birthday),
        group_id = EXCLUDED.group_id;
END;
$$;


-- Procedure: insert many contacts
CREATE OR REPLACE PROCEDURE insert_many_contacts(p_usernames VARCHAR[], p_phones VARCHAR[])
LANGUAGE plpgsql AS $$
DECLARE
    i INT;
    v_contact_id INT;
BEGIN
    FOR i IN 1 .. array_length(p_usernames, 1) LOOP
        IF p_phones[i] ~ '[a-zA-Z!@#$%]' THEN
            RAISE NOTICE 'Invalid phone: %', p_phones[i];
        ELSE
            -- Insert contact
            CALL upsert_contact(p_usernames[i]);
            
            -- Get contact id
            SELECT id INTO v_contact_id FROM contacts WHERE username = p_usernames[i];
            
            -- Add phone
            INSERT INTO phones(contact_id, phone, type)
            VALUES (v_contact_id, p_phones[i], 'mobile')
            ON CONFLICT DO NOTHING;
        END IF;
    END LOOP;
END;
$$;


-- Procedure: delete by username or phone
CREATE OR REPLACE PROCEDURE delete_contact(p_value VARCHAR, p_type VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF p_type = 'username' THEN
        DELETE FROM contacts WHERE username = p_value;

    ELSIF p_type = 'phone' THEN
        DELETE FROM phones WHERE phone = p_value;

    ELSE
        RAISE EXCEPTION 'Invalid type';
    END IF;
END;
$$;


-- Function: get paginated contacts
CREATE OR REPLACE FUNCTION get_contacts_page(p_limit INT, p_offset INT)
RETURNS TABLE(
    id INT, 
    username VARCHAR, 
    email VARCHAR, 
    birthday DATE, 
    group_name VARCHAR,
    created_at TIMESTAMP
)
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
    SELECT c.id, c.username, c.email, c.birthday, g.name, c.created_at
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    ORDER BY c.created_at DESC
    LIMIT p_limit OFFSET p_offset;
END;
$$;


-- Procedure: add phone to existing contact
CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR, 
    p_phone VARCHAR, 
    p_type VARCHAR DEFAULT 'mobile'
)
LANGUAGE plpgsql AS $$
DECLARE
    v_contact_id INT;
BEGIN
    -- Validate phone type
    IF p_type NOT IN ('home', 'work', 'mobile') THEN
        RAISE EXCEPTION 'Invalid phone type. Use: home, work, or mobile';
    END IF;
    
    -- Get contact id
    SELECT id INTO v_contact_id FROM contacts WHERE username = p_contact_name;
    
    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact % not found', p_contact_name;
    END IF;
    
    -- Insert phone
    INSERT INTO phones(contact_id, phone, type)
    VALUES (v_contact_id, p_phone, p_type);
    
    RAISE NOTICE 'Phone % added to contact %', p_phone, p_contact_name;
END;
$$;


-- Procedure: move contact to a different group
CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR, 
    p_group_name VARCHAR
)
LANGUAGE plpgsql AS $$
DECLARE
    v_group_id INT;
    v_contact_id INT;
BEGIN
    -- Get or create group
    SELECT id INTO v_group_id FROM groups WHERE name = p_group_name;
    
    IF v_group_id IS NULL THEN
        INSERT INTO groups(name) VALUES (p_group_name) RETURNING id INTO v_group_id;
        RAISE NOTICE 'Created new group: %', p_group_name;
    END IF;
    
    -- Get contact id
    SELECT id INTO v_contact_id FROM contacts WHERE username = p_contact_name;
    
    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact % not found', p_contact_name;
    END IF;
    
    -- Update contact group
    UPDATE contacts SET group_id = v_group_id WHERE id = v_contact_id;
    
    RAISE NOTICE 'Moved % to group %', p_contact_name, p_group_name;
END;
$$;

