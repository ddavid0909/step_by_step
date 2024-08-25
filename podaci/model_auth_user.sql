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
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$720000$4INLd1r13ZxlrKAV36qQLe$nrJIP4TapL91+ejhT1O/4DgljvqCTfVaz3d8t1ojOUw=','2024-05-31 19:43:35.377702',1,'admin','','','',1,1,'2024-05-21 11:07:51.165629'),(2,'pbkdf2_sha256$720000$HDHisbvPORGHHgZzGkfTMK$I7cczzGML9EuXzeIKDb6G6tfmdG53RDOK43lyKpw8OE=','2024-05-31 19:46:37.382411',0,'kk210270d@student.etf.bg.ac.rs','','','',0,1,'2024-05-21 11:31:37.181326'),(3,'pbkdf2_sha256$720000$NKuOlW9pnFlNjZyLqfKPAi$avJT5Yl3IKnG9oAcmtEaMb5Qm9Y4QRxsX9exUlO5bk4=','2024-05-31 19:46:19.677622',0,'dd210102d@student.etf.bg.ac.rs','','','',0,1,'2024-05-21 12:25:54.669238'),(5,'pbkdf2_sha256$720000$7QM4GrcFsNdaEhLLi9EQcZ$zAOqwJ/jC6hTQqYddYPdUgXsLOp8UwqA0eFgNXRnFn0=','2024-05-29 13:51:43.203329',0,'ca210066d@student.etf.bg.ac.rs','','','',0,1,'2024-05-21 12:39:52.494759'),(6,'pbkdf2_sha256$720000$87f92anHblvdNkse0rDEiX$whl+QFqhB6h17oQ+yOm0IOTSDW+PDKItqlaOjrhqdeU=','2024-05-31 19:50:26.174655',0,'Danko','','','',0,1,'2024-05-21 13:20:59.451256'),(7,'pbkdf2_sha256$720000$YWnW1yAg5NA6s6tIqFQvpF$YLA6aLlq14+hyBsqKo9/epG6qR8ERWE9fn7SwiPZ8eA=','2024-05-25 18:12:09.736009',0,'Sara','','','',0,1,'2024-05-21 13:31:31.653614'),(8,'pbkdf2_sha256$720000$IpuJccBA5dpzTA5jOGW1Ia$Tn67e8pJBZ9Njgk2O5oc8h4JXQbSmx3YOaHjSHUTH2c=',NULL,0,'Milena','','','',0,1,'2024-05-21 19:57:23.236367'),(10,'pbkdf2_sha256$720000$V173hsM8AO17rDT0tbcYZo$gqPp2y6eXNGGTGWSQLhtYNyTE/UUFO2UDGe0KCjYHqM=','2024-05-31 13:10:19.649619',0,'Ksenija','','','',0,1,'2024-05-21 20:00:58.853494'),(11,'pbkdf2_sha256$720000$ZkuNtctGegSmHXa7pp85bW$qUELcmjMvEo5ph1k/gzSHDwR+U2CbeL4KCffNdwuUio=','2024-05-25 15:24:45.436529',0,'Sergej','','','',0,1,'2024-05-25 15:23:30.613113'),(15,'pbkdf2_sha256$720000$UKEvmNpvw93ORAhRQqn1Q2$wzaXSAlXX4yJsJJWb70lysA3UnZ5JZk1VWjI84TgkYg=','2024-05-28 10:18:40.329315',0,'Janko','','','',0,1,'2024-05-27 10:29:06.501105'),(18,'pbkdf2_sha256$720000$Hca0i6P8LvJoKmkYunNmks$AptpXc5YFPqcf/pBzZu2+ktwasn7XdtB01EMmzYrNoo=','2024-05-31 19:45:53.197874',0,'se210332d@student.etf.bg.ac.rs','','','',0,1,'2024-05-29 09:57:41.087788'),(19,'pbkdf2_sha256$720000$JnYPIR3amcEqxfhgCobIMH$kmnp5nDYssCy8mEqWBF/R8AQsA4FwfAhTl0Q1LOCTYw=','2024-05-31 13:09:23.441292',0,'ms210486d@student.etf.bg.ac.rs','','','',0,1,'2024-05-31 12:41:27.917680'),(22,'pbkdf2_sha256$720000$zCdOzSzr1qRdNjWLOPpkZK$4LqUil+jLNu/21v2vVgFD9RXaqI5pN37ecplQWWlyYw=','2024-05-31 14:16:09.697644',0,'rt210214d@student.etf.bg.ac.rs','','','',0,1,'2024-05-31 14:13:09.143923'),(23,'pbkdf2_sha256$720000$G1GyMuOngAZVDIQpFPochN$ixbmizOpVYe0uVDf3Ph1ldvULFbKtu6ckh/Qz7/uZ2k=','2024-05-31 19:46:59.935789',0,'Ivan','','','',0,1,'2024-05-31 19:44:36.972929');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
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
