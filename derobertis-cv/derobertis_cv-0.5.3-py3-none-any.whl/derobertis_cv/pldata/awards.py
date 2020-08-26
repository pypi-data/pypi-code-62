import pyexlatex.resume as lr


def get_awards():
    return [
        lr.Award('Warrington College of Business Ph.D. Student Teaching Award', 'Fall 2016'),
        lr.Award('Warrington Finance Ph.D. Research Grants', '2014-2019', r'\$2000/yr'),
        lr.Award('CFA Global Investment Research Challenge – Global Semi-Finalist', '2013'),
        lr.Award('Finance Student of the Year', '2013'),
        lr.Award('Alcoa Foundation Community Scholarship', '2010-2014', 'full tuition and fees'),
        lr.Award('VCU School of Business Scholarship', '2010-2014', r'\$3000/yr')
    ]