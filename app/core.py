import os.path
import json

from utils import inputs


# Variables
CONFIG_DIR = './configs'
COURSES = 'courses.json'
LESSONS = 'lessons.json'

if not os.path.isdir(CONFIG_DIR):
    os.makedirs(CONFIG_DIR)


def get_courses() -> list[dict]:
    return list(filter(lambda x: not x['skip'], get_saved_courses()))
    # courses = []
    # for course in get_saved_courses():
    #     if not course['skip']:
    #         courses.append(course)
    # return courses


def get_saved_courses() -> list[dict]:
    path = os.path.join(CONFIG_DIR, COURSES)
    return inputs.open_json_file(path)


def get_saved_course(_id: int) -> dict or None:
    courses = get_saved_courses()
    for course in courses:
        if course['id'] == _id:
            return course
    return None


def write_courses(courses: list[dict]) -> None:
    path = os.path.join(CONFIG_DIR, COURSES)
    file = []
    for course in courses:
        c = get_saved_course(course['id'])
        file.append({
            'id': course['id'],
            'name': course['name'],
            'skip': c['skip'] if c is not None else False
        })
    fp = open(path, 'w')
    fp.write(json.dumps(file, indent=2))
    fp.close()


def get_saved_lessons() -> list[dict]:
    path = os.path.join(CONFIG_DIR, LESSONS)
    return inputs.open_json_file(path)


def get_saved_lesson(_id: str) -> dict or None:
    lessons = get_saved_lessons()
    for lesson in lessons:
        if lesson['id'] == _id:
            return lesson
    return None


def get_new_lessons(_lessons: list[dict]) -> list[dict]:
    return list(filter(lambda x: not get_saved_lesson(x['id']), _lessons))
    # lessons = []
    # for lesson in _lessons:
    #     if not get_saved_lesson(lesson['id']):
    #         lessons.append(lesson)
    # return lessons


def write_new_lessons(new_lessons: dict or list[dict]) -> None:
    path = os.path.join(CONFIG_DIR, LESSONS)
    file = (new_lessons if isinstance(new_lessons, list) else [new_lessons]) + get_saved_lessons()

    fp = open(path, 'w')
    fp.write(json.dumps(file, indent=2))
    fp.close()
