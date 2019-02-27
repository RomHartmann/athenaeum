.PHONY: start-cluster
start-cluster:
	docker-compose up


.PHONY: stop-cluster
stop-cluster:
	docker-compose down


.PHONY: destroy-cluster
destroy-cluster:
	docker-compose down -v

.PHONY: inspect-cluster
inspect-cluster:
	curl http://127.0.0.1:9200/_cat/health

