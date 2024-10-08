CREATE TABLE `ismi`.`appointments` (
`id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
`id_doctor` INT UNSIGNED NOT NULL,
`id_patient` INT UNSIGNED NOT NULL,
`date` DATETIME NOT NULL,
PRIMARY KEY (`id`),
UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE);

INSERT INTO `ismi`.`appointments`
(`id_doctor`, `id_patient`, `date`)
VALUES
(%s, %s, %s);

UPDATE `ismi`.`appointments`
SET
`id_doctor` = %s,
`id_patient` = %s,
`date` = %s
WHERE `id` = %s;

DELETE FROM `ismi`.`appointments`
WHERE `id` = %s;

SELECT `appointments`.`id`,
    `appointments`.`id_doctor`,
    `appointments`.`id_patient`,
    `appointments`.`date`
FROM `ismi`.`appointments`;
