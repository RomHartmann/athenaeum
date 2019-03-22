"""Script from where to run things from."""
import logging

import indexers
from parsers import scraper_parsers

logging.basicConfig(level=logging.INFO, format='%(asctime)-15s %(filename)s:%(lineno)d %(levelname)s - %(message)s')

# Drop down very noisy ES logging
es_logger = logging.getLogger('elasticsearch')
es_logger.setLevel(logging.WARNING)


def index_all_bcres():
    indexer = indexers.DefaultIndexer(
        index_name="property",
        schema_name="property_listings"
    )

    with open("data/bcres_urls.txt", 'r') as f:
        for url in f:
            logging.info(f"Reading URL = {url}")
            parser = scraper_parsers.BcresParser(url=url)
            es_data = parser.run()

            for datum in es_data:
                indexer.index_document(datum)


if __name__ == '__main__':
    index_all_bcres()
