from typing import List

from derobertis_cv.models.course import CourseModel
from derobertis_cv.pldata.constants.institutions import UF, VCU
from derobertis_cv.pldata.courses.fin_model import get_fin_model_course


def get_courses() -> List[CourseModel]:
    return [
        get_fin_model_course(),
        CourseModel(
            title='Debt and Money Markets',
            description="",
            highlight_description='fixed income course',
            evaluation_score=4.8,
            periods_taught=['Fall 2016', 'Spring 2018'],
            university=UF
        ),
        CourseModel(
            title='Financial Management Lab',
            description="",
            highlight_description='Excel skills course',
            periods_taught=['Spring 2014'],
            university=VCU
        ),
    ]