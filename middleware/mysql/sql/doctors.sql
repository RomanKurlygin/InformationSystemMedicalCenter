CREATE TABLE `ismi`.`doctors` (
`id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
`name` VARCHAR(64) NOT NULL,
`job` VARCHAR(64) NOT NULL,
`wage` INT UNSIGNED ZEROFILL NOT NULL,
`phone` VARCHAR(16) NULL,
PRIMARY KEY (`id`),
UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
UNIQUE INDEX `phone_UNIQUE` (`phone` ASC) VISIBLE);

INSERT INTO `ismi`.`doctors`
(`name`, `job`, `wage`, `phone`)
VALUES
(%s, %s, %s, %s);

UPDATE `ismi`.`doctors`
SET
`name` = %s,
`job` = %s,
`wage` = %s,
`phone` = %s
WHERE `id` = %s;

DELETE FROM `ismi`.`doctors`
WHERE `id`=%s;

SELECT `doctors`.`id`,
    `doctors`.`name`,
    `doctors`.`job`,
    `doctors`.`wage`,
    `doctors`.`phone`
FROM `ismi`.`doctors`;
