USE bookstore;

-- =================================================================
-- Profile Management Tables & Sample Data
-- Owner: Ben
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
-- Shared Books Table
-- =================================================================
CREATE TABLE IF NOT EXISTS `books` (
    `book_id` INT           NOT NULL AUTO_INCREMENT,
    `title`   VARCHAR(255)  NOT NULL,
    `author`  VARCHAR(255)  NULL,
    `price`   DECIMAL(6,2)  NOT NULL,
    PRIMARY KEY (`book_id`)
);

INSERT INTO `books` (`title`, `author`, `price`)
VALUES
    ('The Hobbit', 'J.R.R. Tolkien', 14.99),
    ('1984', 'George Orwell', 12.50),
    ('Dune', 'Frank Herbert', 18.00);

-- =================================================================
-- Shopping Cart Tables & Sample Data
-- Owner: Clive
-- =================================================================
CREATE TABLE IF NOT EXISTS `cart_items` (
    `id`       INT NOT NULL AUTO_INCREMENT,
    `uid`      INT NOT NULL,
    `book_id`  INT NOT NULL,
    `quantity` INT NOT NULL DEFAULT 1,
    PRIMARY KEY (`id`),
    CONSTRAINT `fk_cart_uid`
        FOREIGN KEY (`uid`) REFERENCES `profile` (`uid`),
    CONSTRAINT `fk_cart_book`
        FOREIGN KEY (`book_id`) REFERENCES `books` (`book_id`)
);

INSERT INTO `cart_items` (`uid`, `book_id`, `quantity`)
VALUES
    (1, 1, 2),
    (1, 2, 1),
    (2, 3, 1);

-- =================================================================
-- Wishlist Management Tables & Sample Data
-- Owner: Daniela Martinez
-- =================================================================
CREATE TABLE IF NOT EXISTS `wishlist` (
    `wishlist_id` INT NOT NULL AUTO_INCREMENT,
    `uid` INT NOT NULL,
    `wishlist_name` VARCHAR(100) NOT NULL,
    PRIMARY KEY (`wishlist_id`),
    CONSTRAINT `fk_wishlist_profile`
        FOREIGN KEY (`uid`)
        REFERENCES `profile` (`uid`)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS `wishlist_item` (
    `wishlist_item_id` INT NOT NULL AUTO_INCREMENT,
    `wishlist_id` INT NOT NULL,
    `book_id` INT NOT NULL,
    PRIMARY KEY (`wishlist_item_id`),
    UNIQUE INDEX `wishlist_book_UNIQUE` (`wishlist_id`, `book_id`),
    CONSTRAINT `fk_wishlist_item_wishlist`
        FOREIGN KEY (`wishlist_id`)
        REFERENCES `wishlist` (`wishlist_id`)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT `fk_wishlist_item_book`
        FOREIGN KEY (`book_id`)
        REFERENCES `books` (`book_id`)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

INSERT IGNORE INTO `wishlist`
    (`wishlist_id`, `uid`, `wishlist_name`)
VALUES
    (1, 1, 'Favorites');