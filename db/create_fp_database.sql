-- -----------------------------------------------------------
-- Script to generate the schema for the FPDetective database
-- -----------------------------------------------------------

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `fp_detective`
--
CREATE DATABASE `fp_detective` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `fp_detective`;

-- -----------------------------------------------------------

--
-- Table structure for table `crawl_job`
--

CREATE TABLE IF NOT EXISTS `crawl_job` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `num_crawl_urls` int(11) NOT NULL,
  `log_file_path` varchar(4096) NOT NULL,
  `browser_type` varchar(256) NOT NULL,
  `browser_user_agent` varchar(2048) NOT NULL,
  `max_parallel_procs` int(11) NOT NULL,
  `job_dir_path` varchar(1024) NOT NULL,
  `index_html_path` varchar(1024) NOT NULL,
  `browser_binary_path` varchar(1024) NOT NULL,
  `browser_mitm_proxy` tinyint(1) NOT NULL,
  `fc_fontdebug` tinyint(1) NOT NULL,
  `cmd` varchar(256) NOT NULL,
  `desc` varchar(1024) NOT NULL,
  `start_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `finish_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- -----------------------------------------------------------

--
-- Table structure for table `js_info`
--

CREATE TABLE IF NOT EXISTS `js_info` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `rank` int(10) unsigned NOT NULL,
  `url` varchar(1024) NOT NULL COMMENT 'web site url',
  `fonts_loaded` text NOT NULL,
  `fonts_by_origins` mediumtext NOT NULL,
  `num_font_loads` int(11) NOT NULL,
  `num_offsetWidth_calls` int(11) NOT NULL,
  `num_offsetHeight_calls` int(11) NOT NULL,
  `site_crawl_log` text NOT NULL,
  `site_info_id` int(10) unsigned NOT NULL,
  `js_calls` mediumtext NOT NULL,
  `crawl_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `site_info_id` (`site_info_id`),
  KEY `crawl_id` (`crawl_id`),
  KEY `rank` (`rank`),
  KEY `num_font_loads` (`num_font_loads`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- -----------------------------------------------------------

--
-- Table structure for table `site_info`
--

CREATE TABLE IF NOT EXISTS `site_info` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `http_requests` mediumtext NOT NULL,
  `http_responses` mediumtext NOT NULL,
  `crawl_id` int(10) unsigned NOT NULL,
  `url` varchar(4096) NOT NULL,
  `fp_detected` varchar(512) NOT NULL,
  `fc_dbg_font_loads` text NOT NULL COMMENT 'list of fonts collected by fontconfig fc_debug logs',
  `num_fc_dbg_font_loads` int(10) unsigned NOT NULL,
  `rank` int(10) unsigned NOT NULL,
  `visit_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `log_complete` tinyint(1) NOT NULL DEFAULT '0' COMMENT 'flag for incomplete logs (premature ends)',
  PRIMARY KEY (`id`),
  KEY `js_info_id` (`crawl_id`),
  KEY `rank` (`rank`),
  KEY `fp_detected` (`fp_detected`(255))
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- -----------------------------------------------------------

--
-- Table structure for table `swf_obj`
--

CREATE TABLE IF NOT EXISTS `swf_obj` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `rank` int(11) NOT NULL,
  `local_path` varchar(1024) NOT NULL,
  `domain` varchar(512) NOT NULL,
  `page_url` varchar(4096) NOT NULL,
  `duplicate` tinyint(1) NOT NULL DEFAULT '0',
  `swf_url` varchar(4096) NOT NULL,
  `occ_vector` varchar(512) NOT NULL,
  `feat_vector` varchar(512) NOT NULL,
  `hash` varchar(512) NOT NULL,
  `referer` varchar(4096) NOT NULL,
  `occ_string` varchar(1024) NOT NULL,
  `crawl_id` int(10) unsigned NOT NULL,
  `site_info_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `rank` (`rank`),
  KEY `crawl_id` (`crawl_id`),
  KEY `site_info_id` (`site_info_id`),
  KEY `hash` (`hash`(255))
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- -----------------------------------------------------------
-- DB for testing
CREATE DATABASE `fp_detective_test` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `fp_detective_test`;

CREATE TABLE IF NOT EXISTS `crawl_job` LIKE fp_detective.crawl_job;
CREATE TABLE IF NOT EXISTS `js_info` LIKE fp_detective.js_info;
CREATE TABLE IF NOT EXISTS `site_info` LIKE fp_detective.site_info;
CREATE TABLE IF NOT EXISTS `swf_obj` LIKE fp_detective.swf_obj;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
