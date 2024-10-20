import os
import re
import sys
import csv
from bs4 import BeautifulSoup

# Function to extract Salesforce licenses from the HTML file using regex pattern
def extract_sfdc_licenses_from_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Look for "LicenseKey =" followed by any combination of alphanumeric characters, slashes, and equal signs
    license_pattern = r"LicenseKey = ([\w+/=]+)"
    licenses = re.findall(license_pattern, content)

    return licenses

# Function to extract licenses from the database table
def extract_licenses_from_database_table(table):
    licenses = set()
    rows = table.find_all('tr')[1:]  # Skip the header row
    for row in rows:
        columns = row.find_all('td')
        if len(columns) > 3:
            # The LicenseString is in the 4th column (index 3) in the database section
            license_string = columns[3].text.strip()
            licenses.add(license_string)
    return licenses

# Function to identify and extract Database licenses
def extract_license_tables(soup):
    tables = soup.find_all('table')
    database_licenses = set()

    for table in tables:
        # Identify the Database table by checking for "License string" in the header
        if 'License string' in table.text:
            database_licenses = extract_licenses_from_database_table(table)

    return database_licenses

# Function to compare licenses and get the orphans
def get_orphan_licenses(salesforce_licenses, database_licenses):
    orphan_licenses = [license for license in salesforce_licenses if license not in database_licenses]
    return orphan_licenses

# Function to extract all associated data for orphan licenses by searching for relevant HTML structure
def extract_orphan_license_details(file_path, orphan_licenses):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')

    orphan_data = []

    # Loop over each orphan license and search for its surrounding structure
    for license in orphan_licenses:
        license_element = soup.find(string=re.compile(re.escape(license)))
        if license_element:
            # Find the corresponding table row or relevant structure containing other details
            row = license_element.find_parent('tr')
            if row:
                columns = row.find_all('td')
                if len(columns) >= 10:  # Ensure there are enough columns to capture all details
                    orphan_data.append({
                        'LicenseKey': license,
                        'SerialNumber': columns[1].text.strip(),
                        'Name': columns[2].text.strip(),
                        'ActivationID': columns[3].text.strip(),
                        'LicenseTechnology': columns[5].text.strip(),
                        'ParentSKU': columns[6].text.strip(),
                        'SoftwareSKU': columns[7].text.strip(),
                        'MaintenanceType': columns[8].text.strip(),
                        'MaintenanceEndDate': columns[9].text.strip(),
                        'Description': columns[10].text.strip() if len(columns) > 10 else ''
                    })

    return orphan_data

# Function to write the orphan licenses to a CSV file
def write_orphans_to_csv(orphan_licenses, file_name='orphans.csv'):
    # Specify the CSV headers
    headers = ['LicenseKey', 'SerialNumber', 'Name', 'ActivationID', 'LicenseTechnology', 'ParentSKU', 'SoftwareSKU', 'MaintenanceType', 'MaintenanceEndDate', 'Description']

    with open(file_name, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()  # Write the header
        for license in orphan_licenses:
            writer.writerow(license)  # Write each orphan license

# Function to process the HTML file and handle orphan license details
def process_html_file(file_path, verbose=False):
    try:
        with open(file_path, 'r') as file:
            html_content = file.read()

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract database licenses from the HTML structure
        database_licenses = extract_license_tables(soup)

        # Extract Salesforce licenses from the raw HTML content
        salesforce_licenses = extract_sfdc_licenses_from_html(file_path)

        if verbose:
            # Output the full list of local (database) licenses
            print("\n--- Local Database Licenses ---")
            for license in database_licenses:
                print(license)

            # Output the full list of Salesforce licenses
            print("\n--- Salesforce Licenses ---")
            for license in salesforce_licenses:
                print(license)

        # Compare and get orphan licenses (licenses in Salesforce but not applied locally)
        orphan_licenses = get_orphan_licenses(salesforce_licenses, database_licenses)

        if orphan_licenses:
            # Extract details for orphan licenses (surrounding data from HTML)
            orphan_details = extract_orphan_license_details(file_path, orphan_licenses)

            # Write the orphan licenses to 'orphans.csv'
            write_orphans_to_csv(orphan_details)

            # Print the total count of orphan licenses
            print(f"\nOrphan licenses have been written to 'orphans.csv'. Total orphans: {len(orphan_licenses)}")
        else:
            print("\nNo orphan licenses found. All Salesforce licenses are applied locally.")

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Entry point of the script
if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python maestro.py <html_filename> [-v]")
        sys.exit(1)

    html_file_path = sys.argv[1]
    verbose_flag = len(sys.argv) == 3 and sys.argv[2] == '-v'

    process_html_file(html_file_path, verbose=verbose_flag)
