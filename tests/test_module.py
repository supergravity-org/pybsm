import unittest


class TestModule(unittest.TestCase):
    def test_module(self):
        # We have to reload the pybsm module for coverage to detect the usage
        import pybsm
        import imp
        imp.reload(pybsm)

        self.assertEqual(pybsm.RELEASE, (0, 1, 0))
        self.assertTrue(isinstance(pybsm.__version__, str))
        self.assertTrue(isinstance(pybsm.VERSION, tuple))
        self.assertTrue(isinstance(pybsm.VERSION_STR, str))
        self.assertTrue(isinstance(pybsm.RELEASE, tuple))
