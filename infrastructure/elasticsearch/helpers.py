"""Functions to help with elasticsearch tasks.

To increase cluster size, Increase env vars eg "ES_JAVA_OPTS=-Xms3g -Xmx3g" for all elasticsearch services and then run:
  make rebalance

"""
import logging
import json
import os
import csv
import argparse

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


def delete_by_query(index, query):
    """Delete items by query.

    :param index: Index where docs are.
    :type index: str
    :param query: Query, which matched, deletes items.
    :type query: dict
    :return: None
    :rtype: None
    """
    logging.info(f"Deleting by {query}")
    ES.delete_by_query(
        index=index,
        body=query
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


def dump_query_as_nl_json(index_name, query_filename, nljson_filepath=None):
    """Read query, execute and write newline delimited json with results.

    This is useful to do a dumb backup of data.
      It was especially useful to extract data that needed to be re-indexed, but the cluster was full.

    :param index_name: Name of index to query.
    :type index_name: str
    :param query_filename: Filename to query.
    :type query_filename: str
    :param nljson_filepath: Filename to where to save.
    :type nljson_filepath: str
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

    if not nljson_filepath:
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


def backup_index(index_name, save_dir=None, datetime_field="event_datetime"):
    """Read query, execute and write newline delimited json with results.

    This is useful to do a dumb backup of data.
      It was especially useful to extract data that needed to be re-indexed, but the cluster was full.

    :param index_name: Name of index to query.
    :type index_name: str
    :param save_dir: Filename to where to save.
    :type save_dir: str
    :param datetime_field: Field used to find oldest and newest
    :type datetime_field: str
    :return: None
    :rtype: None
    """
    min_res = ES.search(
        index=index_name,
        body={"_source": [datetime_field], "query": {"match_all": {}}, "sort": {datetime_field: "asc"}, "size": 1}
    )
    min_date = min_res.get("hits").get("hits")[0].get("_source").get(datetime_field)
    max_res = ES.search(
        index=index_name,
        body={"_source": [datetime_field], "query": {"match_all": {}}, "sort": {datetime_field: "desc"}, "size": 1}
    )
    max_date = max_res.get("hits").get("hits")[0].get("_source").get(datetime_field)
    filename = os.path.join(
        save_dir or os.path.dirname(os.path.abspath(__file__)),
        f"{index_name}_{min_date}_{max_date}.json.nl".replace(":", "")
    )
    dump_query_as_nl_json(index_name, "everything", filename)


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


def multithread_indexing(index, doc_type, docs_to_index):
    """Multithreaded indexing to Elasticsearch.

    :param index: Index name.
    :type index: str
    :param doc_type: doc_type property
    :type doc_type: str
    :param docs_to_index: An iterable of docs to index to ES.
    :type docs_to_index: Iterable of dict
    :return: None
    :rtype: None
    """
    import time
    from multiprocessing.pool import ThreadPool
    nr_threads = 10
    max_thead_queue_size = 5
    pool = ThreadPool(processes=nr_threads)

    for fetch_nr, doc in enumerate(docs_to_index):
        fetch_nr += 1
        if (fetch_nr+1) % 100 == 0:
            logging.info(f"Indexing {fetch_nr+1}")

        pool.apply_async(ES.index, kwargs={"index": index, "doc_type": doc_type, "body": doc})
        while pool._taskqueue.qsize() > max_thead_queue_size:
            time.sleep(0.1)

    pool.close()
    logging.info("waiting for processes to finish...")
    pool.join()

    logging.info(f"Done.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "index",
        help="What index to work with"
    )
    parser.add_argument(
        "--local_backup_dir",
        default=None,
        help="Filename where to back up to"
    )
    args = parser.parse_args()

    if args.local_backup_dir:
        backup_index(args.index, save_dir=args.local_backup_dir)

    # create_index(args.index)
    # reindex("ecomm", args.index)
    # inplace_index("ecomm", args.index)
    # dump_query_as_nl_json(args.index, "everything")
    # index_from_nl_json("result_ecomm_everything.json.nl", index_overwrite=args.index)
    # dump_query_as_csv(args.index, "socialwidget_grouped_userids", ["account_uuid", "page_uuid"])

    # create_index(args.index)

