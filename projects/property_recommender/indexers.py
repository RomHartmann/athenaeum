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

        if not self.es.indices.exists(index_name):
            self.schema = self.open_schema(schema_name)
            self.create_index()

    def create_index(self, timeout=120):
        """Create ES index if it does not exist, and don't proceed until index is up.

        :param timeout: Amount of seconds to wait for index to be up.
        :type timeout: int or float
        :return: None
        :rtype: None
        """
        logging.info(f"creating elasticsearch index for '{self.index_name}'")
        self.es.indices.create(index=self.index_name, ignore=400, body=self.schema, request_timeout=timeout)

        time_elapsed = 0
        check_interval = 5
        while True:
            cluster_health = self.es.cluster.health()
            if cluster_health.get('status') == "green":
                logging.info("Index on cluster is ready.")
                break

            logging.info(f"Cluster not ready yet, waiting {check_interval}s...")
            time.sleep(check_interval)  # allow some time for index to be created
            time_elapsed += check_interval
            if time_elapsed > timeout:
                raise Exception(f"Creating index after {time_elapsed} has not yet resulted in healthy index.")

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
            id=doc.get("id"),
            index=self.index_name,
            doc_type=self.schema_name,
            body=doc,
            request_timeout=20
        )

    def bulk_index(self, docs):
        """Bulk index many documents.

        :param docs: A list of documents to index to ES.
        :type docs: list of dict
        :return: None
        :rtype: None
        """
        # TODO
