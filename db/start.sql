CREATE TABLE comments (
`id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
comment_id VARCHAR(16) not null,
comment_date varchar(16) not null,
ticker varchar(16) not null,
parent_post varchar(16) not null,
body varchar(10000) not null collate utf8mb4_general_ci,
score varchar(16) not null,
sentiment varchar(16) not null
);