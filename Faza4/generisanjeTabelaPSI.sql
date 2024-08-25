DROP SCHEMA IF EXISTS `PSI model`;
CREATE SCHEMA `PSI model`;

CREATE TABLE `PSI model`.`Korisnik` (
  `IdKor` INT NOT NULL AUTO_INCREMENT,
  `Mejl` VARCHAR(45) UNIQUE NOT NULL,
  `Uloga` VARCHAR(45) NOT NULL,
  `Sifra` VARCHAR(45) NOT NULL,
  `Slika` BLOB NULL,
  PRIMARY KEY (`IdKor`));

CREATE TABLE `PSI model`.`Komentar` (
  `IdKom` INT NOT NULL AUTO_INCREMENT,
  `Tekst` VARCHAR(200) NOT NULL,
  `Status` INT NOT NULL,
  `Datum` DATETIME NOT NULL,
  `IdAutor` INT NULL,
  `IdKomentarisan` INT NOT NULL,
  PRIMARY KEY (`IdKom`),
  INDEX `Komentar_id_autor_idx` (`IdAutor` ASC) VISIBLE,
  INDEX `Komentar_id_komentarisan_idx` (`IdKomentarisan` ASC) VISIBLE,
  CONSTRAINT `Komentar_id_autor`
    FOREIGN KEY (`IdAutor`)
    REFERENCES `PSI model`.`Korisnik` (`IdKor`)
    ON DELETE SET NULL
    ON UPDATE CASCADE,
  CONSTRAINT `Komentar_id_komentarisan`
    FOREIGN KEY (`IdKomentarisan`)
    REFERENCES `PSI model`.`Korisnik` (`IdKor`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);

CREATE TABLE `PSI model`.`Pretplata` (
  `IdPre` INT NOT NULL AUTO_INCREMENT,
  `DatumDo` DATETIME NOT NULL,
  `PreostaloTermina` INT NOT NULL,
  `IdPretplaceni` INT NOT NULL,
  PRIMARY KEY (`IdPre`),
  INDEX `id_pretplaceni_idx` (`IdPretplaceni` ASC) VISIBLE,
  CONSTRAINT `id_pretplaceni`
    FOREIGN KEY (`IdPretplaceni`)
    REFERENCES `PSI model`.`Korisnik` (`IdKor`)
    ON DELETE NO ACTION
    ON UPDATE CASCADE);

CREATE TABLE `PSI model`.`Paket` (
  `IdPak` INT NOT NULL AUTO_INCREMENT,
  `BrTermina` INT NOT NULL,
  `Dana` INT NOT NULL,
  `Cena` DECIMAL(10,2) NOT NULL,
  `Naziv` VARCHAR(40) NOT NULL,
  PRIMARY KEY (`IdPak`));

CREATE TABLE `PSI model`.`Sala` (
  `IdSala` INT NOT NULL AUTO_INCREMENT,
  `Naziv` VARCHAR(45) UNIQUE NOT NULL,
  PRIMARY KEY (`IdSala`));

CREATE TABLE `PSI model`.`Trening` (
  `idTre` INT NOT NULL AUTO_INCREMENT,
  `Tip` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idTre`));

CREATE TABLE `PSI model`.`Obuhvata` (
  `IdTre` INT NOT NULL,
  `IdPak` INT NOT NULL,
  PRIMARY KEY (`IdTre`, `IdPak`),
  INDEX `Paket Obuhvata_idx` (`IdPak` ASC) VISIBLE,
  CONSTRAINT `Paket Obuhvata`
    FOREIGN KEY (`IdPak`)
    REFERENCES `PSI model`.`Paket` (`IdPak`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `Obuhvata trening`
    FOREIGN KEY (`IdTre`)
    REFERENCES `PSI model`.`Trening` (`IdTre`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);

CREATE TABLE `PSI model`.`Pokriva` (
  `IdPre` INT NOT NULL,
  `IdTre` INT NOT NULL,
  PRIMARY KEY (`IdPre`, `IdTre`),
  INDEX `Trening pokriven_idx` (`IdTre` ASC) VISIBLE,
  CONSTRAINT `Pretplata pokriva`
    FOREIGN KEY (`IdPre`)
    REFERENCES `PSI model`.`Pretplata` (`IdPre`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `Trening pokriven`
    FOREIGN KEY (`IdTre`)
    REFERENCES `PSI model`.`Trening` (`IdTre`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);

CREATE TABLE `PSI model`.`Drzi` (
  `IdKor` INT NOT NULL,
  `IdTre1` INT NOT NULL,
  PRIMARY KEY (`IdKor`, `IdTre1`),
  INDEX `Trening drzan_idx` (`IdTre1` ASC) VISIBLE,
  CONSTRAINT `Korisnik drzi`
    FOREIGN KEY (`IdKor`)
    REFERENCES `PSI model`.`Korisnik` (`IdKor`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `Trening drzan`
    FOREIGN KEY (`IdTre1`)
    REFERENCES `PSI model`.`Trening` (`IdTre`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);

CREATE TABLE `PSI model`.`Podrzava` (
  `IdSala` INT NOT NULL,
  `IdTre2` INT NOT NULL,
  PRIMARY KEY (`IdSala`, `IdTre2`),
  INDEX `Podrzava trening_idx` (`IdTre2` ASC) VISIBLE,
  CONSTRAINT `Sala podrzava`
    FOREIGN KEY (`IdSala`)
    REFERENCES `PSI model`.`Sala` (`IdSala`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `Podrzava trening`
    FOREIGN KEY (`IdTre2`)
    REFERENCES `PSI model`.`Trening` (`IdTre`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);

CREATE TABLE `PSI model`.`Termin` (
  `IdTer` INT NOT NULL AUTO_INCREMENT,
  `Dan` VARCHAR(3) NOT NULL CHECK (Dan = 'PON' OR Dan = 'UTO' OR Dan = 'SRE' OR Dan = 'CET' OR Dan = 'PET' OR Dan = 'SUB' OR Dan = 'NED'),
  `Pocetak` TIME NOT NULL,
  `Kraj` TIME NOT NULL,
  `IdSala` INT NOT NULL,
  `IdTre2` INT NOT NULL,
  `IdKor` INT NOT NULL,
  `IdTre1` INT NOT NULL,
  `Preostalo` INT NOT NULL,
  PRIMARY KEY (`IdTer`),
  INDEX `Termin podrzava_idx` (`IdTre2` ASC, `IdSala` ASC) VISIBLE,
  INDEX `Drzi termin_idx` (`IdTre1` ASC, `IdKor` ASC) VISIBLE,
  CONSTRAINT `Termin podrzava`
    FOREIGN KEY (`IdTre2` , `IdSala`)
    REFERENCES `PSI model`.`Podrzava` (`IdTre2` , `IdSala`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `Drzi termin`
    FOREIGN KEY (`IdTre1` , `IdKor`)
    REFERENCES `PSI model`.`Drzi` (`IdTre1` , `IdKor`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);

CREATE TABLE `PSI model`.`Prati` (
  `IdKor` INT NOT NULL,
  `IdTer` INT NOT NULL,
  PRIMARY KEY (`IdKor`, `IdTer`),
  INDEX `Prati termin_idx` (`IdTer` ASC) VISIBLE,
  CONSTRAINT `Prati termin`
    FOREIGN KEY (`IdTer`)
    REFERENCES `PSI model`.`Termin` (`IdTer`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `Korisnik prati`
    FOREIGN KEY (`IdKor`)
    REFERENCES `PSI model`.`Korisnik` (`IdKor`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);