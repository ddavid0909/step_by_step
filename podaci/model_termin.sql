-- MySQL dump 10.13  Distrib 8.0.34, for macos13 (x86_64)
--
-- Host: 127.0.0.1    Database: model
-- ------------------------------------------------------
-- Server version	8.2.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `termin`
--

DROP TABLE IF EXISTS `termin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `termin` (
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
  CONSTRAINT `Drzi termin` FOREIGN KEY (`IdDrzi`) REFERENCES `drzi` (`IdDrzi`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `Termin podrzava` FOREIGN KEY (`IdPodrzava`) REFERENCES `podrzava` (`IdPodrzava`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `termin_chk_1` CHECK ((`Dan` in (_utf8mb4'PON',_utf8mb4'UTO',_utf8mb4'SRE',_utf8mb4'CET',_utf8mb4'PET',_utf8mb4'SUB',_utf8mb4'NED')))
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `termin`
--

LOCK TABLES `termin` WRITE;
/*!40000 ALTER TABLE `termin` DISABLE KEYS */;
INSERT INTO `termin` VALUES (1,'PON','08:00:00','09:00:00',1,1,8),(2,'UTO','09:00:00','10:00:00',2,8,8),(7,'UTO','13:00:00','14:00:00',1,7,9),(10,'PET','13:00:00','14:00:00',4,3,4),(16,'UTO','15:40:00','16:40:00',4,3,3),(19,'PET','12:00:00','13:00:00',4,3,4),(20,'CET','09:00:00','12:00:00',4,3,5),(23,'SUB','12:00:00','13:00:00',3,11,5),(29,'CET','13:30:00','15:30:00',3,11,4),(30,'NED','11:00:00','13:00:00',1,7,9),(31,'PON','12:00:00','14:00:00',4,3,4),(32,'NED','12:00:00','14:00:00',4,3,6),(33,'SRE','12:30:00','14:30:00',4,3,8),(34,'PON','17:16:00','18:16:00',4,3,17),(35,'SUB','13:00:00','16:00:00',2,8,8),(36,'SRE','15:00:00','16:00:00',8,3,10),(37,'PET','12:30:00','14:40:00',6,47,4);
/*!40000 ALTER TABLE `termin` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-05-31 22:03:48
