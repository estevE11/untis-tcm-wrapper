import requests

def get(element_type, element_id, date, format_id=2):
    headers = {'Cookie': 'traceId=66c8f4436e17811a4ac3bd33f9d9f85c3b924dd2; schoolname="_ZnVuZGFjacOzIHRlY25vY2FtcHVz"; schoolname="_ZnVuZGFjacOzIHRlY25vY2FtcHVz"; traceId=66c8f4436e17811a4ac3bd33f9d9f85c3b924dd2; JSESSIONID=3BA4296BE0CDFDAB57FD3E9E0CC32C2C'}

    req = requests.get("https://mese.webuntis.com/WebUntis/api/public/timetable/weekly/data?elementType=" + str(element_type) + "&elementId=" + str(element_id) + "&date=" + date + "&formatId=" + str(format_id), headers=headers)

    return req.text

def parse_elements(elements):
    print(elements)
    room_numbers = {}
    teacher_names = {}
    lesson_names = {}

class Lesson:
    def __init__(self):
        self.number = ""
        self.name = ""
        self.p = False

    def parse(self, obj):
        print(obj)