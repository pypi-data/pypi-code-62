from tests.test_structure_tensor import StructTensorTestCase
from tests.test_lf_depth import LfDepthTestCase
from tests.test_cli import CliTestCase


test_classes = [StructTensorTestCase, LfDepthTestCase, CliTestCase]

for test_class in test_classes:
    obj = test_class()
    obj.setUp()
    obj.test_all()
    del obj
