-- MySQL dump 10.13  Distrib 5.7.24, for osx10.9 (x86_64)
--
-- Host: localhost    Database: PSI model
-- ------------------------------------------------------
-- Server version	8.2.0
DROP DATABASE IF EXISTS `PSI model`;
CREATE DATABASE `PSI model`;
USE `PSI model`;


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Drzi`
--

DROP TABLE IF EXISTS `Drzi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Drzi` (
  `IdDrzi` int NOT NULL AUTO_INCREMENT,
  `IdKor` int NOT NULL,
  `IdTre1` int NOT NULL,
  PRIMARY KEY (`IdDrzi`),
  UNIQUE KEY `ak_drzi` (`IdKor`,`IdTre1`),
  KEY `Trening drzan_idx` (`IdTre1`),
  CONSTRAINT `Korisnik drzi` FOREIGN KEY (`IdKor`) REFERENCES `Korisnik` (`IdKor`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `Trening drzan` FOREIGN KEY (`IdTre1`) REFERENCES `Trening` (`idTre`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Drzi`
--

LOCK TABLES `Drzi` WRITE;
/*!40000 ALTER TABLE `Drzi` DISABLE KEYS */;
/*!40000 ALTER TABLE `Drzi` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Komentar`
--

DROP TABLE IF EXISTS `Komentar`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Komentar` (
  `IdKom` int NOT NULL AUTO_INCREMENT,
  `Tekst` varchar(200) NOT NULL,
  `Status` int NOT NULL,
  `Datum` datetime NOT NULL,
  `IdAutor` int DEFAULT NULL,
  `IdKomentarisan` int NOT NULL,
  PRIMARY KEY (`IdKom`),
  KEY `Komentar_id_autor_idx` (`IdAutor`),
  KEY `Komentar_id_komentarisan_idx` (`IdKomentarisan`),
  CONSTRAINT `Komentar_id_autor` FOREIGN KEY (`IdAutor`) REFERENCES `Korisnik` (`IdKor`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `Komentar_id_komentarisan` FOREIGN KEY (`IdKomentarisan`) REFERENCES `Korisnik` (`IdKor`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Komentar`
--

LOCK TABLES `Komentar` WRITE;
/*!40000 ALTER TABLE `Komentar` DISABLE KEYS */;
/*!40000 ALTER TABLE `Komentar` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Korisnik`
--

DROP TABLE IF EXISTS `Korisnik`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Korisnik` (
  `IdKor` int NOT NULL AUTO_INCREMENT,
  `Mejl` varchar(45) NOT NULL,
  `Uloga` varchar(45) NOT NULL,
  `Sifra` varchar(45) NOT NULL,
  `Slika` blob,
  PRIMARY KEY (`IdKor`),
  UNIQUE KEY `Mejl` (`Mejl`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Korisnik`
--

LOCK TABLES `Korisnik` WRITE;
/*!40000 ALTER TABLE `Korisnik` DISABLE KEYS */;
/*!40000 ALTER TABLE `Korisnik` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Obuhvata`
--

DROP TABLE IF EXISTS `Obuhvata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Obuhvata` (
  `IdObuh` int NOT NULL AUTO_INCREMENT,
  `IdTre` int NOT NULL,
  `IdPak` int NOT NULL,
  PRIMARY KEY (`IdObuh`),
  UNIQUE KEY `ak_obuhvata` (`IdTre`,`IdPak`),
  KEY `Paket Obuhvata_idx` (`IdPak`),
  CONSTRAINT `Obuhvata trening` FOREIGN KEY (`IdTre`) REFERENCES `Trening` (`idTre`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `Paket Obuhvata` FOREIGN KEY (`IdPak`) REFERENCES `Paket` (`IdPak`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Obuhvata`
--

LOCK TABLES `Obuhvata` WRITE;
/*!40000 ALTER TABLE `Obuhvata` DISABLE KEYS */;
/*!40000 ALTER TABLE `Obuhvata` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Paket`
--

DROP TABLE IF EXISTS `Paket`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Paket` (
  `IdPak` int NOT NULL AUTO_INCREMENT,
  `BrTermina` int NOT NULL,
  `Dana` int NOT NULL,
  `Cena` decimal(10,2) NOT NULL,
  `Naziv` varchar(40) NOT NULL,
  PRIMARY KEY (`IdPak`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Paket`
--

LOCK TABLES `Paket` WRITE;
/*!40000 ALTER TABLE `Paket` DISABLE KEYS */;
/*!40000 ALTER TABLE `Paket` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Podrzava`
--

DROP TABLE IF EXISTS `Podrzava`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Podrzava` (
  `IdPodrzava` int NOT NULL AUTO_INCREMENT,
  `IdSala` int NOT NULL,
  `IdTre2` int NOT NULL,
  PRIMARY KEY (`IdPodrzava`),
  UNIQUE KEY `ak_podrzava` (`IdSala`,`IdTre2`),
  KEY `Podrzava trening_idx` (`IdTre2`),
  CONSTRAINT `Podrzava trening` FOREIGN KEY (`IdTre2`) REFERENCES `Trening` (`idTre`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `Sala podrzava` FOREIGN KEY (`IdSala`) REFERENCES `Sala` (`IdSala`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Podrzava`
--

LOCK TABLES `Podrzava` WRITE;
/*!40000 ALTER TABLE `Podrzava` DISABLE KEYS */;
/*!40000 ALTER TABLE `Podrzava` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Pokriva`
--

DROP TABLE IF EXISTS `Pokriva`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Pokriva` (
  `IdPokriva` int NOT NULL AUTO_INCREMENT,
  `IdPre` int NOT NULL,
  `IdTre` int NOT NULL,
  PRIMARY KEY (`IdPokriva`),
  UNIQUE KEY `ak_pokriva` (`IdPre`,`IdTre`),
  KEY `Trening pokriven_idx` (`IdTre`),
  CONSTRAINT `Pretplata pokriva` FOREIGN KEY (`IdPre`) REFERENCES `Pretplata` (`IdPre`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `Trening pokriven` FOREIGN KEY (`IdTre`) REFERENCES `Trening` (`idTre`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Pokriva`
--

LOCK TABLES `Pokriva` WRITE;
/*!40000 ALTER TABLE `Pokriva` DISABLE KEYS */;
/*!40000 ALTER TABLE `Pokriva` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Prati`
--

DROP TABLE IF EXISTS `Prati`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Prati` (
  `IdPrati` int NOT NULL AUTO_INCREMENT,
  `IdKor` int NOT NULL,
  `IdTer` int NOT NULL,
  PRIMARY KEY (`IdPrati`),
  UNIQUE KEY `ak_prati` (`IdKor`,`IdTer`),
  KEY `Prati termin_idx` (`IdTer`),
  CONSTRAINT `Korisnik prati` FOREIGN KEY (`IdKor`) REFERENCES `Korisnik` (`IdKor`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `Prati termin` FOREIGN KEY (`IdTer`) REFERENCES `Termin` (`IdTer`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Prati`
--

LOCK TABLES `Prati` WRITE;
/*!40000 ALTER TABLE `Prati` DISABLE KEYS */;
/*!40000 ALTER TABLE `Prati` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Pretplata`
--

DROP TABLE IF EXISTS `Pretplata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Pretplata` (
  `IdPre` int NOT NULL AUTO_INCREMENT,
  `DatumDo` datetime NOT NULL,
  `PreostaloTermina` int NOT NULL,
  `IdPretplaceni` int NOT NULL,
  PRIMARY KEY (`IdPre`),
  KEY `id_pretplaceni_idx` (`IdPretplaceni`),
  CONSTRAINT `id_pretplaceni` FOREIGN KEY (`IdPretplaceni`) REFERENCES `Korisnik` (`IdKor`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Pretplata`
--

LOCK TABLES `Pretplata` WRITE;
/*!40000 ALTER TABLE `Pretplata` DISABLE KEYS */;
/*!40000 ALTER TABLE `Pretplata` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Sala`
--

DROP TABLE IF EXISTS `Sala`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Sala` (
  `IdSala` int NOT NULL AUTO_INCREMENT,
  `Naziv` varchar(45) NOT NULL,
  PRIMARY KEY (`IdSala`),
  UNIQUE KEY `Naziv` (`Naziv`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Sala`
--

LOCK TABLES `Sala` WRITE;
/*!40000 ALTER TABLE `Sala` DISABLE KEYS */;
/*!40000 ALTER TABLE `Sala` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Termin`
--

DROP TABLE IF EXISTS `Termin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Termin` (
  `IdTer` int NOT NULL AUTO_INCREMENT,
  `Dan` varchar(3) NOT NULL,
  `Pocetak` time NOT NULL,
  `Kraj` time NOT NULL,
  `IdPodrzava` int NOT NULL,
  `IdDrzi` int NOT NULL,
  `Preostalo` int NOT NULL,
  PRIMARY KEY (`IdTer`),
  KEY `Termin podrzava_idx` (`IdPodrzava`),
  KEY `Drzi termin_idx` (`IdDrzi`),
  CONSTRAINT `Drzi termin` FOREIGN KEY (`IdDrzi`) REFERENCES `Drzi` (`IdDrzi`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `Termin podrzava` FOREIGN KEY (`IdPodrzava`) REFERENCES `Podrzava` (`IdPodrzava`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `termin_chk_1` CHECK ((`Dan` in (_utf8mb4'PON',_utf8mb4'UTO',_utf8mb4'SRE',_utf8mb4'CET',_utf8mb4'PET',_utf8mb4'SUB',_utf8mb4'NED')))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Termin`
--

LOCK TABLES `Termin` WRITE;
/*!40000 ALTER TABLE `Termin` DISABLE KEYS */;
/*!40000 ALTER TABLE `Termin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Trening`
--

DROP TABLE IF EXISTS `Trening`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Trening` (
  `idTre` int NOT NULL AUTO_INCREMENT,
  `Tip` varchar(45) NOT NULL,
  PRIMARY KEY (`idTre`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Trening`
--

LOCK TABLES `Trening` WRITE;
/*!40000 ALTER TABLE `Trening` DISABLE KEYS */;
/*!40000 ALTER TABLE `Trening` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-05-02 23:05:08
