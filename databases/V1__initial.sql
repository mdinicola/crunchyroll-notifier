CREATE TABLE `series` (
  `id` varchar(45) NOT NULL,
  `title` varchar(100) NOT NULL,
  `slug_title` varchar(100) NOT NULL,
  `date_added` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `seasons` (
  `id` varchar(45) NOT NULL,
  `series_id` varchar(45) NOT NULL,
  `title` varchar(100) NOT NULL,
  `slug_title` varchar(100) NOT NULL,
  `date_added` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_seasons_series_id` (`series_id`),
  CONSTRAINT `FK_seasons_series_id` FOREIGN KEY (`series_id`) REFERENCES `series` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `episodes` (
  `id` varchar(45) NOT NULL,
  `series_id` varchar(45) NOT NULL,
  `season_id` varchar(45) NOT NULL,
  `title` varchar(100) NOT NULL,
  `slug_title` varchar(100) NOT NULL,
  `is_dubbed` tinyint(1) NOT NULL,
  `is_subbed` tinyint(1) NOT NULL,
  `date_added` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_episodes_series_id` (`series_id`),
  KEY `FK_episodes_seasons_id` (`season_id`),
  CONSTRAINT `FK_episodes_seasons_id` FOREIGN KEY (`season_id`) REFERENCES `seasons` (`id`),
  CONSTRAINT `FK_episodes_series_id` FOREIGN KEY (`series_id`) REFERENCES `series` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `locales` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `episode_id` varchar(45) NOT NULL,
  `audio_locale` varchar(25) NOT NULL,
  `subtitle_locale` varchar(25) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_locales_episodes_id` (`episode_id`),
  CONSTRAINT `FK_locales_episodes_id` FOREIGN KEY (`episode_id`) REFERENCES `episodes` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;