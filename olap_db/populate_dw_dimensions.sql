INSERT INTO mtp_dw_country (country_name)
SELECT DISTINCT country_name
FROM mtp_src_region;

INSERT INTO mtp_dw_region (region_id, reg_name, country_id)
SELECT DISTINCT
    r.region_id,
    r.reg_name,
    c.country_id
FROM
    mtp_src_region r
    JOIN mtp_dw_country c ON r.country_name = c.country_name;

INSERT INTO mtp_dw_city (city_id, city_name, region_id)
SELECT DISTINCT city_id, city_name, region_id
FROM mtp_src_city;

INSERT INTO mtp_dw_patient (patient_id, patient_name, patient_age, patient_address, patient_phone, city_id)
SELECT DISTINCT
    patient_id,
    patient_first_name || ' ' || patient_last_name AS patient_name,
    TRUNC(MONTHS_BETWEEN(SYSDATE, TO_DATE(patient_dob, 'DD-MON-YY')) / 12) AS patient_age,
    patient_address,
    patient_phone,
    city_id
FROM mtp_src_patient;

INSERT INTO mtp_dw_procedure (procedure_id, procedure_name, procedure_cost)
SELECT DISTINCT procedure_id, procedure_name, procedure_cost
FROM mtp_src_procedure;

INSERT INTO mtp_dw_facility (facility_id, facility_name, facility_location, city_id)
SELECT DISTINCT facility_id, facility_name, facility_location, city_id
FROM mtp_src_facility;

INSERT INTO mtp_dw_department_and_roles (staff_id, staff_role, dept_name)
SELECT
    s.staff_id,
    s.staff_role,
    d.dept_name
FROM
    mtp_src_staff s
JOIN
    mtp_src_department d ON s.dept_id = d.dept_id;

INSERT INTO mtp_dw_appointment (appointment_id, appointment_date, patient_id, procedure_id, staff_id)
SELECT DISTINCT appointment_id, appointment_date, patient_id, procedure_id, staff_id
FROM mtp_src_appointment;

INSERT INTO mtp_dw_time (time_id, day, month, year, full_date, day_in_year, month_in_year)
SELECT
    TO_NUMBER(TO_CHAR(date '2018-01-01' + level - 1, 'YYYYMMDD')),
    TO_NUMBER(TO_CHAR(date '2018-01-01' + level - 1, 'DD')),
    TO_CHAR(date '2018-01-01' + level - 1, 'MONTH'),
    TO_NUMBER(TO_CHAR(date '2018-01-01' + level - 1, 'YYYY')),
    date '2018-01-01' + level - 1,
    TO_NUMBER(TO_CHAR(date '2018-01-01' + level - 1, 'DDD')),
    TO_NUMBER(TO_CHAR(date '2018-01-01' + level - 1, 'MM'))
FROM
    dual
CONNECT BY
    level <= 6 * 365;
    
commit;