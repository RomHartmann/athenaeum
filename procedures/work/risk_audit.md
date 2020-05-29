# Risk Audit

Good way to do readiness review.

Q: What are top 3 risks and way to mitigate?


## 1) Steady state

If a service is deployed and not touched again, could it run for the next year?

- Check inodes (pointer to keep track of files): `df -i`
- Run out of primary keys
- Traffic and traffic projections and traffic spikes
- Database table scans, indices, query patterns
- Database free disk space: 5GB and 10%
- Resources that require renewal and rotation (certs, api keys, tokens)

That said, don't overengineer and build for over-resilience.


## 2) Performance hot spots that could lead to saturation or db lockup

- Database: blocking threads, not batching, n+1 queries (query list of size n, query over each of n)
- Unbounded in-memory collection: gather all data into memory to then output.


## 3) Gaps in monitoring and alarms

Systems need:
- Monitoring for availability (cpu, memory, disk space, uptime)
- Monitoring for business outcome (eg. tasks running in given time, data sanity)

- response time, performance characteristics
- job scheduling
- Spending and costs
- Synthetic and real user monitoring - Performance SLOs


## 4) Gaps in Knowledge, process, ownership

Ensure:
- all members of team can deploy safely
- all members of team understand hystem's health, metrics and alarms
- regular, schedled maintainence is performed
  - dependencies and runtimes updated
  - Security vulnerabilities addressed
  - capacity plans updated

Do regular fire drills


## 5)  Existing risk from previous incidents

- post mortem action items


## 6)  Audit logs of services and database

- Go through logs, keep eye out for warnings and errors
  - Ensure warning and errors are useful indicators of instability
  - Fix or silence warnings and errors

## 7)  Analyze for any potential security vulnerabilities

- GDPR complience
- Take a look at owasp.org/www-project-top-ten/

- permission scoping


## 8) Identify dependencies on other services and understand risks

- rate limits
- other services are down, is our service resilient
  - Are healthchecks impacted by eg the database health? (no, database should not be part of service healthcheck)
- Graceful recovery
- Credentials rotation








