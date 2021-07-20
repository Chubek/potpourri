import unittest
from pathlib import Path

def runall():
    loader = unittest.TestLoader()
    start_dir = Path(__file__)
    suite = loader.discover(start_dir)

    runner = unittest.TextTestRunner()
    runner.run(suite)