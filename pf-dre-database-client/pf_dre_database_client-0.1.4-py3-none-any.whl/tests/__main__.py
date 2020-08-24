# tests/runner.py
import unittest

# import your tests modules
import tests.test_devices as devices
import tests.test_configuration as config
import tests.test_data as data


# initialize the tests suite
loader = unittest.TestLoader()
suite = unittest.TestSuite()

# add tests to the tests suite
suite.addTests(loader.loadTestsFromModule(devices))
suite.addTests(loader.loadTestsFromModule(config))
suite.addTests(loader.loadTestsFromModule(data))

# initialize a runner, pass it your suite and run it
runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)
