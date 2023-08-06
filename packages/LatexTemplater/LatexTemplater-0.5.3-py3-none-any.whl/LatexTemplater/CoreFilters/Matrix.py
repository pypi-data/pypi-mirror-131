from LatexTemplater.TemplateFilter import TemplateFilter
from LatexTemplater.TemplateCore import TemplateCore
import os
from typing import List, Dict, Callable


def registrationInfo() -> Dict[str, Callable[[any], str]]:
    """
    Returns all of the infromation needed for registration of filters
    in this file
    """
    return {
        BMatrixFilter.name: BMatrixFilter.filter,
        VMatrixFilter.name: VMatrixFilter.filter,
    }


def _matrix(values: List[List[float]], matrixType: str) -> str:
    """
    A utility function that is used to print a generic matrix
    """
    inst = TemplateCore.instance()
    return_str = r"\begin{" + matrixType + "}" + os.linesep
    for i, row in enumerate(values):
        for j, item in enumerate(row):
            if type(item) == float:
                return_str += inst.filter("decimal", item)
            elif type(item) == complex:
                return_str += inst.filter("imaginary", item)
            else:
                return_str += str(item)
            if not (j == len(row)-1):
                return_str += " & "
        if not (i == len(values)-1):
            return_str += r"\\"
        return_str += os.linesep
    return_str += r"\end{" + matrixType + "}" + os.linesep
    return return_str


class BMatrixFilter(TemplateFilter):
    """
    Filters a float value
    """

    name = "bmatrix"

    @staticmethod
    def filter(bmatrix: List[List[float]]) -> str:
        return _matrix(bmatrix, "bmatrix")


class VMatrixFilter(TemplateFilter):
    """
    Filters a float value
    """

    name = "vmatrix"

    @staticmethod
    def filter(bmatrix: List[List[float]]) -> str:
        return _matrix(bmatrix, "vmatrix")
