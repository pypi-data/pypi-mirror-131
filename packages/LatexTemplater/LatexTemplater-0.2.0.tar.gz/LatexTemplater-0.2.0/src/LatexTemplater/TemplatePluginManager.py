import importlib
from typing import List


class PluginInterface:
    """
    Defines the interface that is used by LatexTemplater for custom filters
    """

    @staticmethod
    def initialize():
        """
        Initializes the plugins with Latex templater
        """


def load_plugins(plugins: List[str]) -> None:
    """
    Loads the plugins defined in the plugins list, will try the listed, if that 
    doesnt work then it will try same name with .Plugin appended
    """
    for plugin_name in plugins:
        plugin = import_module(plugin_name)
        try:
            plugin.initialize()
        except AttributeError:
            plugin = import_module(plugin_name + '.Plugin')
            plugin.initialize()


def import_module(name: str) -> PluginInterface:
    return importlib.import_module(name)
