DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

CREATE TABLE user_type
(
  id          SERIAL PRIMARY KEY,
  title       VARCHAR(64),
  description VARCHAR(512)
);

CREATE TABLE users
(
  id           SERIAL PRIMARY KEY,
  name         VARCHAR(64),
  email        VARCHAR(64),
  phone        VARCHAR(64),
  username     VARCHAR(64) NOT NULL,
  password     VARCHAR(64),
  user_type_id INTEGER REFERENCES user_type
);

CREATE TABLE doctor
(
  id         INTEGER NOT NULL PRIMARY KEY REFERENCES users,
  department VARCHAR(64)
);

CREATE TABLE patient_type
(
  id          SERIAL PRIMARY KEY,
  title       VARCHAR(64) NOT NULL,
  description VARCHAR(512)
);

CREATE TABLE patient
(
  id              INTEGER PRIMARY KEY REFERENCES users,
  patient_tag     VARCHAR(16) NOT NULL,
  age             INTEGER     NOT NULL,
  height          FLOAT       NOT NULL,
  sex             VARCHAR(1)  NOT NULL,
  patient_type_id INTEGER     NOT NULL REFERENCES patient_type
);

CREATE TABLE doctor_patient
(
  id         INTEGER PRIMARY KEY,
  patient_id INTEGER NOT NULL REFERENCES patient,
  doctor_id  INTEGER NOT NULL REFERENCES doctor
);

CREATE TABLE prehab_status
(
  id          SERIAL PRIMARY KEY,
  title       VARCHAR(64),
  description VARCHAR(512)
);

CREATE TABLE task_schedule (
  id         INTEGER PRIMARY KEY,
  title      VARCHAR(64),
  created_by INTEGER REFERENCES doctor,
  is_active  BOOLEAN DEFAULT TRUE
);

CREATE TABLE task_type
(
  id          SERIAL PRIMARY KEY,
  title       VARCHAR(64),
  description VARCHAR(512)
);

CREATE TABLE task (
  id              INTEGER PRIMARY KEY,
  title           VARCHAR(64),
  description     VARCHAR(512),
  multimedia_link VARCHAR(512),
  task_type_id    INTEGER REFERENCES task_type
);

CREATE TABLE schedule_week_task (
  id               INTEGER PRIMARY KEY,
  task_schedule_id INTEGER REFERENCES task_schedule,
  week_number      INTEGER NOT NULL,
  task_id          INTEGER REFERENCES task
);

CREATE TABLE prehab
(
  id                INTEGER PRIMARY KEY,
  init_date         DATE    NOT NULL                 DEFAULT now(),
  expected_end_date DATE,
  actual_end_date   DATE,
  surgery_date      DATE,
  week_numbers      INTEGER NOT NULL                 DEFAULT 4,
  status_id            INTEGER REFERENCES prehab_status DEFAULT 1
);

CREATE TABLE task_schedule_status
(
  id          SERIAL PRIMARY KEY,
  title       VARCHAR(64),
  description VARCHAR(512)
);

CREATE TABLE patient_task_schedule
(
  id                   INTEGER PRIMARY KEY,
  prehab_id            INTEGER REFERENCES prehab,
  week_number          INTEGER NOT NULL,
  day_number           INTEGER NOT NULL, -- 1 to 7: Sunday to Saturday
  task_id              INTEGER REFERENCES task,
  expected_repetitions INTEGER,
  actual_repetitions   INTEGER,
  status_id               INTEGER REFERENCES task_schedule_status DEFAULT 1
);

------------- POPULATE DATA ----------------
INSERT INTO user_type (title) VALUES
  ('Admin Privileges'),
  ('Doctor Privileges'),
  ('Patient Privileges');

INSERT INTO patient_type (title) VALUES
  ('Normal'),
  ('Diabetico'),
  ('Insuficiente Renal'),
  ('Desnutrido'),
  ('Vegetariano'),
  ('Hepático'),
  ('Hipertenso');

INSERT INTO users (name, email, phone, username, password, user_type_id)
VALUES ('Admin', 'admin@cubicon.xyz', NULL, 'admin', 'admin', 1);
INSERT INTO users (name, email, phone, username, password, user_type_id)
VALUES ('Sample Doctor', 'doctor@cubicon.xyz', NULL, 'doctor', 'doctor', 2);

INSERT INTO doctor (id, department) VALUES (2, 'Not Specified');

INSERT INTO prehab_status (title) VALUES
  ('PENDING'),
  ('ONGOING'),
  ('COMPLETED'),
  ('NOT COMPLETED');

INSERT INTO task_schedule_status (title) VALUES
  ('PENDING'),
  ('ONGOING'),
  ('COMPLETED'),
  ('NOT COMPLETED');

INSERT INTO task_type (title) VALUES
  ('RESPIRATÓRIO'),
  ('ENDURANCE'),
  ('RESISTÊNCIA');