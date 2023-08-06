from LatexTemplater.TemplateFilter import TemplateFilter
from typing import Dict, Callable


def registrationInfo() -> Dict[str, Callable[[any], str]]:
    """
    Returns all of the infromation needed for registration of filters
    in this file
    """
    return {
        DecimalFilter.name: DecimalFilter.filter,
    }


class DecimalFilter(TemplateFilter):
    """
    Filters a float value
    """
    roundTo = 3
    name = "decimal"

    @staticmethod
    def filter(val: float) -> str:
        return str(round(float(val), DecimalFilter.roundTo))
