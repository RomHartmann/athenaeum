Elasticsearch
=============

# Deploy

https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html

Everything is managed via the `Makefile`.


# How to use

## UI

A rudimentary UI is avaialable via the chrome extension `ElasticSearch Head`: chrome://extensions/?id=ffmkiejjmecolpfloofpjologoblkegm

This connects to ES on `http://localhost:9200/` by default.


## Create an Index

Indeces are created automatically on post to that index (at least when using the python api).

## How to data

Generally we interact with ES via a REST API.  

But there is a wrapper python:  https://elasticsearch-py.readthedocs.io/en/master/

```bash
pip install elasticsearch
# or
pip install -r requirements.txt
```

Add data to ES:
```python
from elasticsearch import Elasticsearch
es = Elasticsearch()

doc = {
    'author': 'kimchy',
    'text': 'Elasticsearch: cool. bonsai cool.'
}
res = es.index(index="test-index", doc_type='tweet', id=1, body=doc)
```

Query ES:

```python
from elasticsearch import Elasticsearch
es = Elasticsearch()
print(es.get(index="test-index", doc_type='tweet', id=1))
print(es.search(index="test-index", body={"query": {"match_all": {}}}))
```
