Property Recommender
====================

# Infrastructure

### Elasticsearch

This requires a local elasticsearch cluster.  Please see `athenaeum/infrastructure/elasticsearch` for details on how to set one up.


# How to use

### Data formats

All formats that have parsers written:
    - CSV


### Querying

- Define latlongs of where you'd like to be and weight of its importance.
- Cost requirements
- Bedrooms etc
- Square footage requirements
- Room requirements
- Pet requirements


# TODOS
enrichers:
    - ReverseGeolocationEnricher
    - ImageEnricher

indexers:
    - Bulk indexer
    - Update index for new enrichers and backfill for all. 
        - Also include 'updated_at' field in schema

parsers:
    - fill do_validate_schema method
    - Use generators instead of lists
    - Build the ScraperParser


Features:
- reverse geocoding
- Latlong query comparison
- google image processing of pictures









