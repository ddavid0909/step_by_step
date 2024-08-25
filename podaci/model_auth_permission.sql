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
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=73 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add drzi',7,'add_drzi'),(26,'Can change drzi',7,'change_drzi'),(27,'Can delete drzi',7,'delete_drzi'),(28,'Can view drzi',7,'view_drzi'),(29,'Can add komentar',8,'add_komentar'),(30,'Can change komentar',8,'change_komentar'),(31,'Can delete komentar',8,'delete_komentar'),(32,'Can view komentar',8,'view_komentar'),(33,'Can add korisnik',9,'add_korisnik'),(34,'Can change korisnik',9,'change_korisnik'),(35,'Can delete korisnik',9,'delete_korisnik'),(36,'Can view korisnik',9,'view_korisnik'),(37,'Can add obuhvata',10,'add_obuhvata'),(38,'Can change obuhvata',10,'change_obuhvata'),(39,'Can delete obuhvata',10,'delete_obuhvata'),(40,'Can view obuhvata',10,'view_obuhvata'),(41,'Can add paket',11,'add_paket'),(42,'Can change paket',11,'change_paket'),(43,'Can delete paket',11,'delete_paket'),(44,'Can view paket',11,'view_paket'),(45,'Can add podrzava',12,'add_podrzava'),(46,'Can change podrzava',12,'change_podrzava'),(47,'Can delete podrzava',12,'delete_podrzava'),(48,'Can view podrzava',12,'view_podrzava'),(49,'Can add pokriva',13,'add_pokriva'),(50,'Can change pokriva',13,'change_pokriva'),(51,'Can delete pokriva',13,'delete_pokriva'),(52,'Can view pokriva',13,'view_pokriva'),(53,'Can add prati',14,'add_prati'),(54,'Can change prati',14,'change_prati'),(55,'Can delete prati',14,'delete_prati'),(56,'Can view prati',14,'view_prati'),(57,'Can add pretplata',15,'add_pretplata'),(58,'Can change pretplata',15,'change_pretplata'),(59,'Can delete pretplata',15,'delete_pretplata'),(60,'Can view pretplata',15,'view_pretplata'),(61,'Can add sala',16,'add_sala'),(62,'Can change sala',16,'change_sala'),(63,'Can delete sala',16,'delete_sala'),(64,'Can view sala',16,'view_sala'),(65,'Can add termin',17,'add_termin'),(66,'Can change termin',17,'change_termin'),(67,'Can delete termin',17,'delete_termin'),(68,'Can view termin',17,'view_termin'),(69,'Can add trening',18,'add_trening'),(70,'Can change trening',18,'change_trening'),(71,'Can delete trening',18,'delete_trening'),(72,'Can view trening',18,'view_trening');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-05-31 22:03:45
