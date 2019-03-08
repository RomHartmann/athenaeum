"""Parsers that scrape online sources and load them into ES format."""
import logging

from . import BaseParser


# TODO
class ScraperParser(BaseParser):
    """Scrape a given site and parser for elasticsearch."""

    def __init__(self, url):
        """Scrape url.

        :param url: The url we want to scrape for listings.
        :type url: str
        """
        super().__init__()
        self.url = url

    def deserialize(self, *args, **kwargs):
        raise NotImplementedError

    def run(self, *args, **kwargs):
        raise NotImplementedError



