from enum import Enum
from collections import namedtuple
from datetime import datetime, time


class DayOrder(Enum):
    One = 1
    Two = 2
    Three = 3
    Four = 4
    Five = 5


Slot = namedtuple("Slot", ["do", "start", "to", "place", "subject"])


def add_event(slot, calendar, day, time_start, time_end):
    # return calendar.save_event(dtstart=datetime.combine(day, time_start))
    return {
        "subject": slot.subject,
        "start date": day,
        "end date": day,
        "start time": slot.start,
        "end time": slot.to,
        "location": slot.place,
    }


even_slots = dict()
even_slots[DayOrder.One] = "P1,P2,P3,P4,P5,A,A,F,F,G,L11,L12".split(",")
even_slots[DayOrder.Two] = "B,B,G,G,A,P16,P17,P18,P19,P20,L21,L22".split(",")
even_slots[DayOrder.Three] = "P21,P22,P23,P24,P25,C,C,A,D,B,L31,L32".split(",")
even_slots[DayOrder.Four] = "D,D,B,E,C,P36,P37,P38,P39,P40,L41,L42".split(",")
even_slots[DayOrder.Five] = "P41,P42,P43,P44,P45,E,E,C,F,D,L51,L52".split(",")

odd_slots = dict()
odd_slots[DayOrder.One] = "A,A,F,F,G,P6,P7,P8,P9,P10,L11,L12".split(",")
odd_slots[DayOrder.Two] = "P11,P12,P13,P14,P15,B,B,G,G,A,L21,L22".split(",")
odd_slots[DayOrder.Three] = "C,C,A,D,B,P26,P27,P28,P29,P30,L31,L32".split(",")
odd_slots[DayOrder.Four] = "P31,P32,P33,P34,P35,D,D,B,E,C,L41,L42".split(",")
odd_slots[DayOrder.Five] = "E,E,C,F,D,P46,P47,P48,P49,P50,L51,L52".split(",")

TimeSlot = namedtuple("TimeSlot", ["start", "end"])
time_slots = (
    TimeSlot(time(8, 00), time(8, 50)),
    TimeSlot(time(8, 50), time(9, 40)),
    TimeSlot(time(9, 45), time(10, 35)),
    TimeSlot(time(10, 40), time(11, 30)),
    TimeSlot(time(11, 35), time(12, 25)),
    TimeSlot(time(12, 30), time(13, 20)),
    TimeSlot(time(13, 25), time(14, 15)),
    TimeSlot(time(14, 20), time(15, 10)),
    TimeSlot(time(15, 10), time(16, 00)),
    TimeSlot(time(16, 00), time(16, 50)),
    TimeSlot(time(16, 50), time(17, 30)),
    TimeSlot(time(17, 30), time(18, 10)),
)

assert len(time_slots) == len(even_slots[DayOrder.One])


class DayOrderSched:
    def __init__(self, do: DayOrder, sched: dict, batch: str, time_zone="Asia/Kolkata"):
        self.day_order = do
        if batch == "even":
            self.slots = even_slots[self.day_order]
        else:
            self.slots = odd_slots[self.day_order]
        self.times = time_slots
        self.sched = sched
        self.time_zone = time_zone

    def add_events(self, day: datetime):
        events = []
        for t, s in zip(self.times, self.slots):
            if s not in self.sched:
                continue
            events.append(
                {
                    "summary": self.sched[s]["name"],
                    "start": {
                        "dateTime": datetime.combine(day, t.start).isoformat(),
                        "timeZone": self.time_zone,
                    },
                    "end": {
                        "dateTime": datetime.combine(day, t.end).isoformat(),
                        "timeZone": self.time_zone,
                    },
                    "location": self.sched[s]["location"],
                }
            )
        return events
