import os
import sys
import csv
from bs4 import BeautifulSoup
from collections import defaultdict, Counter

# Function to extract member information from the HTML file
def extract_members_by_type_and_model(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')

    # Find the table with id "device-info"
    table = soup.find('table', {'id': 'device-info'})

    if not table:
        print("Error: Device Info table not found in the HTML.")
        return None

    # Extract the rows of the table (excluding the header)
    rows = table.find_all('tr')[1:]

    # Initialize a counter for member types and models
    member_data = defaultdict(Counter)

    # Iterate through each row and extract the hardware platform and model type
    for row in rows:
        columns = row.find_all('td')
        if len(columns) > 2:
            hardware_platform = columns[1].text.strip()  # Column 2 contains the hardware platform
            model_type = columns[0].text.strip()         # Column 1 contains the model type (e.g., 2205, 1405)
            member_data[hardware_platform][model_type] += 1

    return member_data

# Function to display member counts
def display_counts(member_data):
    # Display member counts
    total_members = sum(sum(model_counter.values()) for model_counter in member_data.values())
    print(f"Total Members: {total_members}")

    print("\nBreakdown by Member Type and Model:")
    for hardware_platform, model_counter in member_data.items():
        print(f"\n{hardware_platform}:")
        for model_type, count in model_counter.items():
            print(f"  {model_type}: {count}")

# Main function to run the script
def main():
    if len(sys.argv) < 2:
        print("Usage: python member_count.py <html_filename>")
        return

    html_file_path = sys.argv[1]

    # Extract members by type and model from the HTML file
    member_data = extract_members_by_type_and_model(html_file_path)
    
    if member_data is None:
        return

    # Display the member counts
    display_counts(member_data)

if __name__ == "__main__":
    main()
