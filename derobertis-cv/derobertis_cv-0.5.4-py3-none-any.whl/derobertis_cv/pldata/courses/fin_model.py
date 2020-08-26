from typing import Dict, Any

import pyexlatex as pl

from derobertis_cv.models.course import CourseModel
from derobertis_cv.models.prereq import CoursePrerequsitesModel
from derobertis_cv.models.textbook import TextbookModel
from derobertis_cv.pldata.constants.institutions import UF_NAME
from derobertis_cv.pldata.course_categories import COURSE_CATEGORIES, FIN_MODEL_COURSE_CATEGORIES, \
    FIN_MODEL_COURSE_MAIN_CATEGORIES
from derobertis_cv.pldata.courses.general import get_grading_model
from derobertis_cv.pldata.software import get_software_projects
from derobertis_cv.pldata.universities import UF


def get_fin_model_course(**overrides: Dict[str, Any]) -> CourseModel:
    default_textbook = TextbookModel(
        title='Financial Modeling',
        author='Simon Benninga',
        required=False,
        description="""
Textbook is only recommended. This book is very focused on Excel and we will be using both Excel
and Python in the course. It is however useful as a reference for the Excel material and generally how
to build the models.
        """.strip(),
        publisher_details='Fourth Edition, MIT Press'
    )

    default_prereqs = CoursePrerequsitesModel(
        required_courses=[
            CourseModel('Business Finance', '', course_id='FIN 3403'),
        ],
        recommended_courses=[
            CourseModel('Debt and Money Markets', '', course_id='FIN 4243'),
            CourseModel('Equity and Capital Markets', '', course_id='FIN 4504'),
        ],
        courses_description="""
FIN 3403 (Business Finance) is the minimum requirement. It is highly recommended that you have also taken
FIN 4243 (Debt and Money Markets) and FIN 4504 (Equity and Capital Markets) as we will build models
based on the concepts in these courses without a thorough treatment of them. We have a lot to cover already
in the course and so the finance concepts are not the focus. I can recommend textbooks for any concepts
which you haven’t covered in prior courses, but then you will have a large learning curve.   
        """.strip(),
        technical_skills=[COURSE_CATEGORIES['Algebra'], COURSE_CATEGORIES['Excel']],
        technical_skills_description="""
Understanding of algebra is necessary to work with equations in the models. Introductory Excel capabilities
are required. Any experience with Python is a plus. It will be assumed that most students have introductory to
intermediate skills in Excel and no experience with Python. If you have no Excel experience but still want to
take the course, contact me and I can send some resources to learn introductory Excel.
        """
    )

    default_class_structure = [
        pl.SubSubSection(
            [
                """
The class is structured in three parts: lecture videos, lecture review sessions, and interactive lab sessions.
The lecture review sessions will be a group video call which also be recorded and provide an opportunity 
for students to ask general questions 
about the lecture. For the lab sessions, I will be giving weekly problems for you to work on which reinforce
the content from the lectures for that week. During the lab session video calls, I will be available for any 
individual questions as you complete the exercises. You may need to spend time outside of the lab sessions
completing the exercises as well. You are encouraged to discuss the lab exercises with your
classmates, but everyone should complete the exercises on their own computer.      
                """.strip()
            ],
            title='A Typical Day'
        ),
        pl.SubSubSection(
            [
                """
There will be approximately five projects in the course. The grading in this course is entirely project-based,
between the projects and the lab exercises.

Projects are to be completed individually. Do not copy each other’s code or workbooks. This includes
copy/paste as well as manually following someone’s specific steps. You can however discuss them with your
classmates, so long as the final submission is entirely your own work.
                """.strip()
            ],
            title='Projects'
        ),
        pl.SubSubSection(
            [
                """
There are four ways you may ask questions: in lecture review sessions, in lab sessions, by email,
and by appointment. Before you ask a question, be sure that you have watched the relevant lecture(s),
and if the question is directly asking a question clearly covered in the lecture I may only point 
you to that.
                
If you are not able to figure out the lab exercise in the time provided, I am happy to help you by email or 
appointment for a video call.
                """.strip()
            ],
            title='Questions?'
        ),
        pl.SubSubSection(
            [
                pl.Model("""
I will accept late projects, {{ "but I will subtract 10% from the grade for each day" | Bold  }} late. Projects are 
{{ "due by midnight on the due date" | Bold }} and must be submitted to Canvas by this time. If you turn it in 
five minutes after midnight, I will subtract 10%. Then each additional 10% subtraction happens at midnight on each 
following day. But {{ "once we review the project as a class, you are no longer allowed to submit it." | Bold }} 
This will usually be about a week after but not always.

For example, if a project was due Tuesday, and you submit it two minutes after midnight (Wednesday 12:02 AM), 
you will lose
10%. Then, starting 12:01 AM Thursday (Wednesday night), you are losing 20%. Then starting 12:01 Friday
(Thursday night), you are losing 30%. But we review the project as a class that Thursday, you may only
submit it up until that time on Thursday.
                """.strip())
            ],
            title='Late Policy'
        ),
        pl.SubSubSection(
            [
                """
I highly recommend using some outside resources to learn some basic Python as it will allow you
to focus more on the course content. I will be teaching from the basics, but this is not a programming
class so we don't have the time to give the language a proper treatment. In the past, students which started early
with external Python and Excel resources performed well and got more applicable knowledge out of the class.
                
Watching every lecture is important as the knowledge from prior lectures becomes essential 
to understand the later lectures. Beyond the lectures, we will have interactive lab
sessions where you can ask me questions and actively get help with the course material as you work on it. For
the projects, you will need to build upon (directly or indirectly) what you have put together in the lab sessions.
Practice problems will also be provided, and it is encouraged that you complete them
before the projects. Start the projects early as there is considerable work involved. Many students have
said they have been the most challenging and rewarding projects they completed at UF.

If you feel lost at any time, please contact me and I can provide additional help, as the
material will continue to build on itself. You cannot afford to feel lost and do nothing and 
hope it will get better, it will only get worse as the course progresses.
                """.strip()
            ],
            title='How to be Successful in This Class'
        ),
        pl.SubSubSection(
            [
                """
Projects may be turned in late for reduced credit but not after we have reviewed it. See Projects section
above.
                """.strip()
            ],
            title='Make-Up Policy'
        ),
    ]

    default_grading_model = get_grading_model()

    software_project_names = ['fin-model-course', 'py-finstmt', 'sensitivity']
    default_software_projects = get_software_projects(
        include_projects=software_project_names,
        order=software_project_names,
    )

    data = dict(
        title='Financial Modeling',
        description="""
Financial modeling course which focuses on using Python and Excel to understand
personal finance and valuation problems.
        """.strip(),
        highlight_description='Python and Excel-based course',
        long_description="""
This course covers the full financial modelling workflow using both Excel and Python. I will try to teach you
how to build a model in general, all the way from concept and data collection to the result and visualization,
and how to complete the various steps in either Excel or Python. My goal is to give you tangible skills which
would be applicable in a finance job, and more so than any other course you’ve ever taken. This course will
be very challenging for the less technically inclined, but I will try to help everyone succeed.
        """.strip(),
        evaluation_score=4.2,
        periods_taught=['Fall 2019', 'Spring 2020', 'Fall 2020', 'Spring 2021'],
        university=UF,
        course_id='FIN 4934',
        current_period='Fall 2020',
        current_time='Fully Online, Asynchronous',
        office_hours='TBD',
        textbook=default_textbook,
        daily_prep='Have a computer with Microsoft Excel 2007 or newer ready. We will be installing Python '
                   'on this machine as well.',
        prerequisites=default_prereqs,
        class_structure_body=default_class_structure,
        grading=default_grading_model,
        topics=FIN_MODEL_COURSE_MAIN_CATEGORIES,
        software_projects=default_software_projects,
    )
    data.update(overrides)

    return CourseModel(**data)