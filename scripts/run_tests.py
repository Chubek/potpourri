import unittest
import os

loader = unittest.TestLoader()
start_dir = os.path.join(os.getcwd(), "potpourri", "tests")
suite = loader.discover(start_dir)

runner = unittest.TextTestRunner()
runner.run(suite)