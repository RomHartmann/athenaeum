.PHONY: start
start:
	docker-compose up


.PHONY: stop
stop:
	docker-compose down


.PHONY: destroy
destroy:
	docker-compose down -v

.PHONY: inspect
inspect:
	curl http://127.0.0.1:9200/_cat/health

.PHONY: rebalance
rebalance:
	curl -XPUT localhost:9200/_cluster/settings -H 'Content-Type: application/json' -d '{"persistent" : {"cluster.routing.allocation.disk.threshold_enabled": false}}'


.PHONY: backup-data
backup-data:
	python helpers.py $(INDEX) --local_backup $(SAVE_DIR)

