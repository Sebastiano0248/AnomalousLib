#!/usr/bin/env python3
import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def run_all_tests():
    loader = unittest.TestLoader()
    suite = loader.discover(os.path.dirname(__file__), pattern='test_*.py')
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()

def run_specific_test(test_name):
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromName(test_name)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        success = run_specific_test(sys.argv[1])
    else:
        success = run_all_tests()
    
    sys.exit(0 if success else 1)
