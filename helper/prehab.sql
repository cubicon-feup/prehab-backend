CREATE TABLE type_user 
(
	id serial PRIMARY KEY,
    description varchar(50),
    typeUser int NOT NULL
);

CREATE TABLE auth_user 
(
	id serial PRIMARY KEY,
    name varchar(50),
    email varchar(50),
    password varchar(50),
    typeUser int NOT NULL,
    CONSTRAINT link_user_to_type FOREIGN KEY (typeUser)
	    REFERENCES type_user(id)
	    ON DELETE CASCADE    
	    ON UPDATE CASCADE  
);

CREATE TABLE doctor
(
    id int NOT NULL PRIMARY KEY,
    department varchar(50),
    CONSTRAINT link_doctor_to_user FOREIGN KEY (id)
	    REFERENCES auth_user(id)
	    ON DELETE CASCADE    
	    ON UPDATE CASCADE  
);

CREATE TABLE patient_type
(
    id serial PRIMARY KEY,
    description varchar(50),
    typePatient int Default 1
);

CREATE TABLE patient
(
    id int NOT NULL PRIMARY KEY,
    tag varchar(50) NULL,
    age int NOT NULL,
    alt float NOT NULL,
    sex char NOT NULL,
    typePatient int NOT NULL,

    CONSTRAINT link_patient_to_user FOREIGN KEY (id)
	    REFERENCES auth_user(id)
	    ON DELETE CASCADE    
	    ON UPDATE CASCADE,
    CONSTRAINT link_patient_to_type FOREIGN KEY (typePatient)
	    REFERENCES patient_type(id)
	    ON DELETE CASCADE    
	    ON UPDATE CASCADE
);

INSERT INTO type_user (description, typeUser) VALUES 
( 'Admin Privileges', 1 ), 
( 'Doctor Privileges' , 2), 
( 'Patient Privileges', 3);

INSERT INTO patient_type (description, typePatient) VALUES 
( 'Normal', 1 ), 
( 'Diabetico', 2), 
( 'Insuficiente Renal', 3), 
( 'Desnutrido', 4),
( 'Vegetariano', 5),
( 'Hepático', 6),
( 'Hipertenso', 7);

INSERT INTO auth_user (name, email, password, typeUser) VALUES ( 'admin', 'cubicon@fe.up.pt', 'supereasy', 1);

INSERT INTO auth_user (name, email, password, typeUser) VALUES ( 'Doctor_1', 'doctor@fe.up.pt', 'supereasy', 2);

INSERT INTO doctor (id, department) VALUES ( 2, 'Brain');
