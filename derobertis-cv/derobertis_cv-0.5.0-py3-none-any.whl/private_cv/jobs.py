import datetime
from typing import Sequence, Optional, List

import pyexlatex as pl
import pyexlatex.resume as lr

from derobertis_cv.pldata.employment_model import EmploymentModel


def get_professional_jobs(excluded_companies: Optional[Sequence[str]] = None) -> List[EmploymentModel]:
    jobs = [
        EmploymentModel(
            [
                'Manage up to 10 software developers, providing technical guidance and tracking progress',
                'Architect a web application to assist individuals in claiming lost money',
                'Developed and deployed the full-stack prototype of the application'
            ],
            'Claimfound, Inc.',
            'Co-Founder and Chief Technology Officer',
            'Gainesville, FL',
            datetime.datetime(2016, 8, 15),
        ),
    ]
    if excluded_companies:
        jobs = [job for job in jobs if job.company_name not in excluded_companies]
    return jobs
