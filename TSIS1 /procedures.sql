CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone        VARCHAR,
    p_type         VARCHAR
)
LANGUAGE plpgsql AS $$
DECLARE
    v_contact_id INT;
BEGIN
    SELECT contact_id INTO v_contact_id
    FROM contacts
    WHERE contact_name = p_contact_name;

    IF v_contact_id IS NULL THEN
        RAISE NOTICE 'Contact "%" not found.', p_contact_name;
        RETURN;
    END IF;

    INSERT INTO phones(contact_id, phone, type)
    VALUES (v_contact_id, p_phone, p_type);

    RAISE NOTICE 'Phone % (%) added to "%".', p_phone, p_type, p_contact_name;
END;
$$;

CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name   VARCHAR
)
LANGUAGE plpgsql AS $$
DECLARE
    v_group_id INT;
BEGIN
    SELECT id INTO v_group_id FROM groups WHERE name = p_group_name;

    IF v_group_id IS NULL THEN
        INSERT INTO groups(name) VALUES (p_group_name) RETURNING id INTO v_group_id;
        RAISE NOTICE 'Group "%" created.', p_group_name;
    END IF;

    UPDATE contacts SET group_id = v_group_id WHERE contact_name = p_contact_name;

    IF NOT FOUND THEN
        RAISE NOTICE 'Contact "%" not found.', p_contact_name;
    ELSE
        RAISE NOTICE 'Contact "%" moved to group "%".', p_contact_name, p_group_name;
    END IF;
END;
$$;

CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(
    id            INT,
    contact_name  VARCHAR,
    email         VARCHAR,
    birthday      DATE,
    group_name    VARCHAR,
    phone         VARCHAR,
    phone_type    VARCHAR
)
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
        SELECT DISTINCT
            c.contact_id,
            c.contact_name,
            c.email,
            c.birthday,
            g.name        AS group_name,
            p.phone,
            p.type        AS phone_type
        FROM contacts c
        LEFT JOIN groups g ON g.id = c.group_id
        LEFT JOIN phones p ON p.contact_id = c.contact_id
        WHERE
            c.contact_name ILIKE '%' || p_query || '%'
         OR c.email        ILIKE '%' || p_query || '%'
         OR p.phone        ILIKE '%' || p_query || '%'
        ORDER BY c.contact_name;
END;
$$;
