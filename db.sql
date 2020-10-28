-- --------------------------------------------------------
-- 主机:                           127.0.0.1
-- 服务器版本:                        8.0.19 - MySQL Community Server - GPL
-- 服务器操作系统:                      Win64
-- HeidiSQL 版本:                  11.0.0.5919
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- 导出 xpc 的数据库结构
CREATE DATABASE IF NOT EXISTS `xpc` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `xpc`;

-- 导出  表 xpc.comments 结构
CREATE TABLE IF NOT EXISTS `comments` (
  `pid` int DEFAULT NULL,
  `uname` varchar(999) DEFAULT NULL,
  `uid` int DEFAULT NULL,
  `avatar` varchar(999) DEFAULT NULL,
  `commentid` int DEFAULT NULL,
  `created_at` varchar(50) DEFAULT NULL,
  `like_counts` int DEFAULT NULL,
  `content` varchar(9999) DEFAULT NULL,
  `reply` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 数据导出被取消选择。

-- 导出  表 xpc.composers 结构
CREATE TABLE IF NOT EXISTS `composers` (
  `uid` int DEFAULT NULL,
  `banner` varchar(999) DEFAULT NULL,
  `avatar` varchar(999) DEFAULT NULL,
  `name` varchar(999) DEFAULT NULL,
  `introduction` varchar(9999) DEFAULT NULL,
  `like_counts` int DEFAULT NULL,
  `fans_counts` int DEFAULT NULL,
  `follow_counts` int DEFAULT NULL,
  `location` varchar(50) DEFAULT NULL,
  `career` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 数据导出被取消选择。

-- 导出  表 xpc.copyrights 结构
CREATE TABLE IF NOT EXISTS `copyrights` (
  `puid` varchar(999) DEFAULT NULL,
  `pid` int DEFAULT NULL,
  `uid` int DEFAULT NULL,
  `roles` varchar(99) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 数据导出被取消选择。

-- 导出  表 xpc.posts 结构
CREATE TABLE IF NOT EXISTS `posts` (
  `pid` int DEFAULT NULL,
  `title` varchar(100) DEFAULT NULL,
  `thumbnail` varchar(1000) DEFAULT NULL,
  `preview` varchar(1000) DEFAULT NULL,
  `video` varchar(1000) DEFAULT NULL,
  `video_format` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT 'mp4',
  `duration` int DEFAULT NULL,
  `category` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `created_at` varchar(50) DEFAULT NULL,
  `play_counts` int DEFAULT NULL,
  `like_counts` int DEFAULT NULL,
  `description` varchar(9999) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 数据导出被取消选择。

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
