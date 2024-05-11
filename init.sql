GRANT ALL PRIVILEGES ON *.* TO 'root' 
    IDENTIFIED BY 'password' 
    WITH GRANT OPTION;

FLUSH PRIVILEGES;



CREATE DATABASE IF NOT EXISTS app_db;
USE app_db;

CREATE TABLE posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    post_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    username VARCHAR(255) NOT NULL,
    score1 INT,
    score2 INT
);


-- ダミー
INSERT INTO posts (username, score1, score2) VALUES ('user1', 10, 20);