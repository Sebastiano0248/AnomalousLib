import unittest
import numpy as np
from anomalouslib.constants import params, trajectory_types_mapping

class TestConstants(unittest.TestCase):
    
    def test_random_walk_constants(self):
        self.assertIn(params.rw.default_type, ["nonstop", "chill_stop", "hard_stop"])
        self.assertEqual(len(params.rw.nonstop), 4)
        self.assertIn([0, 0], params.rw.chill_stop)
        self.assertGreater(len(params.rw.hard_stop), len(params.rw.chill_stop))
    
    def test_brownian_motion_constants(self):
        self.assertGreater(params.bm.default_delta_t, 0)
        self.assertGreater(params.bm.default_sigma, 0)
        self.assertLess(params.bm.min_delta_t, params.bm.max_delta_t)
        self.assertLess(params.bm.min_sigma, params.bm.max_sigma)
    
    def test_fractional_brownian_motion_constants(self):
        self.assertGreater(params.fbm.default_hurst, 0)
        self.assertLess(params.fbm.default_hurst, 1)
        self.assertLess(params.fbm.min_hurst, params.fbm.max_hurst)
    
    def test_trajectory_types_mapping(self):
        expected_types = ["Random Walk", "Brownian Motion", "Fractional Brownian Motion",
                         "Continuous Time Random Walk", "Lévy Walk", 
                         "Annealed Transient Time Model", "Scaled Brownian Motion"]
        for traj_type in expected_types:
            self.assertIn(traj_type, trajectory_types_mapping)

if __name__ == "__main__":
    unittest.main()
