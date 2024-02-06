#!/usr/bin/env python3
import csv
import math
import pickle
import pandas as pd
from datetime import datetime

tables = pd.read_html("302_plan.html")
semsched = tables[1]
months = len(semsched.columns)

mn_sched = list()
inital_month = 1
dayorders = dict()
for i,m in enumerate(range(0, months, 5)):
    # this_m = semsched.iloc[:,m:(m+4)]
    # this_m.rename(columns={this_m.columns[0]: "dt", this_m.columns[1]: "dow", this_m.columns[3]: "do"})
    mn_sched.append(semsched.iloc[:,m:(m+4)])

# breakpoint()

tables = pd.read_html("timetable.html")
tt = tables[-2]
exclude = set(["18CSC350T", "18LEM110L", "nan", "18CSP104L", "18CSC307L", "Course Code"])
courses = dict()
for row_struct in tt.iterrows():
    row = row_struct[1]
    if len(row) < 8:
        continue
    if str(row[1]) in exclude:
        continue
    for slot in row[8].split('-'):
        courses[slot] = dict(location=row[10], name=row[2])

# breakpoint()

with open(str(datetime.now())+".pkl", "wb") as f:
    pickle.dump((mn_sched, courses), file=f)
