from cral.tracking.pyfunc import scoring_server
from cral.tracking import pyfunc
app = scoring_server.init(pyfunc.load_pyfunc("/opt/ml/model/"))
