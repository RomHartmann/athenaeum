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

Indeces are created automatically on post to that index.  But sometimes we want to define schema:


```python
from elasticsearch import Elasticsearch
es = Elasticsearch()

schema = {
    "mappings": {
        "test_type": {
            "properties": {
                "user": {
                    "type": "nested" 
                }
            }
        }
    }
}
es.indices.create(index='nested_ecomm', ignore=400, body=schema)
```

## How to data

Generally we interact with ES via a REST API.  

But there is a wrapper python:  https://elasticsearch-py.readthedocs.io/en/master/

```bash
pip install elasticsearch
# or
pip install -r requirements.txt
```

### Add data to ES:
```python
from elasticsearch import Elasticsearch
es = Elasticsearch()

doc = {
    'author': 'kimchy',
    'text': 'Elasticsearch: cool. bonsai cool.'
}
res = es.index(index="test-index", doc_type='test_type', body=doc)  # can set id=1 here.
```

### Query ES:

```python
from elasticsearch import Elasticsearch
es = Elasticsearch()
print(es.get(index="test-index", doc_type='test_type', id=1))  # or rather, whatever the real id is.
print(es.search(index="test-index", body={"query": {"match_all": {}}}))
```

### or via rest:

```python
import requests
import json
ret = requests.post(
    'http://localhost:9200/test-index/_search', 
    headers = {'Content-Type': 'application/json'}, 
    data=json.dumps(query)
)
print(ret)
ret.raise_for_status()
```

### A more complicated query

A query for this schema

```python
POM_SCHEMA = {
    "mappings": {
        "POM": {
            "properties": {
                "pom_path": {"type": "text"},
                "account_uuid": {"type": "text"},
                "page_uuid": {"type": "text"},
                "event_datetime": {"type": "date"},
                "pom_elements": {
                    "type": "nested",
                    "properties": {
                        "name": {"type": "keyword"},
                        "id": {"type": "text"},
                        "type": {"type": "keyword"},
                        "content": {
                            "type": "nested",
                            "properties": {
                                "html": {"type": "text"},
                                "label": {"type": "keyword"},
                                "text": {"type": "text"},
                                "title": {"type": "text"}
                            }
                        }
                    }
                }
            }
        }
    }
}
```

where we only want to return the actual html entries would look like this
```python
from elasticsearch import Elasticsearch
ES = Elasticsearch(
    hosts=[{'host': 'localhost', 'port': 9200, 'use_ssl': False}]
)
index = "ecomm"
query = {
  "_source" : ["pom_path", "event_datetime"],
  "query": {
    "nested": {
      "path": "pom_elements.content",
      "query": {
        "wildcard": {"pom_elements.content.html" : "*http*"}
      },
      "inner_hits": {} 
    }
  }
}
ret = ES.search(index=index, body=query)
print(ret)
```
