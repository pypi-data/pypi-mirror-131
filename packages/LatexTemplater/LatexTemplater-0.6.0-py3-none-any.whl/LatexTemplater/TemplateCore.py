from __future__ import annotations
import jinja2
from typing import Callable
import os
from LatexTemplater.LatexGenerator import PdfLatexGenerator, LatexGenerator
from typing import List, Dict
import json
import glob


class TemplateCore:
    """
    A Jinja template class made to work well with latex the following commands
    are used to render text:
    \\PYTHON{} for blocks
    \\PY{} for variables
    \\#{} for comments

    custom filters can be written for all sorts of things
    """
    __instance = None

    @staticmethod
    def instance() -> TemplateCore:
        """
        Gets the globa instance of the Template that all plugins register in
        """
        if TemplateCore.__instance is None:
            TemplateCore.__instance = TemplateCore()
        return TemplateCore.__instance

    def __init__(self) -> None:
        self._templater = jinja2.Environment(
            block_start_string=r'\PYTHON{',
            block_end_string='}',
            variable_start_string=r'\PY{',
            variable_end_string='}',
            comment_start_string='#{',
            comment_end_string='}',
            line_statement_prefix='%-',
            line_comment_prefix='%#',
            trim_blocks=True,
            autoescape=False,
            loader=jinja2.FileSystemLoader(".")
        )
        self._resultsFolder = '.'
        self._generator = PdfLatexGenerator()
        self._vars = {}

    @property
    def vars(self) -> Dict[str, any]:
        return self._vars

    @property
    def resultsFolder(self) -> str:
        return self._resultsFolder

    @resultsFolder.setter
    def resultsFolder(self, newResultFolder: str):
        self._resultsFolder = newResultFolder

    @property
    def templateDir(self) -> str:
        return self._templater.loader.searchpath

    @templateDir.setter
    def templateDir(self, templateFolder: str) -> None:
        self._templater.loader = jinja2.FileSystemLoader(
            os.path.abspath(templateFolder)
        )

    @property
    def generator(self) -> LatexGenerator:
        return self._generator

    @generator.setter
    def generator(self, newGenerator: LatexGenerator) -> None:
        self._generator = newGenerator

    def registerFilter(self,
                       name: str,
                       filter: Callable[[any], str]) -> None:
        """
        This function is used to register a jinja filter for
        the templates
        """
        self._templater.filters[name] = filter

    def filter(self, filterName: str, arg: any) -> str:
        return self._templater.filters[filterName](arg)

    def render(self, templateFile: str, varFiles: List[str] = [], **args) -> None:
        """
        render a template file and output it to output file. template file
        should be a path relative to template folder mentioned above. Will
        place it in the resultsFolder. If no file extension is included the
        defeault extension will be chosen(normally .tex.j2). The last File
        extension will be dropped, for the ouput file
        Variables can also be specified in a file and automatically read in
        if both are present, args takes presidence
        (typically j2)
        example:
         - render("test")
        inputFile is interpreted as test.tex.j2
        outputFIle is test.tex
        """
        self._vars = {}
        for varFile in varFiles:
            if varFile is not None:
                with open(varFile) as jsonFile:
                    data = json.load(jsonFile)
                    self._vars.update(data)
        self._vars.update(args)
        if "." not in templateFile:
            templateFile += ".tex.j2"
        template = self._templater.get_template(templateFile)
        outFileName = '.'.join(templateFile.split('.')[:-1])

        if not os.path.isdir(self.resultsFolder):
            os.mkdir(self.resultsFolder)
        with open(f'{self.resultsFolder}/{outFileName}', "w") as outFile:
            outFile.write(template.render(**self.vars))

    def generate(self,
                 mainTexFile: str = None,
                 resultDir: str = None,
                 render: bool = True, **args) -> None:
        templateFiles = glob.glob(self.templateDir[0] + "/*.tex.j2")
        templateFiles = [path.split('/')[-1] for path in templateFiles]
        if render:
            for templateFile in templateFiles:
                self.render(templateFile, **args)

        if mainTexFile is None:
            mainTexFile = templateFiles[0]

        if "." not in mainTexFile:
            mainTexFile += ".tex"

        if resultDir is None:
            resultDir = self._resultsFolder
        self.generator.generate(mainTexFile, resultDir, resultDir)
