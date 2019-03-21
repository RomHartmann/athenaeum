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
        url="https://bcres.paragonrels.com/publink/default.aspx?GUID=6f01a19a-b50f-4a34-9d08-9baef9db5121&Report=Yes"
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
