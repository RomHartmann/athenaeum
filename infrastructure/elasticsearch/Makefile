.PHONY: start
start:
	docker-compose up


.PHONY: stop
stop:
	docker-compose down


.PHONY: restart
restart:
	docker-compose restart


.PHONY: destroy
destroy:
	docker-compose down -v


.PHONY: inspect
inspect:
	curl http://127.0.0.1:9200/_cat/health


.PHONY: rebalance
rebalance:
	curl -XPOST localhost:9200/_flush
	curl -XPUT localhost:9200/_cluster/settings -H 'Content-Type: application/json' -d '{"persistent" : {"cluster.routing.allocation.disk.threshold_enabled": false}}'
	curl -XPUT localhost:9200/_cluster/settings -H 'Content-Type: application/json' -d '{"persistent" : {"cluster.routing.allocation.enable": "all"}}'
	curl -XPUT localhost:9200/_cluster/settings -H 'Content-Type: application/json' -d '{"persistent" : {"cluster.routing.allocation.disk.threshold_enabled": true}}'


.PHONY: backup-data
backup-data:
	python helpers.py $(INDEX) --local_backup $(SAVE_DIR)
