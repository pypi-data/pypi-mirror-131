from LatexTemplater.TemplateFilter import TemplateFilter
import os
from typing import Dict, Callable


def registrationInfo() -> Dict[str, Callable[[any], str]]:
    """
    Returns all of the infromation needed for registration of filters
    in this file
    """
    return {
        EquationFilter.name: EquationFilter.filter,
    }


class EquationFilter(TemplateFilter):
    """
    Filters a float value
    """

    name = "eq"

    @staticmethod
    def filter(equation: str) -> str:
        return (r"\begin{equation}" + os.linesep +
                str(equation) + os.linesep +
                r"\end{equation}" + os.linesep)
