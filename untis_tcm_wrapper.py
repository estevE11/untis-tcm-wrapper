from regex import B
import requests
import json
import datetime

PRACTIC = "G102"

def get(element_type, element_id, date, format_id=2):
    headers = {'Cookie': 'traceId=66c8f4436e17811a4ac3bd33f9d9f85c3b924dd2; schoolname="_ZnVuZGFjacOzIHRlY25vY2FtcHVz"; schoolname="_ZnVuZGFjacOzIHRlY25vY2FtcHVz"; traceId=66c8f4436e17811a4ac3bd33f9d9f85c3b924dd2; JSESSIONID=3BA4296BE0CDFDAB57FD3E9E0CC32C2C'}

    url = "https://mese.webuntis.com/WebUntis/api/public/timetable/weekly/data?elementType=" + str(element_type) + "&elementId=" + str(element_id) + "&date=" + date + "&formatId=" + str(format_id)
    print(url)
    req = requests.get(url, headers=headers)

    return json.loads(req.text)["data"]["result"]["data"]

def parse_elements(elements):
    room_numbers = {}
    teacher_names = {}
    lesson_names = {}

    for el in elements:
        if el["type"] == 2:
            teacher_names[str(el["id"])] = {
                "name": el["longName"]
            }
        elif el["type"] == 3:
            lesson_names[str(el["id"])] = {
                "name": el["longName"],
                "id": el["id"]
            }
        elif el["type"] == 4:
            room_numbers[str(el["id"])] = {
                "name": el["name"]
            }

    return room_numbers, teacher_names, lesson_names


def parse(data):
    res = []

    rooms, teachers, lessons = parse_elements(data["elements"])

    lessons_obj = data["elementPeriods"][str(data["elementIds"][0])]

    for it in lessons_obj:
        if PRACTIC in it["lessonText"] or it["lessonText"] == "":
            obj = {}
            for el in it["elements"]:
                if el["type"] == 2:
                    obj["teacher"] = teachers[str(el["id"])]["name"]
                elif el["type"] == 3:
                    obj["name"] = lessons[str(el["id"])]["name"][7:]
                    obj["lesson_id"] = lessons[str(el["id"])]["id"]
                elif el["type"] == 4:
                    obj["room"] = rooms[str(el["id"])]["name"].split("-")[1]

            obj["start_time"] = split_time(it["startTime"])
            obj["end_time"] = split_time(it["endTime"])
            obj["date"] = split_date(it["date"])
            res.append(Lesson(obj))
    
    res = group_lessons(res)

    return res

def group_lessons(lessons):
    res = []

    curr = None
    i = 0
    while i < len(lessons)-1:
        curr = lessons[i]
        nxt = lessons[i+1]
        if curr.lesson_id == nxt.lesson_id and curr.date == nxt.date and lessons_together(curr, nxt):
            lesson = join_lessons(curr, nxt)
            res.append(lesson)
            i += 1
        else:
            res.append(curr)
        i += 1
    return res

def join_lessons(l0, l1):
    l0.end_time = l1.end_time
    return l0

def lessons_together(l0, l1):
    l0_et_h = int(l0.end_time.split(":")[0])
    l0_et_m = int(l0.end_time.split(":")[1])
    l1_st_h = int(l1.start_time.split(":")[0])
    l1_st_m = int(l1.start_time.split(":")[1])
    a = datetime.datetime(2022, 10, 10, l0_et_h, l0_et_m)
    b = datetime.datetime(2022, 10, 10, l1_st_h, l1_st_m)
    c = a-b
    return (c.total_seconds() / 60) < 15

class Lesson:
    def __init__(self, lesson_data):
        self.lesson_id = lesson_data["lesson_id"]
        self.name = lesson_data["name"]
        self.room = lesson_data["room"]
        self.teacher = lesson_data["teacher"]
        self.p = False
        self.start_time = str(lesson_data["start_time"])
        self.end_time = str(lesson_data["end_time"])
        self.date = str(lesson_data["date"])

def split_date(d):
    d = str(d)
    return d[0:4] + "-" + d[4:6] + "-" + d[6:8]

def split_time(t):
    t = str(t)
    if len(t) == 3:
        return f"{t[0:1]}:{t[1:]}:00"
    return f"{t[0:2]}:{t[2:]}:00"
    