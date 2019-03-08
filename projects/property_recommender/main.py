"""Script from where to run things from."""
import logging

import indexers
from parsers import csv_parsers

logging.basicConfig(level=logging.INFO, format='%(asctime)-15s %(filename)s:%(lineno)d %(levelname)s - %(message)s')


def main():

    parser = csv_parsers.MslParser(
        file_path="data/msl_2019_03.csv"
    )
    es_data = parser.run()

    indexer = indexers.DefaultIndexer(
        index_name="property",
        schema_name="property_listings"
    )
    for datum in es_data:
        indexer.index_document(datum)


if __name__ == '__main__':
    main()
