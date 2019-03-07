CREATE TABLE Scheme
(
 scheme_id INT NOT NULL AUTO_INCREMENT,
 scheme_name VARCHAR(255) NOT NULL UNIQUE,
 is_active tinyint(1) NOT NULL DEFAULT 1,
 CONSTRAINT scheme_pk PRIMARY KEY (scheme_id, scheme_name)
);

CREATE TABLE Super_user
(
 email VARCHAR(255) NOT NULL,
 password_hash VARCHAR(255) NOT NULL,
 CONSTRAINT su_pk PRIMARY KEY (email)
);

CREATE TABLE Student
(
 scheme_id INT NOT NULL,
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
 CONSTRAINT student_pk PRIMARY KEY(scheme_id, k_number),
 CONSTRAINT scheme_fk FOREIGN KEY (scheme_id) REFERENCES Scheme(scheme_id)
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
 scheme_id INT NOT NULL,
 hobby_id INT NOT NULL,
 k_number VARCHAR(255) NOT NULL,
 CONSTRAINT student_hobby_pk PRIMARY KEY (scheme_id, hobby_id, k_number),
 CONSTRAINT student_hobby_fk FOREIGN KEY (scheme_id, k_number) REFERENCES Student(scheme_id, k_number),
 CONSTRAINT hobby_fk FOREIGN KEY (hobby_id) REFERENCES Hobby(id)
);

CREATE TABLE Student_Interest
(
 scheme_id INT NOT NULL,
 interest_id INT NOT NULL,
 k_number VARCHAR(255) NOT NULL,
 CONSTRAINT student_interest_pk PRIMARY KEY (scheme_id, interest_id, k_number),
 CONSTRAINT student_interest_fk FOREIGN KEY (scheme_id, k_number) REFERENCES Student(scheme_id, k_number),
 CONSTRAINT interest_fk FOREIGN KEY (interest_id) REFERENCES Interest(id)
);

CREATE TABLE Allocation
(
 scheme_id INT NOT NULL,
 mentor_k_number VARCHAR(255) NOT NULL,
 mentee_k_number VARCHAR(255) NOT NULL,
 CONSTRAINT allocation_pk PRIMARY KEY (scheme_id, mentor_k_number, mentee_k_number),
 CONSTRAINT mentor_fk FOREIGN KEY (scheme_id, mentor_k_number) REFERENCES Student(scheme_id, k_number),
 CONSTRAINT mentee_fk FOREIGN KEY (scheme_id, mentee_k_number) REFERENCES Student(scheme_id, k_number)

);

CREATE TABLE Allocation_Config
(
 scheme_id INT NOT NULL,
 age_weight INT NOT NULL,
 gender_weight INT NOT NULL,
 hobby_weight INT NOT NULL,
 interest_weight INT NOT NULL,
 table_lock BIT(1) NOT NULL DEFAULT 0,
 CONSTRAINT allocation_config_pk PRIMARY KEY (scheme_id, table_lock),
 CONSTRAINT scheme_config_fk FOREIGN KEY (scheme_id) REFERENCES Scheme(scheme_id),
 CONSTRAINT lock_check CHECK (table_lock = 0)
);




-- mock data for testing / development

INSERT INTO Super_user VALUES("buddyadmin@kcl.ac.uk", "pbkdf2:sha256:50000$igDdtEIs$17ab89312192f317e44bd9b29f2e04346519a6a06e79e4bfffc0156f44c7a13b");


INSERT INTO Scheme VALUES(0, "Computer Science 2018", 1);
INSERT INTO Scheme VALUES(0, "Law 2018", 1);
INSERT INTO Scheme VALUES(0, "Gender Studies 2018", 1);

INSERT INTO Allocation_Config VALUES(1, 50, 50, 50, 50, 0);
INSERT INTO Allocation_Config VALUES(2, 50, 50, 50, 50, 0);
INSERT INTO Allocation_Config VALUES(3, 50, 50, 50, 50, 0);


INSERT INTO Student VALUES(1, "k1234567", "John", "Doe", "Comp Sci Bsc", 1, "Male", 0, 1, "pbkdf2:sha256:50000$igDdtEIs$17ab89312192f317e44bd9b29f2e04346519a6a06e79e4bfffc0156f44c7a13b", 0, 3);
INSERT INTO Student VALUES(1, "k1234568", "Janye", "Roe", "Comp Sci Msc", 2, "Female", 1, 1, "pbkdf2:sha256:50000$igDdtEIs$17ab89312192f317e44bd9b29f2e04346519a6a06e79e4bfffc0156f44c7a13b", 1, 3);
INSERT INTO Student VALUES(1, "k1234569", "Jong-un", "Kim", "Robotics Bsc", 1, "Male", 0, 1,"pbkdf2:sha256:50000$igDdtEIs$17ab89312192f317e44bd9b29f2e04346519a6a06e79e4bfffc0156f44c7a13b", 0, 3);
INSERT INTO Student VALUES(1, "k6666666", "Bernie", "Sanders", "Comp Sci Phd", 3, "Male", 1, 1, "pbkdf2:sha256:50000$igDdtEIs$17ab89312192f317e44bd9b29f2e04346519a6a06e79e4bfffc0156f44c7a13b", 1, 3);

INSERT INTO Student VALUES(2, "k1234569", "Hillary", "Clinton", "Law and Politics Bsc", 1, "Female", 0, 1, "pbkdf2:sha256:50000$igDdtEIs$17ab89312192f317e44bd9b29f2e04346519a6a06e79e4bfffc0156f44c7a13b", 0, 3);
INSERT INTO Student VALUES(2, "k1234567", "John", "Doe", "Law Bsc", 1, "Male", 0, 1, "pbkdf2:sha256:50000$igDdtEIs$17ab89312192f317e44bd9b29f2e04346519a6a06e79e4bfffc0156f44c7a13b", 1, 3);
INSERT INTO Student VALUES(2, "k1234567", "Angela", "Merkle", "European Law Msc", 3, "Female", 1, 1, "pbkdf2:sha256:50000$igDdtEIs$17ab89312192f317e44bd9b29f2e04346519a6a06e79e4bfffc0156f44c7a13b", 1, 3);

INSERT INTO Student VALUES(3, "k7654321", "Donald", "Trump", "Womens Studies Phd", 4, "Male", 1, 1, "pbkdf2:sha256:50000$igDdtEIs$17ab89312192f317e44bd9b29f2e04346519a6a06e79e4bfffc0156f44c7a13b", 1, 3);
INSERT INTO Student VALUES(3, "k1234567", "John", "Doe", "Gender Studies Bsc", 1, "Male", 0, 1,"pbkdf2:sha256:50000$igDdtEIs$17ab89312192f317e44bd9b29f2e04346519a6a06e79e4bfffc0156f44c7a13b", 1, 3);











