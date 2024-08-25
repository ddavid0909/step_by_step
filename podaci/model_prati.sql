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
-- Table structure for table `prati`
--

DROP TABLE IF EXISTS `prati`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `prati` (
  `IdPrati` int NOT NULL AUTO_INCREMENT,
  `IdKor` int NOT NULL,
  `IdTer` int NOT NULL,
  PRIMARY KEY (`IdPrati`),
  UNIQUE KEY `ak_prati` (`IdKor`,`IdTer`),
  KEY `Prati termin_idx` (`IdTer`),
  CONSTRAINT `Korisnik prati` FOREIGN KEY (`IdKor`) REFERENCES `korisnik` (`IdKor`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `Prati termin` FOREIGN KEY (`IdTer`) REFERENCES `termin` (`IdTer`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=109 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `prati`
--

LOCK TABLES `prati` WRITE;
/*!40000 ALTER TABLE `prati` DISABLE KEYS */;
INSERT INTO `prati` VALUES (85,2,10),(92,2,16),(102,2,20),(104,2,29),(86,2,31),(93,2,32),(106,2,33),(29,4,1),(84,4,2),(39,4,7),(71,19,10),(76,19,16),(70,19,19),(97,19,33),(107,19,37),(100,20,2),(101,20,35),(105,23,2);
/*!40000 ALTER TABLE `prati` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-05-31 22:03:46
