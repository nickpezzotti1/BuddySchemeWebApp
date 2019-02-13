CREATE TABLE Students
(
 k_number VARCHAR(255) NOT NULL,
 first_name  VARCHAR(255) NOT NULL,
 last_name VARCHAR(255) NOT NULL,
 degree_title VARCHAR(255) NOT NULL,
 year_study INT NOT NULL,
 gender VARCHAR(255) NOT NULL,
 password_hash VARCHAR(255) NOT NULL, 
 PRIMARY KEY(k_number)
);

CREATE TABLE Informations
(
 hobbies VARCHAR(255) NOT NULL,
 fields VARCHAR(255) NOT NULL,
 k_number VARCHAR(255) NOT NULL,
 FOREIGN KEY (k_number) REFERENCES Students(k_number)
);

CREATE TABLE Allocation
(
 mentor_k_number VARCHAR(255) NOT NULL,
 mentee_k_number VARCHAR(255) NOT NULL,
 PRIMARY KEY (mentor_k_number, mentee_k_number),
 FOREIGN KEY (mentor_k_number) REFERENCES Students(k_number),
 FOREIGN KEY (mentee_k_number) REFERENCES Students(k_number)
);
