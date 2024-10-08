CREATE TABLE `ismi`.`medical_records` (
`id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
`id_patient` INT UNSIGNED NOT NULL,
`diagnosis` VARCHAR(64) NULL,
PRIMARY KEY (`id`),
UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE);

INSERT INTO `ismi`.`medical_records`
(`id_patient`, `diagnosis`)
VALUES
(%s, %s);

UPDATE `ismi`.`medical_records`
SET
`id_patient` = %s,
`diagnosis` = %s
WHERE `id` = %s;

DELETE FROM `ismi`.`medical_records`
WHERE `id` = %s;

SELECT `medical_records`.`id`,
    `medical_records`.`id_patient`,
    `medical_records`.`diagnosis`
FROM `ismi`.`medical_records`;
