GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' 
    IDENTIFIED BY 'password' 
    WITH GRANT OPTION;

FLUSH PRIVILEGES;


CREATE DATABASE IF NOT EXISTS app_db;
USE app_db;

CREATE TABLE submitlog (
    id INT AUTO_INCREMENT PRIMARY KEY,
    post_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    username VARCHAR(255) NOT NULL,
    public_score DOUBLE NOT NULL,
    private_score DOUBLE NOT NULL
);


CREATE TABLE team (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    -- 画像のバイナリデータをそのまま保存する. max 1MB
    icon MEDIUMBLOB NOT NULL
);

-- ダミーの投稿データ
INSERT INTO submitlog (username, public_score, private_score) VALUES ('user1', 0.5, 0.5);
INSERT INTO submitlog (username, public_score, private_score) VALUES ('user2', 0.6, 0.6);
INSERT INTO submitlog (username, public_score, private_score) VALUES ('user2', 0.7, 0.7);
INSERT INTO submitlog (username, public_score, private_score) VALUES ('user4', 0.8, 0.8);
INSERT INTO submitlog (username, public_score, private_score) VALUES ('Unknown', 0.03, 0.8);


INSERT INTO submitlog (post_date, username, public_score, private_score)
VALUES (STR_TO_DATE('2024-05-10 00:00:00', '%Y-%m-%d %H:%i:%s'), 'abap34', 0.5, 0.5);
INSERT INTO submitlog (post_date, username, public_score, private_score)
VALUES (STR_TO_DATE('2024-05-10 01:00:00', '%Y-%m-%d %H:%i:%s'), 'abap34', 0.4, 0.6);
INSERT INTO submitlog (post_date, username, public_score, private_score)
VALUES (STR_TO_DATE('2024-05-10 02:00:00', '%Y-%m-%d %H:%i:%s'), 'abap34', 0.8, 0.7);
INSERT INTO submitlog (post_date, username, public_score, private_score)
VALUES (STR_TO_DATE('2024-05-10 03:00:00', '%Y-%m-%d %H:%i:%s'), 'abap34', 0.3, 0.8);
INSERT INTO submitlog (post_date, username, public_score, private_score)
VALUES (STR_TO_DATE('2024-05-11 05:00:00', '%Y-%m-%d %H:%i:%s'), 'abap34', 0.1, 0.5);
INSERT INTO submitlog (post_date, username, public_score, private_score)
VALUES (STR_TO_DATE('2024-05-11 16:00:00', '%Y-%m-%d %H:%i:%s'), 'abap34', 0.06, 0.5);

