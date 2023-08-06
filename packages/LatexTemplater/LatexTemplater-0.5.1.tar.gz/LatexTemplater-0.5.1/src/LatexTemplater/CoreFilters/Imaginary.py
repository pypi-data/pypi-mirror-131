from LatexTemplater.TemplateFilter import TemplateFilter
from LatexTemplater.TemplateCore import TemplateCore
from typing import Dict, Callable


def registrationInfo() -> Dict[str, Callable[[any], str]]:
    """
    Returns all of the infromation needed for registration of filters
    in this file
    """
    return {
        ImaginaryFilter.name: ImaginaryFilter.filter,
    }


class ImaginaryFilter(TemplateFilter):
    """
    Filters a Imaginary Number
    """

    name = "imaginary"

    @staticmethod
    def filter(val: complex) -> str:
        inst = TemplateCore.instance()
        return (f'{inst.filter("decimal", val.real)} + ' +
                f'{inst.filter("decimal", val.imag)}j')
