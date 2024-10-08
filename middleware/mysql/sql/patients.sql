CREATE TABLE `ismi`.`patients` (
`id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
`name` VARCHAR(64) NOT NULL,
`phone` VARCHAR(16) NOT NULL,
`sex` TINYINT NOT NULL,
`weight` FLOAT NULL,
`height` FLOAT NULL,
PRIMARY KEY (`id`),
UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
UNIQUE INDEX `phone_UNIQUE` (`phone` ASC) VISIBLE);

INSERT INTO `ismi`.`patients`
(`name`, `phone`, `sex`, `weight`, `height`)
VALUES
(%s, %s, %s, %s, %s);

UPDATE `ismi`.`patients`
SET
`name` = %s,
`phone` = %s,
`sex` = %s,
`weight` = %s,
`height` = %s
WHERE `id` = %s;

DELETE FROM `ismi`.`patients`
WHERE `id`=%s;

SELECT `patients`.`id`,
    `patients`.`name`,
    `patients`.`phone`,
    `patients`.`sex`,
    `patients`.`weight`,
    `patients`.`height`
FROM `ismi`.`patients`;
