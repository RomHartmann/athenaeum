"""Parsers for loading data for the indexer.

Parsers are broken up according to source and only import what they need.
"""


class BaseParser:
    """Base parser describing parsing pattern."""

    def __init__(self, validate_schema=None):
        """

        :param validate_schema: Set schema path to run a schema validation
        :type validate_schema: str or None
        """
        self.validate_schema = validate_schema

    def do_validate_schema(self, document):
        """Validate the schema of the document.

        :param document: The es_formatted data.
        :type document: dict
        :return: None
        :rtype: None
        """
        # TODO
        # if not valid: raise SchemaNotValidError
        pass

    def deserialize(self, *args, **kwargs):
        raise NotImplementedError

    def run(self, *args, **kwargs):
        raise NotImplementedError
