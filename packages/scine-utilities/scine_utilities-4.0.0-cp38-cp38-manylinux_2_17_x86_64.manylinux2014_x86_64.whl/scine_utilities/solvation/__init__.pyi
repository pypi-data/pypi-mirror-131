import scine_utilities.solvation
import typing
from typing import Union
import numpy
import scine_utilities
import scine_utilities.core
import scine_utilities.molsurf

__all__ = [
    "add",
    "arrange",
    "check_distances",
    "give_solvent_shell_vector",
    "merge_atom_collection_vector",
    "merge_solvent_shell_vector",
    "solvate",
    "solvate_shells",
    "solvation_strategy",
    "transfer_solvent_shell_vector"
]


def add(complex: scine_utilities.AtomCollection, additive: scine_utilities.AtomCollection, complex_surface_site: scine_utilities.molsurf.SurfaceSite, additive_surface_site: scine_utilities.molsurf.SurfaceSite, min_distance: float, max_distance: float, increment_distance: float = 0.25, number_rotation_attempts: int = 3) -> bool:
    """
    Add additive to given complex at given surface site of the complex.
    """
def arrange(surface_point_1: numpy.ndarray, surface_normal_1: numpy.ndarray, surface_point_2: numpy.ndarray, surface_normal_2: numpy.ndarray, molecule_2: numpy.ndarray, distance: float) -> numpy.ndarray:
    """
    Arrange one atom collection such that the two positions given face each other.
    """
def check_distances(molecule_1: scine_utilities.AtomCollection, molecule_2: scine_utilities.AtomCollection) -> bool:
    """
    Check if two atom collections overlap with their VdW spheres.
    """
def give_solvent_shell_vector(complex: scine_utilities.AtomCollection, solute_size: int, solvent_size_vector: typing.List[int], resolution: int, logger: scine_utilities.core.Log, strategic_solvation: bool = True, threshold: float = 1.0) -> typing.List[typing.List[scine_utilities.AtomCollection]]:
    """
    Analyze a complex and return its solvent shell vector.
    """
def merge_atom_collection_vector(atom_collection_vector: typing.List[scine_utilities.AtomCollection]) -> scine_utilities.AtomCollection:
    """
    Merges list of atom collections to one atom collection.
    """
def merge_solvent_shell_vector(shell_vector: typing.List[typing.List[scine_utilities.AtomCollection]]) -> scine_utilities.AtomCollection:
    """
    Merge a vector of a vector of atom collections (solvent shell vector) to one atom collection.
    """
def solvate(solute_complex: scine_utilities.AtomCollection, solute_size: int, solvent: scine_utilities.AtomCollection, number_solvents: int, seed: int, resolution: int = 32, solvent_offset: float = 0.0, max_distance: float = 10.0, step_size: float = 0.25, number_rotamers: int = 3, strategic_solvation: bool = False, coverage_threshold: float = 1.0) -> typing.List[typing.List[scine_utilities.AtomCollection]]:
    """
    Add systematically a number of solvents to solute.
    """
def solvate_shells(solute_complex: scine_utilities.AtomCollection, solute_size: int, solvent: scine_utilities.AtomCollection, number_shells: int, seed: int, resolution: int = 32, solvent_offset: float = 0.0, max_distance: float = 10.0, step_size: float = 0.25, number_rotamers: int = 3, strategic_solvation: bool = False, coverage_threshold: float = 1.0) -> typing.List[typing.List[scine_utilities.AtomCollection]]:
    """
    Add number of solvent shells to solute.
    """
def solvation_strategy(arg0: int) -> int:
    """
    Solvation strategy for faster building of solute - solvent complexes.
    """
def transfer_solvent_shell_vector(shell_vector: typing.List[typing.List[scine_utilities.AtomCollection]]) -> typing.List[int]:
    """
    Translate solvent shell vector into one vector containing the size of the solvents in order.
    """
