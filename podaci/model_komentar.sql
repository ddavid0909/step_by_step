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
-- Table structure for table `komentar`
--

DROP TABLE IF EXISTS `komentar`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `komentar` (
  `IdKom` int NOT NULL AUTO_INCREMENT,
  `Tekst` varchar(200) NOT NULL,
  `Status` int NOT NULL,
  `Datum` datetime NOT NULL,
  `IdAutor` int DEFAULT NULL,
  `IdKomentarisan` int DEFAULT NULL,
  PRIMARY KEY (`IdKom`),
  KEY `Komentar_id_autor_idx` (`IdAutor`),
  KEY `Komentar_id_komentarisan_idx` (`IdKomentarisan`),
  CONSTRAINT `Komentar_id_autor` FOREIGN KEY (`IdAutor`) REFERENCES `korisnik` (`IdKor`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `Komentar_id_komentarisan` FOREIGN KEY (`IdKomentarisan`) REFERENCES `korisnik` (`IdKor`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `komentar`
--

LOCK TABLES `komentar` WRITE;
/*!40000 ALTER TABLE `komentar` DISABLE KEYS */;
INSERT INTO `komentar` VALUES (2,'Treninzi su veoma efikasni i zanimljivi.',1,'2024-05-21 11:00:00',2,6),(3,'Preporučujem svima, vrhunski profesionalac.',1,'2024-05-22 12:00:00',NULL,7),(4,'Sve pohvale za trud i rad sa klijentima.',1,'2024-05-23 13:00:00',4,8),(7,'Profesionalan pristup i odlična atmosfera.',1,'2024-05-26 16:00:00',NULL,6),(8,'Trener je uvek dostupan za savete i pomoć.',1,'2024-05-27 17:00:00',4,7),(9,'Individualni pristup svakom klijentu, toplo preporučujem.',1,'2024-05-28 18:00:00',1,8),(12,'Teretana je super, a programeri za 40/40!',1,'2024-05-24 17:05:27',2,NULL),(13,'Sve je odlicno.',1,'2024-05-25 15:20:21',2,NULL),(15,'Sve naj',1,'2024-05-26 16:18:47',2,NULL),(18,'Lepo',1,'2024-05-29 13:53:04',4,7),(19,'Pregledno',1,'2024-05-29 13:53:45',4,NULL),(22,'Ksendza zakon',1,'2024-05-31 14:15:10',23,10);
/*!40000 ALTER TABLE `komentar` ENABLE KEYS */;
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
