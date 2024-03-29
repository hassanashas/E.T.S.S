from data import *
from timetable import * 
from sections import sections_data
from courses import courses_data
from teachers import teachers_data
from typing import List
import pdfkit
from pdfkit.api import configuration
from jinja2 import FileSystemLoader, Environment
wkhtml_path = pdfkit.configuration(wkhtmltopdf = "C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")  #by using configuration you can add path value.


def generate_data(timetable, reg_data):

    rooms_timetable = {}

    for time in timetable: 
        for r in time.slots: 
            i = r.room 
            if (i) not in rooms_timetable.keys():
                rooms_timetable[i] = [["" for y in range(5)] for z in range(5)]
            for sec in reg_data:
                if time.id == sec.id:
                    t_sec = sections_data[sec.section_id].name.replace(" ", "_")
                    t_course = courses_data[sec.course_id].name.replace(" ", "_")
                    t_instructor = teachers_data[sec.teacher_id].name.replace(" ", "_")
                    rooms_timetable[i][r.day-1][r.slot-1] += t_course + "@" + t_sec + "@" + t_instructor + " "

    return rooms_timetable


def organise_input_data(elements: List[List[str]]) -> List[List]:
    """
    Organises the input data to find double courses for easier use in templates
    """
    new_elements = []
    for day in elements:
        last_course = None
        course_list = []
        index = 0
        for course in day:
            # cleanup data
            course = course.strip().replace(" ", "<hr>")
            # check if long course (and not lunch time)
            if course != "" and course == last_course and index != 3:
                course_list.remove((course, 1))
                course_list.append((course, 2))
                course_list.append(("none", 0))
            else:
                course_list.append((course.replace(" ", "<hr>"), 1))
            last_course = course
            index += 1
        new_elements.append(course_list)

    return new_elements


def generate_html(template, name: str, elements: List[List]) -> str:

    new_elements = organise_input_data(elements=elements)

    rendered = template.render(
        name=name,
        monday=new_elements[0],
        tuesday=new_elements[1],
        wednesday=new_elements[2],
        thursday=new_elements[3],
        friday=new_elements[4]
    )

    with open(f"out_{name}.html", "w+") as file:
        file.write(rendered)

    return rendered


def run(input_data):
    # Init jinja
    file_loader = FileSystemLoader('.')
    env = Environment(loader=file_loader)
    template = env.get_template('template.html')

    full_text = ""
    for name, elements in input_data.items():
        full_text += generate_html(template=template, name=name, elements=elements)

    pdfkit.from_string(full_text, "Rooms Timetable.pdf", configuration = wkhtml_path)


def generate_rooms_timetable(timetable, reg_data):
    rooms_timetable = generate_data(timetable, reg_data)
    rooms_timetable = dict(sorted(rooms_timetable.items()))

    run(rooms_timetable)

