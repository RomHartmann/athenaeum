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

.PHONY: backup-data
backup-data:
	echo "TODO!"

