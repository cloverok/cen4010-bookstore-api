-- -----------------------------------------------------
-- Schema library
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `geekText` DEFAULT CHARACTER SET utf8;

-- -----------------------------------------------------
-- Profile Management
-- -----------------------------------------------------
-- Table profile
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `profile` (
  `uid`      INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `name`     VARCHAR(45) NULL,
  `email`    VARCHAR(45) NULL,
  `address`  VARCHAR(255) NULL,
  PRIMARY KEY (`uid`),
  UNIQUE INDEX `username_UNIQUE` (`username` ASC) VISIBLE
);
-- -----------------------------------------------------
-- Table creditCard
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `creditCard` (
  `card_number` CHAR(16) NOT NULL,
  `uid`         INT NOT NULL,
  `expiration`  DATE NOT NULL,
  `cvv`         CHAR(3) NOT NULL,
  PRIMARY KEY (`card_number`),
  UNIQUE INDEX `cid_UNIQUE` (`card_number` ASC) VISIBLE,
  CONSTRAINT `uid`
    FOREIGN KEY (`uid`) REFERENCES `profile` (`uid`)
     ON DELETE NO ACTION 
     ON UPDATE NO ACTION
);

INSERT INTO `profile` (`username`, `password`, `name`, `email`, `address`)
 VALUES ('bJohns', 'qwert123!', 'Ben Johns', 'bjohns@example.com', '123 Main St');

INSERT INTO `profile` (`username`, `password`, `name`, `email`, `address`)
 VALUES ('tJefferson', 'Winter1!', 'Thomas Jefferson', 'tjefferson@example.com', '456 Oak Ave');

INSERT INTO `creditCard` (`card_number`, `uid`, `expiration`, `cvv`)
 VALUES ('1234567812345678', 1, '2025-12-31', '123');
