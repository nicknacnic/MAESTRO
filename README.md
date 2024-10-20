# MAESTRO 🎹
PIANO is a tool used internally by Infoblox SAs to ascertain health of a grid deployment.  

PIANO stands for Proactive Infoblox Assessments for NIOS Operations, and is targeted towards grid reviews as opposed to the cloud-managed or deployed Infoblox products. 

MAESTRO is a toolset used to enhance PIANO's purview.

## Usage
> [!WARNING]
> PIANO is required to run on each individual NIOS GM DB backup, so if you are a multi-grid customer, 'orphaned' licenses may be on another grid...

### Installation:
Pull the repo.
```git clone https://github.com/nicknacnic/MAESTRO.git```

Run the script.
```python orphans.py PIANO.html``` or ```python orphans.py PIANO.html > out.txt```

> [!TIP]
> Use -v for verbose mode. It will output Grid and SFDC licenses in the GUI. You can then pipe the output to a text file.

### How It Works:
This script analyzes HTML table header data:

License Extraction:

The script parses an HTML file to extract Salesforce licenses (identified by their LicenseKey values) using regex.
It also extracts locally applied database licenses from an HTML table in the same file using BeautifulSoup.
License Comparison:

The extracted Salesforce licenses are compared to the locally applied database licenses to find "orphan licenses" (licenses that exist in Salesforce but are not present locally).
Orphan Data Extraction:

Once orphan licenses are identified, the script extracts additional details (e.g., SerialNumber, ActivationID, LicenseTechnology, etc.) by locating the corresponding HTML elements.
CSV Generation:

The script writes all orphan license details into a CSV file named orphans.csv with the following fields:
LicenseKey
SerialNumber
Name
ActivationID
LicenseTechnology
ParentSKU
SoftwareSKU
MaintenanceType
MaintenanceEndDate
Description
Output:

A total count of orphan licenses is displayed in the terminal.
The CSV file (orphans.csv) contains all the detailed information for each orphan license.

## To-Do
- [ ] Multi-grid support, licenses and object counts
- [ ] Compare known local applied licenses to object counts for utilization determination, more best-practice checks
- [ ] (Offline / private) UDDI tokens output
- [ ] Refresh X6 output 😎

### Notes:
> [!CAUTION]
> Requires python3 and beautifulsoup4 (e.g. brew install python3 && pip install bs4

