import json

from flask import Blueprint, request
from pyutil.performance.return_series import from_nav
from pyweb.web.parser import respond_pandas
from pyweb.web.highcharts import parse, to_json

blueprint = Blueprint('post', __name__, static_folder="static")


def __percentage(x):
    return "{0:.2f}%".format(100*float(x)).replace("nan%", "")


def __series():
    return from_nav(parse(value=json.loads(request.data)))
    # series is an array [[t1,v1],[t2,v2],...]


@blueprint.route('/performance', methods=['POST'])
def performance():
    perf = __series().summary_format().apply(str)
    return respond_pandas(object=perf.to_dict(), format="json")


@blueprint.route('/month', methods=['POST'])
def month():
    # return a frame...
    return respond_pandas(object=__series().monthlytable.applymap(__percentage), format="json")


@blueprint.route('/drawdown', methods=['POST'])
def drawdown():
    return respond_pandas(object=to_json(__series().drawdown), format="json")


@blueprint.route('/volatility', methods=['POST'])
def volatility():
    return respond_pandas(object=to_json(__series().ewm_volatility()), format="json")
