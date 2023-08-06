from LatexTemplater.TemplateCore import TemplateCore
from . import Decimal
from LatexTemplater.CoreFilters import Imaginary
from LatexTemplater.CoreFilters import Equation
from LatexTemplater.CoreFilters import Matrix
from LatexTemplater.CoreFilters import InlineEquation


def initialize():
    """
    Registers all the types with the latex filter
    """
    instance = TemplateCore.instance()
    registrationFuncs = [
        Decimal.registrationInfo,
        Imaginary.registrationInfo,
        Equation.registrationInfo,
        Matrix.registrationInfo,
        InlineEquation.registrationInfo
    ]
    for registerFunc in registrationFuncs:
        filterinfo = registerFunc()
        for name, filter in filterinfo.items():
            instance.registerFilter(name, filter)
