from derobertis_cv.models.category import CategoryModel
from derobertis_cv.pltemplates.logo import svg_text

INTRO_FIN_MODEL_CATEGORY = CategoryModel('Introduction to Financial Modeling')
CORPORATE_VALUATION_CATEGORY = CategoryModel('Corporate Valuation')

FIN_MODEL_COURSE_MAIN_CATEGORIES = [
    INTRO_FIN_MODEL_CATEGORY,
    CORPORATE_VALUATION_CATEGORY
]

FIN_MODEL_COURSE_CATEGORIES = [
    *FIN_MODEL_COURSE_MAIN_CATEGORIES,

    CategoryModel('Overview', parents=(INTRO_FIN_MODEL_CATEGORY,)),
    CategoryModel('Basic technical skills and setup – Excel and Python', parents=(INTRO_FIN_MODEL_CATEGORY,)),
    CategoryModel('Time value of money models', parents=(INTRO_FIN_MODEL_CATEGORY,)),
    CategoryModel('Basic statistical tools', parents=(INTRO_FIN_MODEL_CATEGORY,)),
    CategoryModel('Monte Carlo methods', parents=(INTRO_FIN_MODEL_CATEGORY,)),

    CategoryModel('Capital budgeting', parents=(CORPORATE_VALUATION_CATEGORY,)),
    CategoryModel('Estimating beta', parents=(CORPORATE_VALUATION_CATEGORY,)),
    CategoryModel('Estimating market value of debt', parents=(CORPORATE_VALUATION_CATEGORY,)),
    CategoryModel('Weighted average cost of capital (WACC)', parents=(CORPORATE_VALUATION_CATEGORY,)),
    CategoryModel('Free cash flow (FCF)', parents=(CORPORATE_VALUATION_CATEGORY,)),
    CategoryModel('Pro forma financial statements', parents=(CORPORATE_VALUATION_CATEGORY,)),
    CategoryModel('Discounted cash flow (DCF) valuation', parents=(CORPORATE_VALUATION_CATEGORY,)),
]



_COURSE_CATEGORIES = [
    CategoryModel('Algebra'),
    CategoryModel('Excel'),
]

COURSE_CATEGORIES = {cat.title: cat for cat in _COURSE_CATEGORIES}
