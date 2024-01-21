import random

def generate_cost_values(num_values):
    # Define the distribution weights
    weights = [1] * len(range(100, 10001, 10))  # Adjust weights based on desired distribution

    # Generate random values based on weights
    values = random.choices(range(100, 10001, 10), weights=weights, k=num_values)

    return values

# Generate 232 values
cost_values = generate_cost_values(232)

# Print the first few values
print(cost_values[:10])

# Write the values to a file
output_file = '../procedure_cost_data.txt'
with open(output_file, 'w') as file:
    for value in cost_values:
        file.write(str(value) + '\n')