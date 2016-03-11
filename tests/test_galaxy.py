from pybsm.galaxy import Galaxy, GalaxyWarning, GalaxyException, QBTwisting, MatterType
from pybsm import particles
import unittest


class TestGalaxy(unittest.TestCase):
    def test_particles_per_tetrahedron(self):
        self.assertEqual(Galaxy(n_edge=13).particles_per_tetrahedron, 455,
                         "Number of particles should be 455")
        self.assertEqual(Galaxy(n_edge=5).particles_per_tetrahedron, 35,
                         "Number of particles should be 35")

    def test_galaxy_validation(self):
        with self.assertRaises(GalaxyException):
            Galaxy(qb_crystal_depth=3, qb_destruction_depth=4)
        with self.assertRaises(GalaxyException):
            Galaxy(qb_crystal_depth=3, qb_destruction_depth=3)
        with self.assertRaises(GalaxyException):
            Galaxy(qb_crystal_depth=3, qb_destruction_depth=2)
        with self.assertRaises(GalaxyWarning):
            self.assertTrue(Galaxy(qb_crystal_depth=3, qb_destruction_depth=1))
        with self.assertRaises(GalaxyException):
            Galaxy(qb_crystal_depth=3, qb_destruction_depth=0)

        with self.assertRaises(GalaxyException):
            Galaxy(qb_crystal_depth=4, qb_destruction_depth=4)
        with self.assertRaises(GalaxyException):
            Galaxy(qb_crystal_depth=4, qb_destruction_depth=3)
        # this is a valid possibility
        self.assertTrue(Galaxy(qb_crystal_depth=4, qb_destruction_depth=2))
        with self.assertRaises(GalaxyWarning):
            Galaxy(qb_crystal_depth=4, qb_destruction_depth=1)

        with self.assertRaises(GalaxyException):
            Galaxy(qb_crystal_depth=2, qb_destruction_depth=1)
        with self.assertRaises(GalaxyException):
            Galaxy(qb_crystal_depth=2, qb_destruction_depth=0)

        tg = Galaxy(qb_crystal_depth=6, qb_destruction_depth=3)
        self.assertTrue(tg.validate(), "should create a valid Galaxy")

    def test_twisting(self):
        # test normal galaxy
        mg = Galaxy(matter=MatterType.matter)
        self.assertEqual(mg.twisting_for_qb(particles.FPLarge), QBTwisting.right)
        self.assertEqual(mg.twisting_for_qb(particles.FPSmall), QBTwisting.left)

        class FakeFP(particles.FP):
            pass

        with self.assertRaises(GalaxyException):
            mg.twisting_for_qb(FakeFP)

        # test antimatter galaxy
        ag = Galaxy(matter=MatterType.antimatter)
        self.assertEqual(ag.twisting_for_qb(particles.FPLarge), QBTwisting.left)
        self.assertEqual(ag.twisting_for_qb(particles.FPSmall), QBTwisting.right)
