Elasticsearch
=============

# Deploy

https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html

[And to set heap size](https://www.elastic.co/guide/en/elasticsearch/reference/current/heap-size.html)

Everything is managed via the `Makefile`.


# How to use

## UI

A rudimentary UI is avaialable via the chrome extension [ElasticSearch Head](chrome://extensions/?id=ffmkiejjmecolpfloofpjologoblkegm)

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
es.indices.create(index='nested_poms', ignore=400, body=schema)
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

Say we have the schema in `./schemas/poms.json`

If we only want to return the actual html entries the query would look like this
```python
from elasticsearch import Elasticsearch
ES = Elasticsearch(
    hosts=[{'host': 'localhost', 'port': 9200, 'use_ssl': False}]
)
index = "poms"
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

To expand on that even more, here is a query if we want to have multi-level `inner_hits` and multi-level filters:


```json
{
  "_source": ["pom_path", "event_datetime"],
  "query": {
    "nested": {
      "path": "pom_elements",
      "inner_hits": {
        "_source": ["pom_elements.type", "pom_elements.id", "pom_elements.name", "pom_elements.content.html"]
      },
      "query": {
        "bool": {
          "must": [
            {
              "nested": {
                "path": "pom_elements.content",
                "query": {
                  "bool": {
                    "must": [
                      {"wildcard": {"pom_elements.content.html" : "*shopify*"}},
                      {"bool": {
                        "should": [
                          {"match": {"pom_elements.content.html":  "buy_button"}},
                          {"match": {"pom_elements.content.html":  "buy-button"}}
                        ],
                        "minimum_should_match": 1
                      }}
                    ],
                    "must_not": [
                      {"query_string":  {"query": "(pom_elements.content.html: \"sdks.shopifycdn.com\")"}}
                    ]
                  }
                }
              }
            }
          ],
          "must_not": [
            {"term": {"pom_elements.type" : "lp-stylesheet"}}
          ],
          "should": []
        }
      }
    }
  },
  "sort": ["_id"]
}
```


# Backing up an Index by creating a snapshot

More work than it is worth right now, but here is a nice how-to

https://blog.leandot.com/2017/03/04/create-elastic-search-snapshot-docker.html

Or using another little service:

https://github.com/webdestroya/elasticsearch-snapshot

Or creating snapshots in S3

https://hub.docker.com/r/heepster/docker-elasticsearch-s3-snapshot/


