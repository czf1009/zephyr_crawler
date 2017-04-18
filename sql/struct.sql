-- MySQL dump 10.13  Distrib 5.7.16, for Linux (x86_64)
--
-- Host: localhost    Database: app_test
-- ------------------------------------------------------
-- Server version	5.7.16-0ubuntu0.16.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `brand`
--

DROP TABLE IF EXISTS `brand`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `brand` (
  `brand_id` int(11) NOT NULL AUTO_INCREMENT,
  `brand_name` varchar(45) NOT NULL,
  PRIMARY KEY (`brand_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3284 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `category` (
  `category_id` int(11) NOT NULL,
  `category_name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`category_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `common`
--

DROP TABLE IF EXISTS `common`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `common` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `lable` varchar(45) CHARACTER SET latin1 NOT NULL,
  `body` json NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5299628 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `good`
--

DROP TABLE IF EXISTS `good`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `good` (
  `good_id` varchar(11) NOT NULL,
  `good_name` varchar(100) NOT NULL,
  `brand_id` int(11) NOT NULL,
  `link` varchar(100) NOT NULL,
  `category_id` int(11) DEFAULT NULL,
  `category_id_sub` int(11) DEFAULT NULL,
  `category_id_third` int(11) DEFAULT NULL,
  `image` varchar(100) NOT NULL,
  `description` varchar(300) DEFAULT NULL,
  `date_create` timestamp NULL DEFAULT NULL,
  `date_last` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`good_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary view structure for view `good_create_del`
--

DROP TABLE IF EXISTS `good_create_del`;
/*!50001 DROP VIEW IF EXISTS `good_create_del`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE VIEW `good_create_del` AS SELECT 
 1 AS `date`,
 1 AS `num_create`,
 1 AS `num_del`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `good_view`
--

DROP TABLE IF EXISTS `good_view`;
/*!50001 DROP VIEW IF EXISTS `good_view`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE VIEW `good_view` AS SELECT 
 1 AS `good_id`,
 1 AS `good_name`,
 1 AS `brand_name`,
 1 AS `category_name`,
 1 AS `sub_category_name`,
 1 AS `thrid_category_name`,
 1 AS `link`,
 1 AS `image`,
 1 AS `description`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `jd`
--

DROP TABLE IF EXISTS `jd`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `jd` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ware_id` bigint(20) NOT NULL,
  `wname` varchar(100) NOT NULL,
  `jd_price` float NOT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=79828 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `jd_comment`
--

DROP TABLE IF EXISTS `jd_comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `jd_comment` (
  `comment_id` bigint(20) NOT NULL,
  `comment_data` varchar(300) NOT NULL,
  `comment_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `ware_id` bigint(20) NOT NULL,
  PRIMARY KEY (`comment_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `price_stock`
--

DROP TABLE IF EXISTS `price_stock`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `price_stock` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `good_id` varchar(11) NOT NULL,
  `price` float NOT NULL,
  `price_original` float DEFAULT NULL,
  `price_vip` float DEFAULT NULL,
  `price_svip` float DEFAULT NULL,
  `stock` int(11) NOT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5406724 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary view structure for view `price_stock_view`
--

DROP TABLE IF EXISTS `price_stock_view`;
/*!50001 DROP VIEW IF EXISTS `price_stock_view`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE VIEW `price_stock_view` AS SELECT 
 1 AS `good_id`,
 1 AS `good_name`,
 1 AS `price`,
 1 AS `price_original`,
 1 AS `price_vip`,
 1 AS `price_svip`,
 1 AS `date`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `proxy`
--

DROP TABLE IF EXISTS `proxy`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `proxy` (
  `ip` varchar(16) NOT NULL,
  `port` varchar(6) NOT NULL,
  `https` tinyint(2) NOT NULL DEFAULT '0' COMMENT '0: no\n1: yes\n2: yes & no',
  `is_active` tinyint(2) NOT NULL DEFAULT '1' COMMENT '0: not active\n1: active',
  `last_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`ip`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='save proxy';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Final view structure for view `good_create_del`
--

/*!50001 DROP VIEW IF EXISTS `good_create_del`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`user_test`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `good_create_del` AS select `c`.`date` AS `date`,`c`.`num_create` AS `num_create`,`l`.`num_del` AS `num_del` from (((select date_format(`app_test`.`good`.`date_create`,'%Y-%m-%d') AS `date`,count(0) AS `num_create`,NULL AS `num_del` from `app_test`.`good` group by `date` limit 1,999999)) `c` left join (select date_format(`app_test`.`good`.`date_last`,'%Y-%m-%d') AS `date`,NULL AS `NULL`,count(0) AS `num_del` from `app_test`.`good` group by `date` desc limit 1,999999) `l` on((`c`.`date` = `l`.`date`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `good_view`
--

/*!50001 DROP VIEW IF EXISTS `good_view`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`user_test`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `good_view` AS select `g`.`good_id` AS `good_id`,`g`.`good_name` AS `good_name`,`b`.`brand_name` AS `brand_name`,`c`.`category_name` AS `category_name`,`sc`.`category_name` AS `sub_category_name`,`tc`.`category_name` AS `thrid_category_name`,`g`.`link` AS `link`,`g`.`image` AS `image`,`g`.`description` AS `description` from ((((`good` `g` left join `brand` `b` on((`g`.`brand_id` = `b`.`brand_id`))) left join `category` `c` on((`g`.`category_id` = `c`.`category_id`))) left join `category` `sc` on((`g`.`category_id_sub` = `sc`.`category_id`))) left join `category` `tc` on((`g`.`category_id_third` = `tc`.`category_id`))) order by `g`.`good_id` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `price_stock_view`
--

/*!50001 DROP VIEW IF EXISTS `price_stock_view`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`user_test`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `price_stock_view` AS select `price_stock`.`good_id` AS `good_id`,`good`.`good_name` AS `good_name`,`price_stock`.`price` AS `price`,`price_stock`.`price_original` AS `price_original`,`price_stock`.`price_vip` AS `price_vip`,`price_stock`.`price_svip` AS `price_svip`,`price_stock`.`date` AS `date` from (`price_stock` left join `good` on((`price_stock`.`good_id` = `good`.`good_id`))) order by `price_stock`.`good_id` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-04-19  0:51:03
