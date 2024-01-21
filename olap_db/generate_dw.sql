-- Dimension Tables

CREATE SEQUENCE country_seq
    START WITH 1
    INCREMENT BY 1
    NOCACHE
    NOCYCLE;

CREATE TABLE mtp_dw_country (
    country_id      INTEGER DEFAULT country_seq.NEXTVAL PRIMARY KEY,
    country_name    VARCHAR(50) NOT NULL
);

CREATE TABLE mtp_dw_region (
    region_id       INTEGER PRIMARY KEY,
    reg_name        VARCHAR(100) NOT NULL,
    country_id      INTEGER REFERENCES mtp_dw_country(country_id)
);

CREATE TABLE mtp_dw_city (
    city_id         INTEGER PRIMARY KEY,
    city_name       VARCHAR(100) NOT NULL,
    region_id       INTEGER REFERENCES mtp_dw_region(region_id)
);

CREATE TABLE mtp_dw_patient (
    patient_id      INTEGER PRIMARY KEY,
    patient_name    VARCHAR(200) NOT NULL,
    patient_age     INTEGER NOT NULL,
    patient_address VARCHAR(200) NOT NULL,
    patient_phone   VARCHAR(20) NOT NULL,
    city_id         INTEGER REFERENCES mtp_dw_city(city_id)
);

CREATE TABLE mtp_dw_time (
    time_id      INTEGER NOT NULL PRIMARY KEY,
    day         INTEGER NOT NULL,
    month       VARCHAR2(20) NOT NULL,
    year        INTEGER NOT NULL,
    full_date   DATE NOT NULL,
    day_in_year   INTEGER NOT NULL,
    month_in_year INTEGER NOT NULL
);

CREATE TABLE mtp_dw_procedure (
    procedure_id    INTEGER PRIMARY KEY,
    procedure_name  VARCHAR(200) NOT NULL,
    procedure_cost  DECIMAL(10, 2) NOT NULL
);

CREATE TABLE mtp_dw_facility (
    facility_id       INTEGER PRIMARY KEY,
    facility_name     VARCHAR(200) NOT NULL,
    facility_location VARCHAR(200) NOT NULL,
    city_id           INTEGER REFERENCES mtp_dw_city(city_id)
);

CREATE TABLE mtp_dw_department_and_roles (
    staff_id        INTEGER PRIMARY KEY,
    staff_role      VARCHAR(150) NOT NULL,
    dept_name       VARCHAR(100) NOT NULL
);

CREATE TABLE mtp_dw_appointment (
    appointment_id   INTEGER PRIMARY KEY,
    appointment_date TIMESTAMP NOT NULL,
    patient_id       INTEGER REFERENCES mtp_dw_patient(patient_id),
    procedure_id     INTEGER REFERENCES mtp_dw_procedure(procedure_id),
    staff_id        INTEGER REFERENCES mtp_dw_department_and_roles(staff_id),
    time_id         INTEGER REFERENCES mtp_dw_time(time_id)
);