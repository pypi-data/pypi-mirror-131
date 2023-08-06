import argparse
from LatexTemplater.TemplateCore import TemplateCore
from typing import List

from LatexTemplater.TemplatePluginManager import load_plugins


def argParse():
    parser = argparse.ArgumentParser(prog="LatexTemplater",
                                     description="A latex Templating system "
                                     "that allows for easy injection of python "
                                     "into latex")
    parser.add_argument('main_template_file', type=str,
                        help="Path to the main tex file")
    parser.add_argument('--path', "-p", type=str, default=".",
                        help="Path to any other helper files")
    parser.add_argument('--vars', '-v', type=List[str], nargs="*", default=[],
                        help="Path to all config file which specifies all "
                        "variables")
    parser.add_argument('--output', '-o', type=str, nargs=1, default=".",
                        help="output directory for generated latex and pdf")
    parser.add_argument('--filters', '-f', type=List[str], nargs="*", default=[],
                        help="specify filter modules to be loaded")
    return parser


def main():
    parser = argParse()
    inst = TemplateCore.instance()
    args = parser.parse_args()
    load_plugins(args.filters)
    inst.templateDir = args.path
    inst.generate(args.main_template_file,
                  args.output,
                  render=True,
                  varFiles=args.vars)
