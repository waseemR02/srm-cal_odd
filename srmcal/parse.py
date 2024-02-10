#!/usr/bin/env python3
import csv
import math
import pickle
import pandas as pd
import numpy as np
from srmcal.dayorder import DayOrder
from datetime import datetime

tables = pd.read_html("302_plan.html")
semsched = tables[1]
months = len(semsched.columns)

mn_sched = list()
inital_month = 1
dayorders = dict()
# breakpoint()
for i,m in enumerate(range(0, months, 5)):
    # this_m = semsched.iloc[:,m:(m+4)]
    # this_m.rename(columns={this_m.columns[0]: "dt", this_m.columns[1]: "dow", this_m.columns[3]: "do"})
    this_month = semsched.iloc[:,m:(m+4)]
    # breakpoint()
    for row in this_month.iterrows():
        if row[1][3] == '-' or np.isnan(row[1][0]):
            continue
        # print(row[1])
        dayorders[datetime(2024, i+1, int(row[1][0]))] = [DayOrder.One, DayOrder.Two,
                                                     DayOrder.Three, DayOrder.Four, DayOrder.Five][int(row[1][3])-1]
    # dayorders[datetime(this_month[0])]
    # mn_sched.append()

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
    pickle.dump((dayorders, courses), file=f)
