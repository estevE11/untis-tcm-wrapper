import untis_tcm_wrapper
from gcal_manager import GCalManager

date = "2022-10-24"
res = untis_tcm_wrapper.get(1, 3182, date, 2)

data = untis_tcm_wrapper.parse(res)    

gcal = GCalManager()

for l in data:
    print(l.lesson_id)
    print(f"{l.room} {l.name}")
    print(f"{l.date} {l.start_time} {l.end_time}")
    print("-----")
    event = gcal.create_event(f"{l.room} {l.name}", l.teacher, l.start_time, l.end_time, l.date)
