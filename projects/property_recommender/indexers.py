"""This is the modulated indexer, which handles the entire ETL process.

The way this is set up is that enrichment modules can be added to the indexer as needed so that
  the document can gain complexity in the future for more elegant searches.

TODO:
It can also check if any documents are missing information and then do enriching only for what is missing.
"""
import logging
import os
import json
import time

from elasticsearch import Elasticsearch


class DefaultIndexer:
    """The indexer is the ETL processer."""

    def __init__(self, index_name, schema_name):
        """Instantiate the indexer.

        :param index_name: The name of the indexer.
        :type index_name: str
        :param schema_name: The name schema json file in the ./schemas/ directory..
        :type schema_name: str
        """
        self.index_name = index_name
        self.schema_name = schema_name

        self.es = Elasticsearch(
            hosts=[{'host': 'localhost', 'port': 9200, 'use_ssl': False}]
        )
        self.schema = self.open_schema(schema_name)

        if not self.es.indices.exists(index_name):
            logging.info(f"creating elasticsearch index for '{index_name}'")
            self.es.indices.create(index=index_name, ignore=400, body=self.schema)
            time.sleep(10)  # allow some time for index to be created

    @staticmethod
    def open_schema(schema_name):
        """Open the schema at ./schema/<schema_name>.json

        :param schema_name: The filename of the scheama.
        :type schema_name: str
        :return: Deserialized json object.
        :rtype: dict
        """
        filepath = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "schemas",
            f"{schema_name}.json"
        )
        logging.info(f"Opening schema at {filepath}")
        with open(filepath, 'r') as f:
            schema = json.load(f)
        return schema

    def index_document(self, doc):
        """Index a single document

        :param doc: The elasticsearch document to index.
        :type doc: dict
        :return: None
        :rtype: None
        """
        self.es.index(
            index=self.index_name,
            doc_type=self.schema_name,
            body=doc
        )

    def bulk_index(self, docs):
        """Bulk index many documents.

        :param docs: A list of documents to index to ES.
        :type docs: list of dict
        :return: None
        :rtype: None
        """
        body = []
        for doc in docs:
            body.append({
                "_index": self.index_name,
                "_type": self.schema_name,
                "doc": doc,
            })

        self.es.bulk(
            index=self.index_name,
            doc_type=self.schema_name,
            body=body
        )
