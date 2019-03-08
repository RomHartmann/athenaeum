"""Parsers for loading data for the indexer.

"""



class BaseParser:
    """Base parser describing parsing pattern."""

    def __init__(self):
        pass

    def deserialize(self, *args, **kwargs):
        raise NotImplementedError


class CsvParser(BaseParser):
    """Parses CSVs"""