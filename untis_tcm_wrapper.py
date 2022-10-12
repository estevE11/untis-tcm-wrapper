import requests
import json

def get(element_type, element_id, date, format_id=2):
    headers = {'Cookie': 'traceId=66c8f4436e17811a4ac3bd33f9d9f85c3b924dd2; schoolname="_ZnVuZGFjacOzIHRlY25vY2FtcHVz"; schoolname="_ZnVuZGFjacOzIHRlY25vY2FtcHVz"; traceId=66c8f4436e17811a4ac3bd33f9d9f85c3b924dd2; JSESSIONID=3BA4296BE0CDFDAB57FD3E9E0CC32C2C'}

    url = "https://mese.webuntis.com/WebUntis/api/public/timetable/weekly/data?elementType=" + str(element_type) + "&elementId=" + str(element_id) + "&date=" + date + "&formatId=" + str(format_id)

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
                "name": el["longName"]
            }
        elif el["type"] == 4:
            room_numbers[str(el["id"])] = {
                "name": el["name"]
            }

    return room_numbers, teacher_names, lesson_names

class Lesson:
    def __init__(self):
        self.number = ""
        self.name = ""
        self.p = False

    def parse(self, obj):
        print(obj)