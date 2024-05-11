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
    public_score DOUBLE NOT NULL,
    private_score DOUBLE NOT NULL
);


-- ダミー
INSERT INTO posts (username, public_score, private_score) VALUES ('user1', 0.5, 0.5);
INSERT INTO posts (username, public_score, private_score) VALUES ('user2', 0.6, 0.6);
INSERT INTO posts (username, public_score, private_score) VALUES ('user2', 0.7, 0.7);
INSERT INTO posts (username, public_score, private_score) VALUES ('user4', 0.8, 0.8);