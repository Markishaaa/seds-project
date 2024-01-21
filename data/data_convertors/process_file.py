import pandas as pd

def double_single_quotes(value):
    if isinstance(value, str):
        if "'" in value:
            return value.replace("'", "''")
        if "&" in value:
            return value.replace("&", "&&")
    return value

def process_csv(input_file, output_file):
    df = pd.read_csv(input_file)

    # Apply the double_single_quotes function to each element in the DataFrame
    processed_df = df.map(double_single_quotes)

    # Write the processed DataFrame to a new CSV file
    processed_df.to_csv(output_file, index=False)

def process_txt(input_file_path, output_file_path):
    with open(input_file_path, 'r') as infile, open(output_file_path, 'w') as outfile:
        for line in infile:
            processed_line = line.replace("'", "''")
            processed_line = processed_line.replace("&", "&&")
            outfile.write(processed_line)

process_csv('../patient_data.csv', '../processed_data/p_patient_data.csv')
process_txt('../procedure_names.txt', '../processed_data/p_procedure_names.txt')
process_csv('../organization_data.csv', '../processed_data/p_organization_data.csv')
process_csv('../staff_data.csv', '../processed_data/p_staff_data.csv')
process_txt('../staff_roles_and_departments.txt', '../processed_data/p_staff_roles_and_departments.txt')