import argparse
from LatexTemplater import ArgParser
from LatexTemplater.TemplatePluginManager import load_plugins

# include the default plugins
load_plugins(["LatexTemplater.CoreFilters"])


if __name__ == '__main__':
    ArgParser.main()
