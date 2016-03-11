"""
Galaxy module

The galaxy module contains all classes related to underlaying principles of particle crystalization.

Each Galaxy class instance represents a different galaxy with its own parameters determened
through the energies and particles masses of the galactic nucleus while it was
in the hidden crystalization phase.

See BSM-SG Book Chapter 12 for a detailed explanation of the process.
"""


from cached_property import cached_property
from .particles import FPLarge, FPSmall
from enum import IntEnum, Enum


class QBTwisting(Enum):
    """
    A Quasiball must have a internal twisting due geometric considerations.

    QBTwisting is used to repersent this twisting posibility.
    """
    left = 1
    right = 2


class MatterType(Enum):
    """
    Defines the possible twisting combinations for a galaxy.
    """
    matter = 1
    antimatter = 2


class PrismGrade(IntEnum):
    """
    Quality of shaped prisms
    """
    __order__ = 'low good very_good'
    low = 1
    good = 2
    very_good = 3


class GalaxyWarning(Warning):
    """
    The selected parameters are unlikely or unstable
    """


class GalaxyException(Exception):
    """
    The selected parameters are impossible
    """


class Galaxy(object):
    def __init__(self, n_edge=13, matter=MatterType.matter,
                 qb_crystal_depth=5, qb_destruction_depth=2,
                 prism_qb=12,
                 prism_width=0.00000000000001,
                 ratio=3.0/2.0,
                 validate=True):
        """
        Reperesnts a Galaxy with all it's internal parameters.
        The parameters of a galaxy depend on specific to energy leves while
        the galaxy crystalized. See the BSM-SG Book Chapter 12.

        :param n_edge: Edgelength of tetrahedron (integer)
        :param matter: Type of Matter
        :param qb_crystal_depth: height of QB crystalization level
        :param qb_destruction_depth: number of QB levels for prism destruction
        :param prism_qb: number of QB (last size) per prism
        :param ratio: ratio between the small and large fundamental particles
        """
        self.n_edge = n_edge
        self.matter = matter
        self.qb_crystal_depth = qb_crystal_depth
        self.qb_destruction_depth = qb_destruction_depth
        self.prism_qb = prism_qb
        if validate:
            self.validate()

    def validate(self):
        if self.qb_crystal_depth - self.qb_destruction_depth <= 0:
            raise GalaxyException("qb_destruction_depth can't be larger then qb_crystal_depth + 1")
        if self.qb_crystal_depth - self.qb_destruction_depth <= 1:
            raise GalaxyException("qb_crystal_depth - qb_destruction_depth must be larger then 1")
        if self.qb_destruction_depth < 1:
            raise GalaxyException("qb_destruction_depth needs to be at least 1")
        if self.prism_grade < PrismGrade.good:
            raise GalaxyWarning("Bad prism_grade")
        return True

    @cached_property
    def prism_grade(self):
        """
        Quality of prisms formation. Number of QP per prism.
        """
        if self.qb_destruction_depth <= 1:
            return PrismGrade.low
        elif self.qb_destruction_depth == 2:
            return PrismGrade.good
        elif self.qb_destruction_depth >= 3:
            return PrismGrade.very_good

    @cached_property
    def particles_per_tetrahedron(self):
        """
        Calculates the number of particles in one tetrahedron of edge length
        N_edge.
        :param N_edge: edge length, must be integer
        """
        rv = 1
        for height in range(self.n_edge, 1, -1):
            for i in range(1, height+1):
                rv += i
        return rv

    @staticmethod
    def create_milkyway():
        return Galaxy(
            n_edge=13,
            matter=MatterType.matter
        )

    def twisting_for_qb(self, fp):
        """
        Returns the propriet twisting for the QuasiBall.

        It is not clear if the assignment of left and right to the FP's is correct,
        matter and antimatter could be exchanged.

        :param fp: type of fundamental particle for the QuasiBall
        """
        if self.matter == MatterType.matter:
            if issubclass(fp, FPLarge):
                return QBTwisting.right
            elif issubclass(fp, FPSmall):
                return QBTwisting.left
            else:
                raise GalaxyException("unknown fp type")
        elif self.matter == MatterType.antimatter:
            if issubclass(fp, FPLarge):
                return QBTwisting.left
            elif issubclass(fp, FPSmall):
                return QBTwisting.right
            else:
                raise GalaxyException("unknown fp type")
        else:
            raise GalaxyException("unknown matter type")
