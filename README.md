# SRM-Cal

## Description
This project generates events for Google Calendar by parsing the timetable and academic plan.

## Installation
To install the required dependencies, follow these steps:
```bash
    git clone https://github.com/kknives/srm-cal2.git
    cd srm-cal2
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
```
## Usage
To use the project, you need 
1. Download the single html file of your timetable from the SRMIST Student Portal.
2. Download the academic plan from the SRMIST Student Portal.
> Note: Be sure to check if the downloaded html loads properly in a browser. If it doesn't, use single-file extension in your browser to save the html file.

3. Either get added to ![kknives](https://github.com/kknives/kknives) google workspace or create a new project in the google cloud console and enable the google calendar api.

4. Place the credentials.json in the root of this project.

5. Parse timetable and academic plan to generate pickle
```bash
    python3 -m srmcal.parse --plan path/to/academic_plan --timetable path/to/timetable.html
```
6. If there are no errors, you will see a .pkl file in the root of the project. Run create.py to create the events and push to google calendar.
```bash
    python3 -m srmcal.create {odd/even} path/to/pickle_file
```
