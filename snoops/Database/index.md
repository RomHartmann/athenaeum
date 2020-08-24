Database Index
==============

An index is any data structure that improves the performance of lookup.

# General principles

## Supporting fast lookup

### General Index analogy

Say we have deck of cards.  If we want a specific card, then it takes on averate 26 cards to find one we want
by going through each card individually.

If we separate cards into suits, it takes (2 + 7) = 9 flips on average to find card.

Index is is a segregation and sorting of data on keys, such that we can find data faster.


### B+ Tree index

In general databases implement a "B+ tree".  It is a tree algorith that separates and sorts data according to some
property of the key (eg integer size buckets, or first letter of string etc.)

This way, by layering multiple layers of buckets (say, first layer is first letter of string, second is second etc.) we 
can achieve an exponentially increased search time in large databases.

Modern databases generally have algorithms that shift the data and key values between the blocks within the tree to maintain balance.


### Cost

Additional writes and storage space to maintain index data structure.



## Policing database constraints

The index is also what polices constraintes such as UNIQUE, PRIMARY_KEY and FOREIGN_KEY.



# Specific implementations

## Elasticsearch

### Inverted Index
Where relational databases add an index such as B-tree to specific columns in order to improve the speed of data retrieval,
Elasticsearch and Lucene use a structure called _inverted index_ for the same purpose.

- By default every field in a document is indexed, which means it has an inverted index.
- Thismakes it searchable.
- A field without an inverted index is not searchable.

In ES, all data in every field is indexed.

Here are the docs about it: https://www.elastic.co/guide/en/elasticsearch/guide/current/inverted-index.html

But in short, it's the process of running an analyzer on a (generally) text field and storing counts of matches in index.

And more detailed docs: https://www.elastic.co/blog/found-elasticsearch-from-the-bottom-up



