
CREATE DATABASE Highlite;

USE Highlite;

CREATE TABLE Video (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
	file_name VARCHAR(255) NOT NULL,
	format VARCHAR(255) NOT NULL,
    youtube_id VARCHAR(20),
    category VARCHAR(20) NOT NULL,
    creation_date DATE NOT NULL
) ENGINE=INNODB;

CREATE TABLE Article (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	title VARCHAR(510) NOT NULL UNIQUE,
	source VARCHAR(50) NOT NULL,
	category VARCHAR(20) NOT NULL,
    url VARCHAR(510),
    image_url VARCHAR(510) NOT NULL,
    image LONGBLOB,
    publication_time VARCHAR(50),
    scrap_date DATE NOT NULL
) ENGINE=INNODB;

CREATE TABLE VideoArticle (
    video_id INT NOT NULL,
    article_id INT NOT NULL,
    pos INT NOT NULL,
    PRIMARY KEY (video_id, article_id),
    CONSTRAINT FK_VIDEO_1 FOREIGN KEY (video_id)
        REFERENCES `Video`(id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT FK_ARTICLE_1 FOREIGN KEY (article_id)
        REFERENCES `Article`(id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=INNODB;

CREATE TABLE ArticleVote (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    article_id INT NOT NULL,
    ip VARCHAR(50) NOT NULL,
    CONSTRAINT FK_ARTICLE_2 FOREIGN KEY (article_id)
        REFERENCES `Article`(id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=INNODB;

ALTER TABLE ArticleVote
  ADD CONSTRAINT UNIQUE_VOTE UNIQUE(article_id, ip);

ALTER TABLE Article
  MODIFY image LONGBLOB NOT NULL;

CREATE TABLE Pipeline (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    category VARCHAR(20) NOT NULL,
    scrap_time VARCHAR(20) NOT NULL,
    generation_time VARCHAR(20) NOT NULL,
    publication_time VARCHAR(20) NOT NULL,
    filter VARCHAR(510) DEFAULT NULL
) ENGINE=INNODB;

INSERT INTO Pipeline VALUES
    (1, "COVID-19", "17:00", "18:45", "19:00", "confinement,coronavirus,covid,deconfinement"),
    (2, "FOOTBALL", "18:00", "19:45", "20:00", NULL);

CREATE TABLE Source (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    category VARCHAR(20) NOT NULL,
    publisher VARCHAR(40) NOT NULL,
    url VARCHAR(510) NOT NULL
) ENGINE=INNODB;

INSERT INTO Source VALUES
    (1, "COVID-19", "Ouest-France",     "https://www.ouest-france.fr/"),
    (2, "COVID-19", "Le Monde",         "https://www.lemonde.fr/"),
    (3, "COVID-19", "Libération",       "https://www.liberation.fr/"),
    (4, "COVID-19", "Les Echos",        "https://www.lesechos.fr/"),
    (5, "COVID-19", "Le Figaro",        "https://www.lefigaro.fr/"),
    (6, "COVID-19", "Le Parisien",      "http://www.leparisien.fr/"),
    (7, "COVID-19", "20 Minutes",       "https://www.20minutes.fr/"),
    (8, "COVID-19", "La Tribune",       "https://www.latribune.fr/"),
    (9, "COVID-19", "L'Obs",            "https://www.nouvelobs.com/"),

    (10, "FOOTBALL", "L'Equipe",        "https://www.lequipe.fr/Football/"),
    (11, "FOOTBALL", "France Football", "https://www.francefootball.fr/"),
    (12, "FOOTBALL", "Maxifoot",        "http://www.maxifoot.fr/"),
    (13, "FOOTBALL", "Foot365",         "https://www.football365.fr/"),
    (14, "FOOTBALL", "So Foot",         "https://www.sofoot.com/"),
    (15, "FOOTBALL", "Foot Mercato",    "http://www.footmercato.net/");

CREATE TABLE Log (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    status VARCHAR(20) NOT NULL,
    datetime DATETIME NOT NULL,
    trace varchar(8192) NOT NULL
) ENGINE=INNODB;

CREATE TABLE Upload (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    video_id INT NOT NULL,
    platform VARCHAR(20) NOT NULL,
    publication_datetime DATETIME NOT NULL,
    CONSTRAINT FK_VIDEO_UPLOAD_1 FOREIGN KEY (video_id)
        REFERENCES `Video`(id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=INNODB;