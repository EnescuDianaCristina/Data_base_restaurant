DROP TRIGGER IF EXISTS trg_before_insert;
-- TRIGGER_END

CREATE TRIGGER trg_before_insert
BEFORE INSERT ON stoc
FOR EACH ROW
BEGIN
    IF NEW.nr_ingrediente <= 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Cantitatea trebuie sa fie mai mare decat 0';
    END IF;
END
-- TRIGGER_END

DROP TRIGGER IF EXISTS trg_after_update;
-- TRIGGER_END

CREATE TRIGGER trg_after_update
AFTER UPDATE ON ingrediente
FOR EACH ROW
BEGIN
    INSERT INTO user_log (user_id, action)
    VALUES (1, CONCAT('UPDATE INGREDIENT '));
END
-- TRIGGER_END