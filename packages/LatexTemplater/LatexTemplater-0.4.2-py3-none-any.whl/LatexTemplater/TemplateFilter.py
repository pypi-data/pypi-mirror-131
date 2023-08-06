from abc import ABC, abstractmethod


class TemplateFilter(ABC):
    """
    The interface type for a filter
    """

    @abstractmethod
    def filter(any: any) -> str:
        """
        A filter that is used by jinja to mutate data
        """
        pass
