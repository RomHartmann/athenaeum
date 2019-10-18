# CAP Theorem

- C = Consistency: A read returns the most recent data (or an error)
- A = Availability: A read always returns a non-error but not necessarily most recent data.
- P = Partition Tolerance: Data is distributed across nodes even in the case of delays or faults.

Most distributed systems must have partition tolerance, so we are left with two options:
- Availabiliy: Return whatever appears to be the most recent data immediately, even if it is incorrect.
- Consistency: Fail if data is not most recent, or wait until it is (eventual consistency)



## Different Databases:

### Postgres

Postgres is not distributed


### Elasticsearch

- ES little bit gives up on Partition Tolerance.  This means that if enough nodes fail
the cluster turns red and ES does not proceed to operate on that index.  But, an index
can survive a network split, hence it preserves P.
- ES gives up on consistency (a little bit), like most NoSQL databases, since it is eventually consistent.
- ES is Available: Every request will be responded.

Indexing in ES:
- All operations are written to the WAL
  - WAL (write-ahead log): Modifications are written to a log before they are applied.
- Operations are then sent to all the nodes
- If a node is not functioning then the cluster is ok as long as replication is high enough
  - When a stopped node rejoins; initiate recovery using the WAL
    - A "best" WAL created of all consistent replicas - this is used for recovery.


Turns out databases generally don't fully give up on any single component, but a little bit on all
in order to try to have all of them.






