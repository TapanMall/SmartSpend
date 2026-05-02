import mysql.connector
from mysql.connector import Error

def recreate_database():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password=''
        )
        cursor = connection.cursor()

        db_name = "smartspend"
        
        print(f"Connecting to MySQL server at localhost...")
        print(f"Creating database `{db_name}` if it does not exist...")
        
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        cursor.execute(f"USE {db_name}")

        print("Creating tables...")

        print(" -> Creating table `billing_details`...")
        cursor.execute("""CREATE TABLE `billing_details` (
  `user_id` int NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `country` varchar(100) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `tax_id` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  CONSTRAINT `billing_details_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;""")

        print(" -> Creating table `budgets`...")
        cursor.execute("""CREATE TABLE `budgets` (
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
) ENGINE=InnoDB AUTO_INCREMENT=70 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;""")

        print(" -> Creating table `categories`...")
        cursor.execute("""CREATE TABLE `categories` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `icon` varchar(20) DEFAULT NULL,
  `type` enum('expense','income') DEFAULT 'expense',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=8181 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;""")

        print(" -> Creating table `chat_history`...")
        cursor.execute("""CREATE TABLE `chat_history` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `role` enum('user','assistant','system') NOT NULL,
  `content` text NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `chat_history_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=170 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;""")

        print(" -> Creating table `goals`...")
        cursor.execute("""CREATE TABLE `goals` (
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
) ENGINE=InnoDB AUTO_INCREMENT=75 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;""")

        print(" -> Creating table `invoices`...")
        cursor.execute("""CREATE TABLE `invoices` (
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
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;""")

        print(" -> Creating table `loans`...")
        cursor.execute("""CREATE TABLE `loans` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `name` varchar(255) NOT NULL,
  `type` varchar(100) DEFAULT 'Personal',
  `total_amount` decimal(15,2) NOT NULL,
  `emi_amount` decimal(15,2) DEFAULT '0.00',
  `outstanding_amount` decimal(15,2) DEFAULT '0.00',
  `interest_rate` decimal(5,2) DEFAULT '0.00',
  `emi_day` int DEFAULT '5',
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `tenure_months` int DEFAULT '0',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `loans_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;""")

        print(" -> Creating table `sessions`...")
        cursor.execute("""CREATE TABLE `sessions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `refresh_token` varchar(512) NOT NULL,
  `expires_at` timestamp NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_token` (`refresh_token`(255)),
  KEY `idx_user` (`user_id`),
  CONSTRAINT `sessions_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;""")

        print(" -> Creating table `transactions`...")
        cursor.execute("""CREATE TABLE `transactions` (
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
) ENGINE=InnoDB AUTO_INCREMENT=207 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;""")

        print(" -> Creating table `user_billing`...")
        cursor.execute("""CREATE TABLE `user_billing` (
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
) ENGINE=InnoDB AUTO_INCREMENT=108 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;""")

        print(" -> Creating table `user_invoices`...")
        cursor.execute("""CREATE TABLE `user_invoices` (
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
) ENGINE=InnoDB AUTO_INCREMENT=128 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;""")

        print(" -> Creating table `user_payment_methods`...")
        cursor.execute("""CREATE TABLE `user_payment_methods` (
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
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;""")

        print(" -> Creating table `users`...")
        cursor.execute("""CREATE TABLE `users` (
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
) ENGINE=InnoDB AUTO_INCREMENT=446 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;""")

        print(" -> Creating table `emi_history`...")
        cursor.execute("""CREATE TABLE `emi_history` (
  `id` int NOT NULL AUTO_INCREMENT,
  `loan_id` int DEFAULT NULL,
  `amount_paid` decimal(15,2) NOT NULL,
  `principal_paid` decimal(15,2) DEFAULT '0.00',
  `interest_paid` decimal(15,2) DEFAULT '0.00',
  `payment_date` date NOT NULL,
  `status` enum('PAID','PENDING','MISSED') DEFAULT 'PAID',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `loan_id` (`loan_id`),
  CONSTRAINT `emi_history_ibfk_1` FOREIGN KEY (`loan_id`) REFERENCES `loans` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;""")

        print(" -> Creating table `investments`...")
        cursor.execute("""CREATE TABLE `investments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `name` varchar(255) NOT NULL,
  `type` varchar(100) DEFAULT 'Stocks',
  `amount` decimal(15,2) NOT NULL,
  `date` date NOT NULL,
  `notes` text,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `investments_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;""")

        connection.commit()
        print(f"\nDatabase structure for `{db_name}` recreated successfully!")

    except Error as e:
        print(f"Error while connecting to MySQL or creating schema: {e}")
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()

if __name__ == "__main__":
    print("This script will create the `smartspend` database and its exact table structure.")
    print("It assumes MySQL is running locally with user 'root' and no password.\n")
    recreate_database()
