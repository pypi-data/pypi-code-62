from copy import deepcopy
from pyexlatex.logic.format.and_join import join_with_commas_and_and_output_list

SKILLS = [
    'Python',
    'TypeScript/JavaScript',
    'SQL',
    'Angular',
    'Docker',
    'AWS',
    'LaTeX',
    'SAS',
    'Stata',
    'MATLAB',
    'NoSQL',
    'Git',
    'data science',
    'empirical research',
    'software architecture',
    'software development',
    'machine learning',
    'econometrics',
    'project management',
    'dev-ops',
    'QA'
]


def get_skills():
    formatted_skills = deepcopy(SKILLS)
    formatted_skills[0] = formatted_skills[0].capitalize()
    joined = join_with_commas_and_and_output_list(formatted_skills)
    return joined
