import unittest
from injecta.testing.servicesTester import testServices
from gitbundle.containerInit import initContainer

class GitBundleTest(unittest.TestCase):

    def test_init(self):
        container = initContainer('test')

        testServices(container)

        bundleParameters = container.getParameters().gitbundle

        self.assertEquals(bundleParameters.currentBranch, 'master')
        self.assertEquals(bundleParameters.currentBranchWithoutFeature, 'master')

if __name__ == '__main__':
    unittest.main()
