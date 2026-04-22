-- MySQL dump 10.13  Distrib 8.4.7, for Win64 (x86_64)
--
-- Host: localhost    Database: smartspend
-- ------------------------------------------------------
-- Server version	8.4.7

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `billing_details`
--

DROP TABLE IF EXISTS `billing_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `billing_details` (
  `user_id` int NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `country` varchar(100) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `tax_id` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  CONSTRAINT `billing_details_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `billing_details`
--

LOCK TABLES `billing_details` WRITE;
/*!40000 ALTER TABLE `billing_details` DISABLE KEYS */;
/*!40000 ALTER TABLE `billing_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `budgets`
--

DROP TABLE IF EXISTS `budgets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `budgets` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `category` varchar(100) NOT NULL,
  `budget_amount` decimal(12,2) NOT NULL,
  `period` varchar(20) DEFAULT 'monthly',
  `icon` varchar(10) DEFAULT '????',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_user_cat_period` (`user_id`,`category`,`period`),
  CONSTRAINT `budgets_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=70 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `budgets`
--

LOCK TABLES `budgets` WRITE;
/*!40000 ALTER TABLE `budgets` DISABLE KEYS */;
INSERT INTO `budgets` VALUES (16,13,'Transport',99.00,'monthly','????','2026-04-14 05:32:20','2026-04-14 05:32:20'),(64,13,'l',6.00,'monthly','????','2026-04-21 09:20:30','2026-04-21 09:20:30'),(65,13,'Food & Dining',5555555555.00,'monthly','????','2026-04-21 09:49:43','2026-04-21 09:49:43'),(66,13,'Others',12.00,'monthly','????','2026-04-21 09:56:00','2026-04-21 09:56:00'),(67,13,'123',123.00,'monthly','????','2026-04-21 10:03:32','2026-04-21 10:03:32'),(68,444,'Food & Dining',500.00,'monthly','????','2026-04-22 15:22:24','2026-04-22 15:22:24'),(69,445,'Food & Dining',500.00,'monthly','????','2026-04-22 15:22:42','2026-04-22 15:22:42');
/*!40000 ALTER TABLE `budgets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categories` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `icon` varchar(20) DEFAULT NULL,
  `type` enum('expense','income') DEFAULT 'expense',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=8181 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categories`
--

LOCK TABLES `categories` WRITE;
/*!40000 ALTER TABLE `categories` DISABLE KEYS */;
INSERT INTO `categories` VALUES (1,'Food & Dining','🍕','expense'),(2,'Transport','🚗','expense'),(3,'Shopping','🛍️','expense'),(4,'Entertainment','🎬','expense'),(5,'Health','🏥','expense'),(6,'Bills & Utilities','📱','expense'),(7,'Income','💵','income'),(8,'Investment','📈','income'),(9,'Others','📝','expense');
/*!40000 ALTER TABLE `categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `chat_history`
--

DROP TABLE IF EXISTS `chat_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chat_history` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `role` enum('user','assistant','system') NOT NULL,
  `content` text NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `chat_history_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=170 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chat_history`
--

LOCK TABLES `chat_history` WRITE;
/*!40000 ALTER TABLE `chat_history` DISABLE KEYS */;
INSERT INTO `chat_history` VALUES (166,13,'user','mera ek km kroge','2026-04-19 13:29:16'),(167,13,'assistant','Bilkul, Sanjay! 😊  \nBatao kya kaam hai — budget track karna hai, savings plan banana hai, ya phir kisi expense ko cut karne mein help chahiye?  \nAapke current balance hai **₹38,437**, income **₹83,059**, aur aapne **46.28%** save kiya — bohot accha hai! Bas ek nishaan chahiye, main aapke saath step-by-step chalunga.  \nKya aaj kuch specific goal hai? 💡','2026-04-19 13:29:25'),(168,13,'user','jese koi new user sign up krta h toh mhuje bto ki mhuje kya kya onboarding questions pucne chiye new user se','2026-04-19 13:30:21'),(169,13,'assistant','Samjha, Sanjay! 😊  \nAgar koi **new user** aapke financial app ya service pe sign up kar raha hai, toh onboarding questions ko **light, trust-building, aur actionable** banayein — zyada nahi, bas essential:\n\n- **“Aapka monthly income kitna hai?”** *(e.g., ₹83,059 — aapke numbers se inspire!)*  \n- **“Aap har mahine kitna save karne ka soch rahe hain?”** *(Goal: ₹5k? ₹15k?)*  \n- **“Aapke paas abhi koi debt ya loan hai?”** *(Credit card, personal loan, etc.)*  \n- **“Aapka financial goal agle 6 mahine ka kya hai?”** *(Emergency fund? Vacation? Investment?)*  \n- **“Aap kis tarah ka feedback pasand karenge?** *(Daily tips? Weekly summary? Auto-categorization?)*  \n\n💡 *Tip:* Har sawal ke baad ek chhota **“Aapne yeh kyun socha?”** jaise empathetic follow-up daal dein — user feel karega ki aap unki life ke saath khade hain, na ki sirf data collect kar rahe hain.\n\nAapke liye konsa goal priority hai — savings badhana? Ya users ko engage rakhna? 🚀','2026-04-19 13:30:47');
/*!40000 ALTER TABLE `chat_history` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `goals`
--

DROP TABLE IF EXISTS `goals`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `goals` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `name` varchar(255) NOT NULL,
  `target_amount` decimal(12,2) NOT NULL,
  `current_amount` decimal(12,2) DEFAULT '0.00',
  `deadline` date DEFAULT NULL,
  `icon` varchar(10) DEFAULT '????',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_user` (`user_id`),
  CONSTRAINT `goals_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=75 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `goals`
--

LOCK TABLES `goals` WRITE;
/*!40000 ALTER TABLE `goals` DISABLE KEYS */;
INSERT INTO `goals` VALUES (6,13,'lol',9.00,0.00,NULL,'????','2026-04-14 05:31:51','2026-04-14 05:31:51'),(70,13,'l',1.00,1.00,NULL,'????','2026-04-21 09:22:25','2026-04-21 09:22:25'),(71,13,'Goa Vacation',50000.00,36000.00,NULL,'????','2026-04-21 10:04:59','2026-04-21 10:04:59'),(72,13,'x',333.00,3.00,NULL,'????','2026-04-21 12:44:24','2026-04-21 12:44:24'),(73,444,'New Car',20000.00,0.00,NULL,'????','2026-04-22 15:22:24','2026-04-22 15:22:24'),(74,445,'New Car',20000.00,0.00,NULL,'????','2026-04-22 15:22:42','2026-04-22 15:22:42');
/*!40000 ALTER TABLE `goals` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `invoices`
--

DROP TABLE IF EXISTS `invoices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `invoices` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `invoice_number` varchar(50) NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `status` enum('PAID','PENDING','FAILED') DEFAULT 'PAID',
  `date` date NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `invoice_number` (`invoice_number`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `invoices_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `invoices`
--

LOCK TABLES `invoices` WRITE;
/*!40000 ALTER TABLE `invoices` DISABLE KEYS */;
/*!40000 ALTER TABLE `invoices` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `loans`
--

DROP TABLE IF EXISTS `loans`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `loans` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `name` varchar(255) NOT NULL,
  `type` varchar(100) DEFAULT 'Personal',
  `total_amount` decimal(15,2) NOT NULL,
  `emi_amount` decimal(15,2) DEFAULT '0.00',
  `outstanding_amount` decimal(15,2) DEFAULT '0.00',
  `interest_rate` decimal(5,2) DEFAULT '0.00',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `loans_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `loans`
--

LOCK TABLES `loans` WRITE;
/*!40000 ALTER TABLE `loans` DISABLE KEYS */;
INSERT INTO `loans` VALUES (1,13,'kaalu','home',10000000.00,12399.00,0.00,8.50,'2026-04-21 18:16:28'),(2,444,'Home Loan','Home',50000.00,1000.00,45000.00,7.50,'2026-04-22 20:52:24'),(3,445,'Home Loan','Home',50000.00,1000.00,45000.00,7.50,'2026-04-22 20:52:42');
/*!40000 ALTER TABLE `loans` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sessions`
--

DROP TABLE IF EXISTS `sessions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sessions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `refresh_token` varchar(512) NOT NULL,
  `expires_at` timestamp NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_token` (`refresh_token`(255)),
  KEY `idx_user` (`user_id`),
  CONSTRAINT `sessions_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sessions`
--

LOCK TABLES `sessions` WRITE;
/*!40000 ALTER TABLE `sessions` DISABLE KEYS */;
/*!40000 ALTER TABLE `sessions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transactions`
--

DROP TABLE IF EXISTS `transactions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transactions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `name` varchar(255) NOT NULL,
  `category` varchar(100) NOT NULL,
  `amount` decimal(12,2) NOT NULL,
  `type` enum('credit','debit') NOT NULL,
  `icon` varchar(10) DEFAULT '????',
  `date` date NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `is_recurring` tinyint(1) DEFAULT '0',
  `period` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_user_date` (`user_id`,`date` DESC),
  KEY `idx_user_category` (`user_id`,`category`),
  KEY `idx_tx_date` (`date`),
  KEY `idx_tx_category` (`category`),
  CONSTRAINT `transactions_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=207 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transactions`
--

LOCK TABLES `transactions` WRITE;
/*!40000 ALTER TABLE `transactions` DISABLE KEYS */;
INSERT INTO `transactions` VALUES (4,13,'lol','Home',53000.00,'credit','🏠','2026-04-14','2026-04-14 05:31:14',0,NULL),(5,13,'4','Home',44444.00,'debit','🏠','2026-04-14','2026-04-14 05:31:22',0,NULL),(6,13,'lol','Home',30000.00,'credit','🏠','2026-04-14','2026-04-14 05:42:45',0,NULL),(14,13,'spotify','Entertainment',59.00,'debit','🎮','2026-04-14','2026-04-14 06:48:25',0,NULL),(27,13,'spotify','Entertainment',59.00,'debit','🎮','2026-04-14','2026-04-14 07:20:41',0,NULL),(28,13,'dddddddddddddd','Entertainment',59.00,'credit','🎮','2026-04-14','2026-04-14 07:22:39',0,NULL),(33,13,'q','Food & Dining',1.00,'debit','🍕','2026-04-14','2026-04-14 07:43:55',0,NULL),(34,13,'spotify','Entertainment',59.00,'debit','🎮','2026-04-14','2026-04-14 08:13:23',0,NULL),(205,444,'Groceries','Food & Dining',150.50,'debit','📝','2026-04-22','2026-04-22 15:22:24',0,NULL),(206,445,'Groceries','Food & Dining',150.50,'debit','📝','2026-04-22','2026-04-22 15:22:42',0,NULL);
/*!40000 ALTER TABLE `transactions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_billing`
--

DROP TABLE IF EXISTS `user_billing`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_billing` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `plan_type` varchar(50) DEFAULT 'STARTER',
  `billing_email` varchar(255) DEFAULT '',
  `address` varchar(255) DEFAULT '',
  `country` varchar(100) DEFAULT '',
  `business_tax_id` varchar(100) DEFAULT '',
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `user_billing_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=108 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_billing`
--

LOCK TABLES `user_billing` WRITE;
/*!40000 ALTER TABLE `user_billing` DISABLE KEYS */;
INSERT INTO `user_billing` VALUES (9,13,'PRO','','','',''),(104,443,'STARTER','','','',''),(105,444,'STARTER','','','',''),(106,445,'STARTER','','','','');
/*!40000 ALTER TABLE `user_billing` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_invoices`
--

DROP TABLE IF EXISTS `user_invoices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_invoices` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `amount` decimal(15,2) NOT NULL,
  `invoice_number` varchar(100) DEFAULT NULL,
  `status` enum('PAID','PENDING','FAILED') DEFAULT 'PAID',
  `date_issued` date NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `invoice_number` (`invoice_number`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `user_invoices_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=128 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_invoices`
--

LOCK TABLES `user_invoices` WRITE;
/*!40000 ALTER TABLE `user_invoices` DISABLE KEYS */;
INSERT INTO `user_invoices` VALUES (90,13,0.00,'QJTKKF-00003','PAID','2026-03-28'),(91,13,0.00,'QJTKKF-00002','PAID','2026-02-28'),(92,13,0.00,'QJTKKF-00001','PAID','2026-01-28'),(119,443,0.00,'QJTKKF-443-03','PAID','2026-03-28'),(120,443,0.00,'QJTKKF-443-02','PAID','2026-02-28'),(121,443,0.00,'QJTKKF-443-01','PAID','2026-01-28'),(122,444,0.00,'QJTKKF-444-03','PAID','2026-03-28'),(123,444,0.00,'QJTKKF-444-02','PAID','2026-02-28'),(124,444,0.00,'QJTKKF-444-01','PAID','2026-01-28'),(125,445,0.00,'QJTKKF-445-03','PAID','2026-03-28'),(126,445,0.00,'QJTKKF-445-02','PAID','2026-02-28'),(127,445,0.00,'QJTKKF-445-01','PAID','2026-01-28');
/*!40000 ALTER TABLE `user_invoices` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_payment_methods`
--

DROP TABLE IF EXISTS `user_payment_methods`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_payment_methods` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `identifier` varchar(50) DEFAULT NULL,
  `exp_month` int DEFAULT NULL,
  `exp_year` int DEFAULT NULL,
  `brand` varchar(50) DEFAULT NULL,
  `is_default` tinyint(1) DEFAULT '0',
  `method_type` enum('CARD','UPI','QR') DEFAULT 'CARD',
  `upi_id` varchar(255) DEFAULT NULL,
  `card_last4` varchar(4) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `user_payment_methods_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_payment_methods`
--

LOCK TABLES `user_payment_methods` WRITE;
/*!40000 ALTER TABLE `user_payment_methods` DISABLE KEYS */;
INSERT INTO `user_payment_methods` VALUES (35,13,NULL,12,2028,'Visa',1,'CARD',NULL,'4242'),(42,443,NULL,12,2028,'Visa',1,'CARD',NULL,'4242'),(43,444,NULL,12,2028,'Visa',1,'CARD',NULL,'4242'),(44,445,NULL,12,2028,'Visa',1,'CARD',NULL,'4242');
/*!40000 ALTER TABLE `user_payment_methods` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(255) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `full_name` varchar(150) NOT NULL,
  `plan` varchar(50) DEFAULT 'starter',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `last_report_at` datetime DEFAULT NULL,
  `phone` varchar(20) DEFAULT '',
  `currency` varchar(50) DEFAULT '₹ INR — Indian Rupee',
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  KEY `idx_email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=446 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (13,'sanjaynegi101125@gmail.com','pbkdf2:sha256:600000$8kkCAJXFpuzdwglJ$fd9ccbe88426ec5487fb9e1629c38537d11d8dfd2ed1dcdb19301d9ca4543211','Sanjay Negi','pro','2026-04-11 09:20:23','2026-04-18 13:38:46',NULL,'8265888526','₹ INR — Indian Rupee'),(443,'test@test.com','pbkdf2:sha256:600000$yzmyZ1jkwSnPcRFP$12c82853fef3a3e7b32fb953617e3d8d5caffd568da5c3f2a449d00a5f129421','Test User','starter','2026-04-22 15:19:28','2026-04-22 15:19:28',NULL,'','₹ INR — Indian Rupee'),(444,'test_3711@test.com','pbkdf2:sha256:600000$jNjwXavNy3InJgTy$0cb56b00757d16a64e18ff5ae3c89a87b6369fa91e45bba65d8b25668782f731','Test Flow','starter','2026-04-22 15:22:23','2026-04-22 15:22:23',NULL,'','₹ INR — Indian Rupee'),(445,'test_2887@test.com','pbkdf2:sha256:600000$nDpOkenYlIE2wvcc$eb3c846b89df8f5265c9cab059c072d7340cc056b92a9c15ad23b93e6d216562','Test Flow','starter','2026-04-22 15:22:41','2026-04-22 15:22:41',NULL,'','₹ INR — Indian Rupee');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-22 22:48:49
