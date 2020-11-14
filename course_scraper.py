import urllib.request
import sys
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


class Course:
    def __init__(self, courseName):
        self.courseName = courseName


def scraper(subject, semester):
    url = "https://www.asc.ohio-state.edu/barrett.3/schedule/%s/%s.txt" % (subject, semester)
    file = urllib.request.urlopen(url)
    i = 0

    course_set = []
    course_list = []

    for line in file:
        if i < 5:
            i += 1
            continue
        decoded_line = str(line.decode("utf-8")).strip()
        if len(decoded_line) == 0:
            continue

        if decoded_line.split()[0] != "CSE":
            continue
        course_name = str(decoded_line.split()[0] + decoded_line.split()[1])

        if course_name not in course_set:
            print(course_name)
            course_set.append(course_name)
            course = Course(course_name)
            course_list.append(course)

    return course_list


# MAIN
cred = credentials.Certificate('osugrades-287d6-firebase-adminsdk-85eqn-e03289bdcc.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

subject_code = sys.argv[1]  # CSE
semester_code = sys.argv[2]  # semseter number 1208

course_list = scraper(subject_code, semester_code)

for course in course_list:
    doc_ref = db.collection('courses').document(course.courseName)
    doc_ref.set({
        'averageGpa': 0.00,
        'course': course.courseName,
        'rating': 0,
        'reported': 0
    })

