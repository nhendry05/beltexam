-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema thoughts_wall
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `thoughts_wall` ;

-- -----------------------------------------------------
-- Schema thoughts_wall
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `thoughts_wall` DEFAULT CHARACTER SET utf8 ;
USE `thoughts_wall` ;

-- -----------------------------------------------------
-- Table `thoughts_wall`.`users`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `thoughts_wall`.`users` ;

CREATE TABLE IF NOT EXISTS `thoughts_wall`.`users` (
  `user_id` INT(11) NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NULL DEFAULT NULL,
  `last_name` VARCHAR(45) NULL DEFAULT NULL,
  `email` VARCHAR(45) NULL DEFAULT NULL,
  `password` VARCHAR(255) NULL DEFAULT NULL,
  `created_at` DATETIME NULL DEFAULT NULL,
  `updated_at` DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (`user_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 2
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `thoughts_wall`.`thoughts`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `thoughts_wall`.`thoughts` ;

CREATE TABLE IF NOT EXISTS `thoughts_wall`.`thoughts` (
  `thought_id` INT NOT NULL AUTO_INCREMENT,
  `content` TEXT NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  `author` INT NOT NULL,
  PRIMARY KEY (`thought_id`),
  INDEX `fk_thoughts_users_idx` (`author` ASC) VISIBLE,
  CONSTRAINT `fk_thoughts_users`
    FOREIGN KEY (`author`)
    REFERENCES `thoughts_wall`.`users` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `thoughts_wall`.`likes`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `thoughts_wall`.`likes` ;

CREATE TABLE IF NOT EXISTS `thoughts_wall`.`likes` (
  `thought_like` INT NOT NULL,
  `user_like` INT NOT NULL,
  PRIMARY KEY (`thought_like`, `user_like`),
  INDEX `fk_thoughts_has_users_users1_idx` (`user_like` ASC) VISIBLE,
  INDEX `fk_thoughts_has_users_thoughts1_idx` (`thought_like` ASC) VISIBLE,
  CONSTRAINT `fk_thoughts_has_users_thoughts1`
    FOREIGN KEY (`thought_like`)
    REFERENCES `thoughts_wall`.`thoughts` (`thought_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_thoughts_has_users_users1`
    FOREIGN KEY (`user_like`)
    REFERENCES `thoughts_wall`.`users` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
