-- OLTP Database for Healthcare Network Management

CREATE TABLE mtp_src_organization (
    org_id          INTEGER PRIMARY KEY,
    org_name        VARCHAR(200) NOT NULL,
    org_address     VARCHAR(200) NOT NULL,
    org_phone       VARCHAR(20) NOT NULL
);

CREATE TABLE mtp_src_department (
    dept_id         INTEGER PRIMARY KEY,
    dept_name       VARCHAR(100) NOT NULL
);

CREATE TABLE mtp_src_department_organization (
    dept_id INTEGER REFERENCES mtp_src_department(dept_id),
    org_id INTEGER REFERENCES mtp_src_organization(org_id),
    PRIMARY KEY (dept_id, org_id)
);

CREATE TABLE mtp_src_staff (
    staff_id        INTEGER PRIMARY KEY,
    staff_first_name VARCHAR(100) NOT NULL,
    staff_last_name VARCHAR(100) NOT NULL,
    staff_role      VARCHAR(150) NOT NULL,
    dept_id         INTEGER REFERENCES mtp_src_department(dept_id)
);

CREATE TABLE mtp_src_region (
    region_id       INTEGER PRIMARY KEY,
    reg_name        VARCHAR(100) NOT NULL,
    country_name    VARCHAR(50) NOT NULL
);

CREATE TABLE mtp_src_city (
    city_id         INTEGER PRIMARY KEY,
    city_name       VARCHAR(100) NOT NULL,
    region_id       INTEGER REFERENCES mtp_src_region(region_id)
);

CREATE TABLE mtp_src_patient (
    patient_id      INTEGER PRIMARY KEY,
    patient_first_name VARCHAR(100) NOT NULL,
    patient_last_name VARCHAR(100) NOT NULL,
    patient_dob     DATE NOT NULL,
    patient_address VARCHAR(200) NOT NULL,
    patient_phone   VARCHAR(20) NOT NULL,
    city_id         INTEGER REFERENCES mtp_src_city(city_id)
);

CREATE TABLE mtp_src_procedure (
    procedure_id    INTEGER PRIMARY KEY,
    procedure_name  VARCHAR(200) NOT NULL,
    procedure_cost  DECIMAL(10, 2) NOT NULL
);

CREATE TABLE mtp_src_appointment (
    appointment_id  INTEGER PRIMARY KEY,
    appointment_date TIMESTAMP NOT NULL,
    patient_id      INTEGER REFERENCES mtp_src_patient(patient_id),
    staff_id        INTEGER REFERENCES mtp_src_staff(staff_id),
    procedure_id    INTEGER REFERENCES mtp_src_procedure(procedure_id)
);

CREATE TABLE mtp_src_transaction (
    transaction_id  INTEGER PRIMARY KEY,
    transaction_date TIMESTAMP NOT NULL,
    amount          DECIMAL(10, 2) NOT NULL,
    patient_id      INTEGER REFERENCES mtp_src_patient(patient_id),
    procedure_id    INTEGER REFERENCES mtp_src_procedure(procedure_id),
    staff_id        INTEGER REFERENCES mtp_src_staff(staff_id)
);

CREATE TABLE mtp_src_facility (
    facility_id     INTEGER PRIMARY KEY,
    facility_name   VARCHAR(200) NOT NULL,
    facility_location VARCHAR(200) NOT NULL,
    org_id          INTEGER REFERENCES mtp_src_organization(org_id),
    city_id         INTEGER REFERENCES mtp_src_city(city_id)
);