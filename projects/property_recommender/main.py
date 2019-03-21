"""Script from where to run things from."""
import logging

import indexers
from parsers import csv_parsers, scraper_parsers

logging.basicConfig(level=logging.INFO, format='%(asctime)-15s %(filename)s:%(lineno)d %(levelname)s - %(message)s')


def main():

    # parser = csv_parsers.MlsParser(
    #     file_path="data/mls_2019_03.csv"
    # )
    parser = scraper_parsers.BcresParser(
        url="http://bcres.paragonrels.com/publink/default.aspx?GUID=d4a4c4b3-dd14-4e36-bbbf-923a7a9dd56b&Report=Yes"
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
