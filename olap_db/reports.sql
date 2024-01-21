-- How many patients are registered in each city
SELECT
    p.city_id,
    c.city_name,
    COUNT(p.patient_id) AS patient_count
FROM
    mtp_dw_patient p
JOIN
    mtp_dw_city c ON p.city_id = c.city_id
GROUP BY
    p.city_id, c.city_name
ORDER BY
    patient_count DESC;

-- -----------------------------------------------------------------------

-- How many appointments are made in each city
SELECT
    c.city_id,
    c.city_name,
    COUNT(a.appointment_id) AS appointment_count
FROM
    mtp_dw_appointment a
JOIN
    mtp_dw_patient p ON a.patient_id = p.patient_id
JOIN
    mtp_dw_city c ON p.city_id = c.city_id
GROUP BY
    c.city_id, c.city_name;

-- -----------------------------------------------------------------------

-- What are the most frequently needed procedures (by appointment)
SELECT
    pr.procedure_id,
    pr.procedure_name,
    COUNT(a.appointment_id) AS appointment_count
FROM
    mtp_dw_appointment a
JOIN
    mtp_dw_procedure pr ON a.procedure_id = pr.procedure_id
GROUP BY
    pr.procedure_id, pr.procedure_name
ORDER BY
    appointment_count DESC;
      
-- the most frequently needed procedures each year, starting 1.1.2018., ending 31.12.2023.
SELECT
    pr.procedure_id,
    pr.procedure_name,
    EXTRACT(YEAR FROM t.full_date) AS appointment_year,
    COUNT(a.appointment_id) AS appointment_count
FROM
    mtp_dw_appointment a
JOIN
    mtp_dw_procedure pr ON a.procedure_id = pr.procedure_id
JOIN
    mtp_dw_time t ON a.appointment_date >= t.full_date AND a.appointment_date < t.full_date + 1
WHERE
    t.full_date BETWEEN TO_DATE('2018-01-01', 'YYYY-MM-DD') AND TO_DATE('2023-12-31', 'YYYY-MM-DD')
GROUP BY
    pr.procedure_id, pr.procedure_name, EXTRACT(YEAR FROM t.full_date)
ORDER BY
    appointment_year, appointment_count DESC;

-- -----------------------------------------------------------------------

-- What is each facility's highest earning department
WITH RankedDepartments AS (
    SELECT
        f.facility_id,
        f.facility_name,
        d.staff_id,
        d.dept_name,
        SUM(p.procedure_cost) AS total_revenue,
        ROW_NUMBER() OVER (PARTITION BY f.facility_id ORDER BY SUM(p.procedure_cost) DESC) AS rank_within_facility
    FROM
        mtp_dw_appointment a
    JOIN
        mtp_dw_department_and_roles d ON a.staff_id = d.staff_id  -- getting dept_name
    JOIN
        mtp_dw_procedure p ON a.procedure_id = p.procedure_id  -- getting total_revenue
    JOIN
        mtp_dw_patient pa ON a.patient_id = pa.patient_id
    JOIN
        mtp_dw_city c ON pa.city_id = c.city_id
    JOIN
        mtp_dw_facility f ON f.city_id = c.city_id
    GROUP BY
        f.facility_id, f.facility_name, d.staff_id, d.dept_name
    ORDER BY
        f.facility_name
)
SELECT
    facility_id,
    facility_name,
    dept_name,
    total_revenue
FROM
    RankedDepartments
WHERE
    rank_within_facility = 1;