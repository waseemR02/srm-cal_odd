#!/usr/bin/env python3
import pickle
import pandas as pd
import numpy as np
from srmcal.dayorder import DayOrder
from datetime import datetime


def main(plan: str = "302_plan.html", timetable: str = "timetable.html") -> None:
    tables = pd.read_html(plan)
    semsched = tables[1]
    months = len(semsched.columns)

    dayorders = dict()
    # breakpoint()
    for i, m in enumerate(range(0, months, 5)):
        # this_m = semsched.iloc[:,m:(m+4)]
        # this_m.rename(columns={this_m.columns[0]: "dt", this_m.columns[1]: "dow", this_m.columns[3]: "do"})
        this_month = semsched.iloc[:, m : (m + 4)]
        # breakpoint()
        for row in this_month.iterrows():
            if row[1][3] == "-" or np.isnan(row[1][0]):
                continue
            # print(row[1])
            dayorders[datetime(2024, i + 1, int(row[1][0]))] = [
                DayOrder.One,
                DayOrder.Two,
                DayOrder.Three,
                DayOrder.Four,
                DayOrder.Five,
            ][int(row[1][3]) - 1]
        # dayorders[datetime(this_month[0])]
        # mn_sched.append()

    # breakpoint()

    tables = pd.read_html(timetable)
    tt = tables[-2]
    exclude = set(
        [
            "18CSC350T",
            "18LEM110L",
            "nan",
            "18CSP104L",
            "18CSP105L",
            "18CSC307L",
            "18CSP104L",
            "Course Code",
        ]
    )
    courses = dict()
    for row_struct in tt.iterrows():
        row = row_struct[1]
        if len(row) < 8:
            continue
        if str(row[1]) in exclude:
            continue
        if str(row[10]) == "nan":
            continue
        for slot in row[8].split("-"):
            if slot == "":
                continue
            # print(f"{row[1]} - {slot}")
            courses[slot] = dict(location=row[10], name=row[2])
    # print(courses)
    return dayorders, courses


# breakpoint()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Parse SRM's timetable and plan")
    parser.add_argument("--plan", help="path to Academic Plan")
    parser.add_argument("--timetable", help="path to Timetable")
    args = vars(parser.parse_args())

    with open(str(datetime.now()) + ".pkl", "wb") as f:
        dayorders, courses = main(args["plan"], args["timetable"])
        pickle.dump((dayorders, courses), file=f)
