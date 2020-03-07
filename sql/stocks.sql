-- phpMyAdmin SQL Dump
-- version 4.8.3
-- https://www.phpmyadmin.net/
--
-- 主机： localhost
-- 生成日期： 2020-03-04 15:00:25
-- 服务器版本： 8.0.19
-- PHP 版本： 7.4.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 数据库： `stock_data_cn`
--

-- --------------------------------------------------------

--
-- 表的结构 `stocks`
--

CREATE TABLE `stocks` (
  `id` int NOT NULL,
  `code` varchar(6) NOT NULL COMMENT '股票代码',
  `area` varchar(8) NOT NULL COMMENT '交易所',
  `table_name` varchar(12) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '对应的表名'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转储表的索引
--

--
-- 表的索引 `stocks`
--
ALTER TABLE `stocks`
  ADD PRIMARY KEY (`id`),
  ADD KEY `code` (`code`);

--
-- 在导出的表使用AUTO_INCREMENT
--

--
-- 使用表AUTO_INCREMENT `stocks`
--
ALTER TABLE `stocks`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
