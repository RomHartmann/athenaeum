"""Functions to help with elasticsearch tasks.

To increase cluster size, Increase env vars "ES_JAVA_OPTS=-Xms3g -Xmx3g" for all elasticsearch services and then run:
  curl -XPUT localhost:9200/_cluster/settings -H 'Content-Type: application/json' -d '{"persistent" : {"cluster.routing.allocation.disk.threshold_enabled": False}}'

"""
import logging
import json
import os
import csv

from elasticsearch import Elasticsearch, helpers


ES = Elasticsearch(
    hosts=[{'host': 'localhost', 'port': 9200, 'use_ssl': False}]
)

logging.basicConfig(
    level=logging.INFO,
    format='{%(asctime)s.%(msecs)03d  %(filename)s:%(lineno)d} %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
# Set ES logging level.
es_logger = logging.getLogger('elasticsearch')
es_logger.setLevel(logging.WARNING)


def create_index(index_name):
    """Create index with the corresponding schema name in ./schemas.

    :param index_name: Name of index to create
    :type index_name: str
    :return: None
    :rtype: None
    """
    schema_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "schemas",
        f"{index_name}.json"
    )
    logging.info(f"Loading schema from {schema_path}")
    with open(schema_path, 'r') as f:
        schema = json.load(f)

    ES.indices.create(index=index_name, ignore=400, body=schema)


def reindex(old_index, new_index):
    """Reindex old index to new index.

    :param old_index: The name of the old index.
    :type old_index: str
    :param new_index: Name of the new index.
    :type new_index: str
    :return: None
    :rtype: None
    """
    logging.info(f"Reindexing {old_index} to {new_index}")
    res = ES.reindex(
        {"source": {"index": old_index}, "dest": {"index": new_index}},
        wait_for_completion=True,
        request_timeout=300
    )
    if res['total'] and res['took'] and not res['timed_out']:
        logging.info("Seems reindex was successfull")


def inplace_index(old_index, new_index):
    """Dangerous!  This deletes data in the old index after it is created in new.

    This is a way to deal with huge data.

    In case we get forbidden, try:
        curl -X PUT "localhost:9200/poms/_settings" -H 'Content-Type: application/json' -d'
        {
            "index": {
                "blocks": {
                    "read_only_allow_delete": "false"
                }
            }
        }
        '

    and also make sure that cluster has space.

    :param old_index: The name of the old index.
    :type old_index: str
    :param new_index: The name of the new index.
    :type new_index: str
    :return: None
    :rtype: None
    """
    logging.info(f"running a scan query over old index {old_index}")
    scan_size = 1000
    res = helpers.scan(
        client=ES,
        index=old_index,
        query={"query": {"match_all": {}}},
        size=scan_size
    )

    for i, doc in enumerate(res):
        if (i+1) % 1000 == 0:
            logging.info(f"{i+1} documents reindexed.")
        doc_id = doc.get("_id")
        doc_type = doc.get("_type")
        doc_body = doc.get("_source")
        ES.index(
            index=new_index,
            doc_type=doc_type,
            body=doc_body,
            id=doc_id
        )
        ES.delete(
            index=old_index,
            doc_type=doc_type,
            id=doc_id
        )


def dump_query_as_csv(index_name, query_filename, csv_headings):
    """Read query, execute and write csv with results.

    :param index_name: Name of index to query.
    :type index_name: str
    :param query_filename: Filename to query.
    :type query_filename: str
    :param csv_headings: CSV headings.
    :type csv_headings: list of str
    :return: None
    :rtype: None
    """
    query_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "queries",
        index_name,
        f"{query_filename}.json"
    )
    logging.info(f"Loading query from {query_path}")
    with open(query_path, 'r') as f:
        query = json.load(f)

    logging.info("running query.")
    res = helpers.scan(
        client=ES,
        index=index_name,
        query=query
    )

    csv_filepath = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        f"result_{index_name}_{query_filename}.csv"
    )
    logging.info(f"writing to csv {csv_filepath}")
    with open(csv_filepath, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(csv_headings)
        for doc in res:
            row = [doc.get("_source")[s] for s in csv_headings]
            writer.writerow(row)


def dump_query_as_nl_json(index_name, query_filename):
    """Read query, execute and write newline delimited json with results.

    This is useful to do a dumb backup of data.
      It was especially useful to extract data that needed to be re-indexed, but the cluster was full.

    :param index_name: Name of index to query.
    :type index_name: str
    :param query_filename: Filename to query.
    :type query_filename: str
    :return: None
    :rtype: None
    """
    query_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "queries",
        index_name,
        f"{query_filename}.json"
    )
    logging.info(f"Loading query from {query_path}")
    with open(query_path, 'r') as f:
        query = json.load(f)

    logging.info("running query.")
    res = helpers.scan(
        client=ES,
        index=index_name,
        query=query
    )

    nljson_filepath = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        f"result_{index_name}_{query_filename}.json.nl"
    )
    logging.info(f"writing to file {nljson_filepath}")
    with open(nljson_filepath, 'w') as f:
        for i, doc in enumerate(res):
            if (i+1) % 1000 == 0:
                logging.info(f"{i+1} documents downloaded.")
            f.write(f"{json.dumps(doc)}\n")


def index_from_nl_json(query_filename, index_overwrite=None):
    """Read a newline delimited json file and index documents.

    :param query_filename: Filename to query.
    :type query_filename: str
    :param index_overwrite: To overwrite where to write data.
    :type index_overwrite: None or str
    :return: None
    :rtype: None
    """
    nljson_filepath = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        query_filename
    )
    logging.info(f"Reading from to file {nljson_filepath}")
    with open(nljson_filepath, 'r') as f:
        logging.info("iterating through file...")
        for i, json_doc in enumerate(f):
            if (i+1) % 1000 == 0:
                logging.info(f"{i+1} documents loaded.")
            doc = json.loads(json_doc)
            ES.index(
                index=index_overwrite or doc.get("_index"),
                doc_type=doc.get("_type"),
                body=doc.get("_source"),
                id=doc.get("_id")
            )




if __name__ == '__main__':
    # create_index("poms")
    # reindex("ecomm", "poms")
    # dump_query_as_csv("ecomm", "socialwidget_grouped_userids", ["account_uuid"])
    # inplace_index("ecomm", "poms")
    # dump_query_as_nl_json("poms", "everything")
    # index_from_nl_json("result_ecomm_everything.json.nl", index_overwrite="poms")
    increase_cluster_size()
