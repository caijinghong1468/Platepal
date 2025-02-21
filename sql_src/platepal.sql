DROP SCHEMA platepal;
CREATE DATABASE  IF NOT EXISTS `platepal` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `platepal`;
-- MySQL dump 10.13  Distrib 8.0.40, for macos14 (arm64)
--
-- Host: 127.0.0.1    Database: platepal
-- ------------------------------------------------------
-- Server version	9.0.1

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
-- Table structure for table `FOOD`
--

DROP TABLE IF EXISTS `FOOD`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `FOOD` (
  `FoodID` int NOT NULL AUTO_INCREMENT,
  `Fat` float DEFAULT NULL,
  `Protein` float DEFAULT NULL,
  `Starch` float DEFAULT NULL,
  `Calories` float DEFAULT NULL,
  `FName` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`FoodID`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `FOOD`
--

LOCK TABLES `FOOD` WRITE;
/*!40000 ALTER TABLE `FOOD` DISABLE KEYS */;
INSERT INTO `FOOD` VALUES (1,10,20,30,400,'蚵仔麵線'),(2,5,15,25,300,'香菜豬血糕'),(3,8,18,28,350,'鹹酥雞'),(4,3,10,20,250,'臭豆腐');
/*!40000 ALTER TABLE `FOOD` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `GROUP_LEADER`
--

DROP TABLE IF EXISTS `GROUP_LEADER`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `GROUP_LEADER` (
  `GroupID` int NOT NULL AUTO_INCREMENT,
  `Leader` int NOT NULL,
  `GName` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`GroupID`),
  KEY `Leader` (`Leader`),
  CONSTRAINT `group_leader_ibfk_1` FOREIGN KEY (`Leader`) REFERENCES `USERS` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `GROUP_LEADER`
--

LOCK TABLES `GROUP_LEADER` WRITE;
/*!40000 ALTER TABLE `GROUP_LEADER` DISABLE KEYS */;
INSERT INTO `GROUP_LEADER` VALUES (1,1,'健身小隊'),(2,2,'減肥小隊'),(3,1,'明星小隊');
/*!40000 ALTER TABLE `GROUP_LEADER` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `GROUP_MEMBER`
--

DROP TABLE IF EXISTS `GROUP_MEMBER`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `GROUP_MEMBER` (
  `M_GroupID` int NOT NULL,
  `Members` int NOT NULL,
  PRIMARY KEY (`M_GroupID`,`Members`),
  KEY `Members` (`Members`),
  CONSTRAINT `group_member_ibfk_1` FOREIGN KEY (`M_GroupID`) REFERENCES `GROUP_LEADER` (`GroupID`) ON DELETE CASCADE,
  CONSTRAINT `group_member_ibfk_2` FOREIGN KEY (`Members`) REFERENCES `USERS` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `GROUP_MEMBER`
--

LOCK TABLES `GROUP_MEMBER` WRITE;
/*!40000 ALTER TABLE `GROUP_MEMBER` DISABLE KEYS */;
INSERT INTO `GROUP_MEMBER` VALUES (1,2),(3,2),(1,3),(3,3),(2,4);
/*!40000 ALTER TABLE `GROUP_MEMBER` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `MEAL`
--

DROP TABLE IF EXISTS `MEAL`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `MEAL` (
  `MealID` int NOT NULL,
  `UID` int NOT NULL,
  `Dates` date DEFAULT NULL,
  `Times` time DEFAULT NULL,
  `Category` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`UID`,`MealID`),
  CONSTRAINT `meal_ibfk_1` FOREIGN KEY (`UID`) REFERENCES `USERS` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MEAL`
--

LOCK TABLES `MEAL` WRITE;
/*!40000 ALTER TABLE `MEAL` DISABLE KEYS */;
INSERT INTO `MEAL` VALUES (1,1,'2024-12-22','08:00:00','Breakfast'),(2,1,'2024-12-22','12:00:00','Lunch'),(3,1,'2024-12-25','08:00:00','Breakfast'),(4,1,'2024-12-25','12:00:00','Lunch'),(1,2,'2024-12-22','09:00:00','Breakfast'),(2,2,'2024-12-22','13:00:00','Lunch'),(3,2,'2024-12-25','09:00:00','Breakfast'),(4,2,'2024-12-25','13:00:00','Lunch');
/*!40000 ALTER TABLE `MEAL` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `MEAL_FOOD`
--

DROP TABLE IF EXISTS `MEAL_FOOD`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `MEAL_FOOD` (
  `FoodID` int NOT NULL,
  `MealID` int NOT NULL,
  `UID` int NOT NULL,
  `Count` int DEFAULT NULL,
  PRIMARY KEY (`FoodID`,`MealID`,`UID`),
  KEY `UID` (`UID`,`MealID`),
  CONSTRAINT `meal_food_ibfk_1` FOREIGN KEY (`UID`, `MealID`) REFERENCES `MEAL` (`UID`, `MealID`),
  CONSTRAINT `meal_food_ibfk_2` FOREIGN KEY (`FoodID`) REFERENCES `FOOD` (`FoodID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MEAL_FOOD`
--

LOCK TABLES `MEAL_FOOD` WRITE;
/*!40000 ALTER TABLE `MEAL_FOOD` DISABLE KEYS */;
INSERT INTO `MEAL_FOOD` VALUES (1,1,1,3),(1,3,1,3),(2,2,2,1),(2,3,1,1),(3,1,2,1),(3,3,2,1),(3,4,1,2),(3,4,2,1),(4,2,1,1);
/*!40000 ALTER TABLE `MEAL_FOOD` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `USER_GOAL`
--

DROP TABLE IF EXISTS `USER_GOAL`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `USER_GOAL` (
  `U_GoalID` int NOT NULL AUTO_INCREMENT,
  `UID` int NOT NULL,
  `Fat` float DEFAULT NULL,
  `Protein` float DEFAULT NULL,
  `Starch` float DEFAULT NULL,
  `S_DATE` date DEFAULT NULL,
  `E_DATE` date DEFAULT NULL,
  PRIMARY KEY (`U_GoalID`),
  KEY `UID` (`UID`),
  CONSTRAINT `user_goal_ibfk_1` FOREIGN KEY (`UID`) REFERENCES `USERS` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `USER_GOAL`
--

LOCK TABLES `USER_GOAL` WRITE;
/*!40000 ALTER TABLE `USER_GOAL` DISABLE KEYS */;
INSERT INTO `USER_GOAL` VALUES (1,1,70,80,120,'2024-12-22','2024-12-24'),(2,2,60,70,100,'2024-12-20','2024-12-24');
/*!40000 ALTER TABLE `USER_GOAL` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `USERS`
--

DROP TABLE IF EXISTS `USERS`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `USERS` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `UName` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `Gender` enum('M','F') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `Age` int DEFAULT NULL,
  `Height` float DEFAULT NULL,
  `Weight` float DEFAULT NULL,
  `Account` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `Password` int DEFAULT NULL,
  `Activity_level` int DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `USERS`
--

LOCK TABLES `USERS` WRITE;
/*!40000 ALTER TABLE `USERS` DISABLE KEYS */;
INSERT INTO `USERS` VALUES (1,'Jay Chou','M',45,173,60,'JayChou',123,0),(2,'Karina','F',28,168.1,45,'Karina',456,2),(3,'Tom Cruise','M',62,170,68,'TomCruise',789,4),(4,'Taylor Swift','F',35,180,54,'TaylorSwift',111,6);
/*!40000 ALTER TABLE `USERS` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-01-03 11:54:03
