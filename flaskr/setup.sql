CREATE TABLE Students
(
 k_number VARCHAR(255) NOT NULL,
 first_name  VARCHAR(255) NOT NULL,
 last_name VARCHAR(255) NOT NULL,
 degree_title VARCHAR(255) NOT NULL,
 year_study INT NOT NULL,
 gender VARCHAR(255) NOT NULL,
 is_mentor BIT(1) NOT NULL,
 email_confirmed BIT(1) NOT NULL DEFAULT b'0',
 password_hash VARCHAR(255) NOT NULL, 
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
