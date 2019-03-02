CREATE TABLE Student
(
 k_number VARCHAR(255) NOT NULL,
 first_name  VARCHAR(255) NOT NULL,
 last_name VARCHAR(255) NOT NULL,
 degree_title VARCHAR(255) NOT NULL,
 year_study INT NOT NULL,
 gender VARCHAR(255) NOT NULL,
 is_mentor TINYINT(1) NOT NULL,
 email_confirmed TINYINT(1) NOT NULL DEFAULT 0,
 password_hash VARCHAR(255) NOT NULL,
 is_admin TINYINT(1) NOT NULL DEFAULT 0,
 buddy_limit INT NOT NULL DEFAULT 1,
 PRIMARY KEY(k_number)
);

CREATE TABLE Hobby
(
 id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
 hobby_name VARCHAR(255) NOT NULL
);

CREATE TABLE Interest
(
 id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
 interest_name VARCHAR(255) NOT NULL
);

CREATE TABLE Student_Hobby
(
 hobby_id INT NOT NULL,
 k_number VARCHAR(255) NOT NULL,
 PRIMARY KEY (hobby_id, k_number),
 FOREIGN KEY (hobby_id) REFERENCES Hobby(id),
 FOREIGN KEY (k_number) REFERENCES Student(k_number)
);

CREATE TABLE Student_Interest
(
 interest_id INT NOT NULL,
 k_number VARCHAR(255) NOT NULL,
 PRIMARY KEY (interest_id, k_number),
 FOREIGN KEY (interest_id) REFERENCES Interest(id),
 FOREIGN KEY (k_number) REFERENCES Student(k_number)
);

CREATE TABLE Allocation
(
 mentor_k_number VARCHAR(255) NOT NULL,
 mentee_k_number VARCHAR(255) NOT NULL,
 PRIMARY KEY (mentor_k_number, mentee_k_number),
 FOREIGN KEY (mentor_k_number) REFERENCES Student(k_number),
 FOREIGN KEY (mentee_k_number) REFERENCES Student(k_number)
);

CREATE TABLE Allocation_Config
(
 age_weight INT NOT NULL,
 gender_weight INT NOT NULL,
 hobby_weight INT NOT NULL,
 interest_weight INT NOT NULL,
 table_lock BIT(1) PRIMARY KEY NOT NULL DEFAULT 0,
 CONSTRAINT lock_check CHECK (table_lock = 0)
);
