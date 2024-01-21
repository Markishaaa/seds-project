import pandas as pd
import random

def create_procedure_inserts(txt_name_filename, txt_cost_filename, sql_filename):
    # Read TXT files line by line
    with open(txt_name_filename, 'r') as txt_name_file, open(txt_cost_filename, 'r') as txt_cost_file:
        names_data = txt_name_file.readlines()
        costs_data = txt_cost_file.readlines()

    with open(sql_filename, 'w') as sql_file:
        for i in range(1, 232 + 1):
            procedure_name = names_data[i - 1].strip()
            procedure_cost = costs_data[i - 1].strip()

            insert_statement = f"INSERT INTO mtp_src_procedure (procedure_id, procedure_name, procedure_cost) VALUES ({i}, '{procedure_name}', {procedure_cost});\n"

            sql_file.write(insert_statement)

def create_organization_inserts(csv_filename, sql_filename):
    csv_data = pd.read_csv(csv_filename)

    with open(sql_filename, 'w') as sql_file:
        for i in range(len(csv_data)):
            row = csv_data.iloc[i]
            org_id = row['org_id']
            org_name = row['org_name']
            org_address = row['org_address']
            org_phone = row['org_phone']

            insert_statement = f"INSERT INTO mtp_src_organization (org_id, org_name, org_address, org_phone) VALUES ({org_id}, '{org_name}', '{org_address}', '{org_phone}');\n"

            sql_file.write(insert_statement)

def create_facility_inserts(csv_filename, sql_filename):
    csv_data = pd.read_csv(csv_filename)

    with open(sql_filename, 'w') as sql_file:
        for i in range(len(csv_data)):
            row = csv_data.iloc[i]
            facility_id = row['facility_id']
            facility_name = row['facility_name']
            facility_location = row['facility_location']

            # Generate random organization and city IDs
            org_id = random.randint(1, 100)
            city_id = random.randint(1, 25)

            insert_statement = f"INSERT INTO mtp_src_facility (facility_id, facility_name, facility_location, org_id, city_id) VALUES ({facility_id}, '{facility_name}', '{facility_location}', {org_id}, {city_id});\n"

            sql_file.write(insert_statement)

def read_department_roles_from_txt(txt_filename):
    department_roles_map = {}
    current_department = None
    current_roles = []

    with open(txt_filename, 'r') as txt_file:
        for line in txt_file:
            line = line.strip()

            if line.startswith('-'):
                # Found a new department
                if current_department is not None:
                    department_roles_map[current_department] = current_roles
                    current_roles = []

                current_department = line[1:].strip()
            elif current_department is not None:
                # Collect roles for the current department
                current_roles.append(line)

    # Add the last department and its roles
    if current_department is not None:
        department_roles_map[current_department] = current_roles

    return department_roles_map

def create_department_inserts(txt_filename, sql_filename):
    department_roles_map = read_department_roles_from_txt(txt_filename)

    with open(sql_filename, 'w') as sql_file:
        dept_id = 1
        for department, _ in department_roles_map.items():

            dept_insert_statement = f"INSERT INTO mtp_src_department (dept_id, dept_name) VALUES ({dept_id}, '{department}');\n"
            sql_file.write(dept_insert_statement)

            dept_id += 1

def create_staff_inserts(txt_filename, csv_filename, sql_filename):
    department_roles_map = read_department_roles_from_txt(txt_filename)

    staff_data = pd.read_csv(csv_filename)

    with open(sql_filename, 'w') as sql_file:
        for _, staff_info in staff_data.iterrows():
            staff_id = staff_info['staff_id']
            staff_first_name = staff_info['staff_first_name']
            staff_last_name = staff_info['staff_last_name']
            staff_role = random_staff_role(department_roles_map)
            dept_id = get_department_id_for_role(department_roles_map, staff_role)

            staff_insert_statement = (
                f"INSERT INTO mtp_src_staff (staff_id, staff_first_name, staff_last_name, staff_role, dept_id) "
                f"VALUES ({staff_id}, '{staff_first_name}', '{staff_last_name}', '{staff_role}', {dept_id});\n"
            )
            sql_file.write(staff_insert_statement)

def random_staff_role(department_roles_map):
    all_roles = [role for roles in department_roles_map.values() for role in roles]
    return random.choice(all_roles)

def get_department_id_for_role(department_roles_map, role):
    for index, (_, roles) in enumerate(department_roles_map.items()):
        if role in roles:
            return index + 1
        
def generate_department_organization_assignments():
    organizations = list(range(1, 100 + 1))
    departments = list(range(1, 32 + 1))

    assignments = []

    for org_id in organizations:
        # Randomly choose the number of departments for each organization (at least 20)
        num_departments = random.randint(20, 32)
        selected_departments = random.sample(departments, num_departments)

        # Create assignments for the selected departments and the current organization
        assignments.extend([(dept_id, org_id) for dept_id in selected_departments])

    return assignments

def create_department_organization_inserts(sql_filename):
    assignments = generate_department_organization_assignments()

    with open(sql_filename, 'w') as sql_file:
        for dept_id, org_id in assignments:
            sql_file.write(f"INSERT INTO mtp_src_department_organization (dept_id, org_id) VALUES ({dept_id}, {org_id});\n")

def create_patient_inserts(csv_filename, sql_filename):
    csv_data = pd.read_csv(csv_filename)

    with open(sql_filename, 'w') as sql_file:
        for i in range(len(csv_data)):
            row = csv_data.iloc[i]
            patient_id = row['patient_id']
            patient_first_name = row['patient_first_name']
            patient_last_name = row['patient_last_name']
            patient_dob = row['patient_dob']
            patient_address = row['patient_address']
            patient_phone = row['patient_phone']

            city_id = random.randint(1, 25)

            insert_statement = f"INSERT INTO mtp_src_patient (patient_id, patient_first_name, patient_last_name, patient_dob, patient_address, patient_phone, city_id) VALUES ({patient_id}, '{patient_first_name}', '{patient_last_name}', TO_DATE('{patient_dob}', 'YYYY-MM-DD'), '{patient_address}', '{patient_phone}', {city_id});\n"

            sql_file.write(insert_statement)

def create_appointment_inserts(csv_filename, sql_filename):
    csv_data = pd.read_csv(csv_filename)

    with open(sql_filename, 'w') as sql_file:
        for i in range(len(csv_data)):
            row = csv_data.iloc[i]
            appointment_id = row['appointment_id']
            appointment_date = row['appointment_date']
            appointment_time = row['appointment_time']
            datetime = appointment_date + " " + appointment_time

            patient_id = random.randint(1, 1000)
            staff_id = random.randint(1, 1000)
            procedure_id = random.randint(1, 232)

            insert_statement = f"INSERT INTO mtp_src_appointment (appointment_id, appointment_date, patient_id, staff_id, procedure_id) VALUES ({appointment_id}, TO_DATE('{datetime}', 'YYYY-MM-DD HH24:MI:SS'), {patient_id}, {staff_id}, {procedure_id});\n"

            sql_file.write(insert_statement)

def create_transaction_inserts(csv_filename, txt_filename, sql_filename):
    with open(txt_filename, 'r') as txt_file:
        amount_data = txt_file.readlines()

    csv_data = pd.read_csv(csv_filename)

    with open(sql_filename, 'w') as sql_file:
        for i in range(len(csv_data)):
            row = csv_data.iloc[i]
            transaction_id = row['transaction_id']
            transaction_date = row['transaction_date']
            transaction_time = row['transaction_time']
            datetime = transaction_date + " " + transaction_time

            randi = random.randint(0, 231)
            amount = amount_data[randi]

            patient_id = random.randint(1, 1000)
            staff_id = random.randint(1, 1000)
            procedure_id = random.randint(1, 232)

            insert_statement = f"INSERT INTO mtp_src_transaction (transaction_id, transaction_date, amount, patient_id, procedure_id, staff_id) VALUES ({transaction_id}, TO_DATE('{datetime}', 'YYYY-MM-DD HH24:MI:SS'), {amount}, {patient_id}, {procedure_id}, {staff_id});\n"

            sql_file.write(insert_statement)

create_procedure_inserts('../processed_data/p_procedure_names.txt', '../procedure_cost_data.txt', '../oltp_inserts/procedure_inserts.sql')
create_organization_inserts('../processed_data/p_organization_data.csv', '../oltp_inserts/organization_inserts.sql')
# region and city
create_facility_inserts('../facility_data.csv', '../oltp_inserts/facility_inserts.sql')
create_department_inserts('../processed_data/p_staff_roles_and_departments.txt', '../oltp_inserts/department_inserts.sql')
create_staff_inserts('../processed_data/p_staff_roles_and_departments.txt', '../processed_data/p_staff_data.csv', '../oltp_inserts/staff_inserts.sql')
create_department_organization_inserts('../oltp_inserts/organization_department_inserts.sql')
create_patient_inserts('../processed_data/p_patient_data.csv', '../oltp_inserts/patient_inserts.sql')
create_appointment_inserts('../appointment_data.csv', '../oltp_inserts/appointment_inserts.sql')
create_transaction_inserts('../transaction_dates_data.csv', '../procedure_cost_data.txt', '../oltp_inserts/transaction_inserts.sql')