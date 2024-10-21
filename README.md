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
This script analyzes HTML data:

- orphans.py identifies licenses in SFDC that aren't applied on grid
- dedupe.py turns orphans.csv into deduped_orphans_output.csv for a model count + a la carte sub count
- refresh.py identifies total on-grid members / licenses

## To-Do
- [ ] add logic for all SKUs to scripts
- [ ] daybreak.py to auto-write model changes to the dealsheets
- [ ] Multi-grid support: licenses and object counts
- [ ] Compare known local applied licenses to object counts for utilization determination, more best-practice checks
- [ ] UDDI tokens output
- [ ] Unified .sh to parse PIANO to create assessment / recommendation

### Notes:
> [!CAUTION]
> Requires python3 and beautifulsoup4 (e.g. brew install python3 && pip install bs4

