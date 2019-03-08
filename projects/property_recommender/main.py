"""Script from where to run things from."""
import logging

from . import indexers
from parsers import csv_parsers

# TODO set?   format='%(asctime) %(filename)s:%(lineno)d %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO)


def main():
    indexer = indexers.DefaultIndexer(
        index_name="property",
        schema_name="property_listings"
    )

    parser = csv_parsers.MslParser(
        file_path="data/msl_2019_03.csv"
    )
    es_data = parser.run()

    indexer.bulk_index(es_data)


if __name__ == '__main__':
    main()
