import argparse
from LatexTemplater.TemplateCore import TemplateCore


def argParse():
    parser = argparse.ArgumentParser(prog="LatexTemplater",
                                     description="A latex Templating system "
                                     "that allows for easy injection of python "
                                     "into latex")
    parser.add_argument('main_template_file', type=str, nargs=1,
                        help="Path to the main tex file")
    parser.add_argument('--path', "-p", type=str, nargs=1, default=".",
                        help="Path to any other helper files")
    parser.add_argument('--vars', '-v', type=str, nargs=1, default=None,
                        help="Path to a config file which specifies all "
                        "variables")
    parser.add_argument('--output', '-o', type=str, nargs=1, default=".",
                        help="output directory for generated latex and pdf")
    return parser


def main():
    parser = argParse()
    inst = TemplateCore.instance()
    args = parser.parse_args()
    inst.templateDir = args.path
    inst.generate(args.main_template_file[0],
                  args.output,
                  render=True,
                  varFile=args.vars)
