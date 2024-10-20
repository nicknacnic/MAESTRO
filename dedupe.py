import pandas as pd

# Load the CSV file
file_path = 'orphans.csv'  # Replace this with the correct file path
data = pd.read_csv(file_path)

# Step 1: Extract the model from 'ParentSKU' if 'Model' column is missing
if 'Model' not in data.columns:
    data['Model'] = data['ParentSKU'].str.extract(r'-(\d+)$')

# Step 2: De-duplicate NS1 licenses
# Filter for NS1 licenses
ns1_licenses = data[data['ParentSKU'] == 'IB-SWTL-NS1']
# Remove duplicates based on SerialNumber
ns1_deduped = ns1_licenses.drop_duplicates(subset=['SerialNumber'])

# Step 3: Track base models and assign licenses to them
current_base_model = None
base_model_assignment = []

# Loop through the rows to assign base models to each license
for index, row in data.iterrows():
    if 'BASE' in row['ParentSKU']:
        current_base_model = row['Model']
    base_model_assignment.append(current_base_model)

# Add a new column for the assigned base model
data['AssignedBaseModel'] = base_model_assignment

# Step 4: Replace original NS1 data with the deduplicated version
data_without_ns1 = data[data['ParentSKU'] != 'IB-SWTL-NS1']
data_final = pd.concat([data_without_ns1, ns1_deduped])

# Step 5: Group the data by AssignedBaseModel and ParentSKU
final_output = data_final.groupby(['AssignedBaseModel', 'ParentSKU']).size().unstack(fill_value=0)

# Step 6: Output the final CSV
output_file = 'deduped_orphans_output.csv'  # You can change this to your desired output file name
final_output.to_csv(output_file)

print(f"Processed file saved as {output_file}")
