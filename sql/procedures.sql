DROP PROCEDURE IF EXISTS create_rezervare;
-- PROC_END

CREATE PROCEDURE create_rezervare(IN p_user_id INT, IN p_masa_json JSON, IN p_numar_persoane INT)
BEGIN
    DECLARE v_rezervari_id INT;
    DECLARE v_i INT DEFAULT 0;
    DECLARE v_len INT DEFAULT 0;
    DECLARE v_sku VARCHAR(50);
    DECLARE v_qty INT;

    -- 1) Cream comanda
    INSERT INTO rezervari(user_id, numar_persoane) VALUES (p_user_id, p_numar_persoane);
    SET v_rezervari_id = LAST_INSERT_ID();

    -- 2) Parcurgerem array-ul JSON
    SET v_len = JSON_LENGTH(p_masa_json);

    WHILE v_i < v_len DO
        SET v_sku = JSON_UNQUOTE(JSON_EXTRACT(p_masa_json, CONCAT('$[', v_i, '].sku')));
        SET v_qty = JSON_EXTRACT(p_masa_json, CONCAT('$[', v_i, '].qty'));

        -- Inseram rezervare
        INSERT INTO mese_rezervate(rezervare_id, user_id, numar_locuri, sku)
        VALUES (v_rezervari_id, p_user_id, v_qty, v_sku);

        SET v_i = v_i + 1;
    END WHILE;

    -- 3) Returnam rezervare_id
    SELECT v_rezervari_id AS rezervare_id;
END
-- PROC_END