-- Procedure: insert or update a single user
CREATE OR REPLACE PROCEDURE upsert_contact(p_username VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO phonebook(username, phone)
    VALUES (p_username, p_phone)
    ON CONFLICT (username)
    DO UPDATE SET phone = EXCLUDED.phone;
END;
$$;


-- Procedure: insert many users, validate phone, return incorrect ones
CREATE OR REPLACE PROCEDURE insert_many_contacts(p_usernames VARCHAR[], p_phones VARCHAR[])
LANGUAGE plpgsql AS $$
DECLARE
    i INT;
BEGIN
    FOR i IN 1 .. array_length(p_usernames, 1) LOOP
        IF p_phones[i] ~ '[a-zA-Z!@#$%]' THEN
            RAISE NOTICE 'Invalid phone: %', p_phones[i];
        ELSE
            CALL upsert_contact(p_usernames[i], p_phones[i]);
        END IF;
    END LOOP;
END;
$$;


-- Procedure: delete by username or phone
CREATE OR REPLACE PROCEDURE delete_contact(p_value VARCHAR, p_type VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF p_type = 'username' THEN
        DELETE FROM phonebook WHERE username = p_value;
    ELSIF p_type = 'phone' THEN
        DELETE FROM phonebook WHERE phone = p_value;
    ELSE
        RAISE EXCEPTION 'Invalid type: use username or phone';
    END IF;
END;
$$;