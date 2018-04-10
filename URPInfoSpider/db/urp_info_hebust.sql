/*
Navicat MySQL Data Transfer

Source Server         : 本地 MySQL
Source Server Version : 50714
Source Host           : localhost:3306
Source Database       : urp_roll_info

Target Server Type    : MYSQL
Target Server Version : 50714
File Encoding         : 65001

Date: 2018-04-10 12:32:38
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for urp_info_hebust_2
-- ----------------------------
DROP TABLE IF EXISTS `urp_info_hebust_2`;
CREATE TABLE `urp_info_hebust_2` (
  `STUID` varchar(50) NOT NULL,
  `NAME` varchar(50) DEFAULT NULL,
  `NAME_PY` varchar(50) DEFAULT NULL,
  `NAME_EN` varchar(50) DEFAULT NULL,
  `NAME_OLD` varchar(50) DEFAULT NULL,
  `ICID` varchar(50) DEFAULT NULL,
  `GENDER` varchar(50) DEFAULT NULL,
  `STU_CATEGORY` varchar(50) DEFAULT NULL,
  `SPECIAL_CATEGORY` varchar(50) DEFAULT NULL,
  `SCHOOL_ROLL_STATUS` varchar(50) DEFAULT NULL,
  `FEE_CATEGORY` varchar(50) DEFAULT NULL,
  `NATION` varchar(50) DEFAULT NULL,
  `BIRTH_PLACE` varchar(50) DEFAULT NULL,
  `BIRTH_DATE` varchar(50) DEFAULT NULL,
  `POLITICS_STATUS` varchar(50) DEFAULT NULL,
  `EXAM_REGION` varchar(50) DEFAULT NULL,
  `GRADUATE_SCHOOL` varchar(50) DEFAULT NULL,
  `GK_SCORE` varchar(50) DEFAULT NULL,
  `MATRICULATE_ID` varchar(50) DEFAULT NULL,
  `GK_ID` varchar(50) DEFAULT NULL,
  `GK_LANGUAGE` varchar(50) DEFAULT NULL,
  `CONTACT_ADDRESS` varchar(100) DEFAULT NULL,
  `POSTCODE` varchar(50) DEFAULT NULL,
  `PATRIARCH_INFO` varchar(50) DEFAULT NULL,
  `ENROLLMENT_DATE` varchar(50) DEFAULT NULL,
  `DEPARTMENT` varchar(50) DEFAULT NULL,
  `MAJOR` varchar(50) DEFAULT NULL,
  `MAJOR_DIRECTION` varchar(50) DEFAULT NULL,
  `GRADE` varchar(50) DEFAULT NULL,
  `CLASS` varchar(50) DEFAULT NULL,
  `HAS_ROLL` varchar(50) DEFAULT NULL,
  `HAS_NATIONAL_ROLL` varchar(50) DEFAULT NULL,
  `SCHOOL_PART` varchar(50) DEFAULT NULL,
  `TRANSACTION` varchar(50) DEFAULT NULL,
  `FOREIGN_LANGUAGE` varchar(50) DEFAULT NULL,
  `DORM_ADDRESS` varchar(50) DEFAULT NULL,
  `YCSJ` varchar(50) DEFAULT NULL,
  `TRAIN_LEVEL` varchar(50) DEFAULT NULL,
  `TRAIN_PATTERN` varchar(50) DEFAULT NULL,
  `SHUNT_DIRECTION` varchar(50) DEFAULT NULL,
  `LEAVE_SCHOOL` varchar(50) DEFAULT NULL,
  `COMMENT` varchar(50) DEFAULT NULL,
  `COMMENT1` varchar(50) DEFAULT NULL,
  `COMMENT2` varchar(50) DEFAULT NULL,
  `COMMENT3` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`STUID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
