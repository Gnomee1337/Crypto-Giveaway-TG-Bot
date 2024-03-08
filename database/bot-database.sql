-- phpMyAdmin SQL Dump

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: ``
--

-- --------------------------------------------------------

--
-- Table structure for table `bundle_shop`
--

CREATE TABLE IF NOT EXISTS `bundle_shop` (
  `id_bundle_shop` int NOT NULL AUTO_INCREMENT,
  `bundle_name` varchar(45) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `tokens_amount` int DEFAULT NULL,
  `price_amount` int DEFAULT NULL,
  `bundle_status` int DEFAULT NULL,
  PRIMARY KEY (`id_bundle_shop`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `panel_accounts`
--

CREATE TABLE IF NOT EXISTS `panel_accounts` (
  `id_accs` int NOT NULL AUTO_INCREMENT,
  `accs_username` varchar(30) COLLATE utf8mb4_general_ci NOT NULL,
  `accs_password` varchar(90) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id_accs`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `payment_logs`
--

CREATE TABLE IF NOT EXISTS `payment_logs` (
  `id_payment_log` int NOT NULL AUTO_INCREMENT,
  `id_payment_user` bigint NOT NULL,
  `payment_sum` int NOT NULL,
  `points_bought` int NOT NULL,
  PRIMARY KEY (`id_payment_log`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tasks_bot`
--

CREATE TABLE IF NOT EXISTS `tasks_bot` (
  `id_tasks` int NOT NULL AUTO_INCREMENT,
  `task_author` bigint NOT NULL,
  `task` varchar(90) COLLATE utf8mb4_general_ci NOT NULL,
  `task_complete_counter` int NOT NULL DEFAULT '1',
  `points_reward` int DEFAULT '0',
  PRIMARY KEY (`id_tasks`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `task_tracker_2`
--

CREATE TABLE IF NOT EXISTS `task_tracker_2` (
  `id_key_task_tracker` int NOT NULL AUTO_INCREMENT,
  `task_id_tracker` int NOT NULL,
  `assigned_user` int NOT NULL,
  `answer_field` varchar(90) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `completed` varchar(15) COLLATE utf8mb4_general_ci DEFAULT '0',
  `verified` varchar(15) COLLATE utf8mb4_general_ci DEFAULT '0',
  `task_completed_times` int DEFAULT '0',
  PRIMARY KEY (`id_key_task_tracker`),
  KEY `assigned_user` (`assigned_user`),
  KEY `task_id_tracker` (`task_id_tracker`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `users_bot`
--

CREATE TABLE IF NOT EXISTS `users_bot` (
  `id_users` int NOT NULL AUTO_INCREMENT,
  `tg_id` bigint NOT NULL,
  `tg_nickname` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `wallet` varchar(80) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `signup` varchar(15) COLLATE utf8mb4_general_ci DEFAULT '0',
  `referral_id` bigint DEFAULT NULL,
  `user_points` int DEFAULT '0',
  `invite_fails` int DEFAULT '0',
  `language` varchar(15) COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'ru',
  PRIMARY KEY (`id_users`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `task_tracker_2`
--
ALTER TABLE `task_tracker_2`
  ADD CONSTRAINT `task_tracker_2_ibfk_1` FOREIGN KEY (`assigned_user`) REFERENCES `users_bot` (`id_users`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `task_tracker_2_ibfk_2` FOREIGN KEY (`task_id_tracker`) REFERENCES `tasks_bot` (`id_tasks`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
