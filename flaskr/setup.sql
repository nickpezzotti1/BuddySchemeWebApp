CREATE TABLE Students
(
 k_number VARCHAR(255) NOT NULL,
 first_name  VARCHAR(255) NOT NULL,
 last_name VARCHAR(255) NOT NULL,
 degree_title VARCHAR(255) NOT NULL,
 year_study INT NOT NULL,
 gender VARCHAR(255) NOT NULL,
 is_mentor tinyint(1) NOT NULL,
 email_confirmed tinyint(1) NOT NULL DEFAULT 0,
 password_hash VARCHAR(255) NOT NULL,
 is_admin tinyint(1) NOT NULL, DEFAULT 0,
 buddy_limit int NOT NULL, DEFAULT 1,
 PRIMARY KEY(k_number)
);

CREATE TABLE Hobbies
(
 hobby VARCHAR(255) NOT NULL,
 k_number VARCHAR(255) NOT NULL,
 FOREIGN KEY (k_number) REFERENCES Students(k_number),
 PRIMARY KEY (hobby, k_number)
);

CREATE TABLE Interests
(
 interest VARCHAR(255) NOT NULL,
 k_number VARCHAR(255) NOT NULL,
 FOREIGN KEY (k_number) REFERENCES Students(k_number),
 PRIMARY KEY (interest, k_number)
);

CREATE TABLE Allocation
(
 mentor_k_number VARCHAR(255) NOT NULL,
 mentee_k_number VARCHAR(255) NOT NULL,
 PRIMARY KEY (mentor_k_number, mentee_k_number),
 FOREIGN KEY (mentor_k_number) REFERENCES Students(k_number),
 FOREIGN KEY (mentee_k_number) REFERENCES Students(k_number)
);

CREATE TABLE Allocation_Config
(
 age_weight INT NOT NULL,
 gender_weight INT NOT NULL,
 hobby_weight INT NOT NULL,
 interest_weight INT NOT NULL,
 mentee_limit INT NOT NULL,
 table_lock BIT(1) PRIMARY KEY NOT NULL DEFAULT 0,
 CONSTRAINT lock_check CHECK (table_lock = 0)
);
