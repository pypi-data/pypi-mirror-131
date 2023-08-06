from LatexTemplater.TemplateFilter import TemplateFilter
from typing import Dict, Callable


def registrationInfo() -> Dict[str, Callable[[any], str]]:
    """
    Returns all of the infromation needed for registration of filters
    in this file
    """
    return {
        InlineFilter.name: InlineFilter.filter,
    }


class InlineFilter(TemplateFilter):
    """
    Filters a float value
    """

    name = "inline-Eq"

    @staticmethod
    def filter(equation: str) -> str:
        return f"${equation}$"
