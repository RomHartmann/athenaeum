"""This is the modulated indexer, which handles the entire ETL process.

The way this is set up is that enrichment modules can be added to the indexer as needed so that
  the document can gain complexity in the future for more elegant searches.

TODO:
It can also check if any documents are missing information and then do enriching for what is missing.
"""
import logging

from elasticsearch import Elasticsearch

from . import enrichers

# TODO set?   format='%(asctime) %(filename)s:%(lineno)d %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO)


class Indexer:
    """The indexer is the ETL processer."""

    def __init__(self):
        self.es = Elasticsearch(
            hosts=[{'host': 'localhost', 'port': 9200, 'use_ssl': False}]
        )

    # TODO
    def index_document(self):
        pass

    # TODO
    def enrich_missing(self):
        pass


















