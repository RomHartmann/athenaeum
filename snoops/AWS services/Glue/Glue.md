# AWS Glue

- Managed ETL service that runs serverless spark.
  - E: Loads data from a S3 bucket or Glue table
  - T: essentially pandas transformations.
  - L: Loads back into S3 as table in veriety of formats



## Glue ETL

eg: https://github.com/aws-samples/aws-glue-samples/blob/master/examples/data_cleaning_and_lambda.py

- Doing Glue ETL requires the Glue Data Catalog to be populated first, which is generally done via the AWS glue crawler
  - This is also possible by using Hive DDL statements - I.e `MSCK REPAIR`
    - https://medium.com/datadriveninvestor/glue-crawler-optimization-alternative-athena-use-case-15cc5bdd94d6
  - DDL is cheaper, but Crawler should deal with frequently changing data better


Triggering a job: https://docs.aws.amazon.com/glue/latest/dg/about-triggers.html


### Streaming ETL

https://docs.aws.amazon.com/glue/latest/dg/add-job-streaming.html





## Crawlers

- Also detects schemas + register partitions
- Should be faster than `MSCK REPAIR`
- Best practice doc: https://docs.aws.amazon.com/athena/latest/ug/glue-best-practices.html














