USE bookstore;

-- =================================================================
-- Profile Management Tables & Sample Data
-- =================================================================
CREATE TABLE IF NOT EXISTS `profile` (
    `uid`      INT          NOT NULL AUTO_INCREMENT,
    `username` VARCHAR(45)  NOT NULL,
    `password` VARCHAR(255) NOT NULL,
    `name`     VARCHAR(45)  NULL,
    `email`    VARCHAR(45)  NULL,
    PRIMARY KEY (`uid`),
    UNIQUE INDEX `username_UNIQUE` (`username` ASC)
);

CREATE TABLE IF NOT EXISTS `creditCard` (
    `card_number` CHAR(16) NOT NULL,
    `uid`         INT      NOT NULL,
    `expiration`  DATE     NOT NULL,
    `cvv`         CHAR(3)  NOT NULL,
    PRIMARY KEY (`card_number`),
    UNIQUE INDEX `cid_UNIQUE` (`card_number` ASC),
    UNIQUE INDEX `uid_UNIQUE` (`uid` ASC),
    CONSTRAINT `fk_uid`
        FOREIGN KEY (`uid`) REFERENCES `profile` (`uid`)
            ON DELETE NO ACTION ON UPDATE NO ACTION
);

INSERT INTO `profile` (`username`, `password`, `name`, `email`)
VALUES
    ('bJohns',     'qwert123!', 'Ben Johns',        'bjohns@fiu.com'),
    ('tJefferson', 'Winter1!',  'Thomas Jefferson',  'tjefferson@example.com'),
    ('twoods',     'golf_fan1#','Tiger Woods',        'twoods@pga.com');
    
INSERT INTO `creditCard` (`card_number`, `uid`, `expiration`, `cvv`)
VALUES
    ('4111111111111111', 1, '2027-04-30', '123'),
    ('5500000000000004', 2, '2026-11-30', '456'),
    ('340000000000009',  3, '2028-01-31', '789');

-- =================================================================
-- ToDo Tables & Sample Data
-- =================================================================
