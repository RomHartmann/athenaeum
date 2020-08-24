# Athena basics

Athena uses:
- Metastore:
  - Glue Catalog: central metadata repository
    OR
  - Hive: A framework that stores metadata like table definitions
    - Manage partitions using Hive Metastore
    - Hive itself is also a query language for Hadoop MapReduce
- Presto: Query engine (SQL) for distributed file systems (eg HDFS or S3)

Recommendations:
- Use Athena for short queries, EMR for long queries (30+ minutes)
- Never query without filters over partitions if able.

Limitations:
- Athena has 30 minute query limit
- 20 concurrent active queries 
- 5 API calls per second (It varies on type, but this is the strictest limit)

Abilities:
- Complex joins, window functions and datatypes

## Performance for Athena

This is a goldmine:
- https://aws.amazon.com/blogs/big-data/top-10-performance-tuning-tips-for-amazon-athena/


## Partitioning

- Hive partitioning follows:
  Partition column name followed by an equal symbol (‘=’) and then the value.
  `s3://yourBucket/pathToTable/<PARTITION_COLUMN_NAME>=<VALUE>/<PARTITION_COLUMN_NAME>=<VALUE>/`
    - This format allows the Hive `MSCK REPAIR` table command to add partitions to your table automatically.



## Good links
- https://medium.com/@rchamarthi/aws-athena-notes-90a8e2554367

