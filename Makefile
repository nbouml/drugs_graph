SHELL=/bin/bash

ifneq (,$(wildcard ./drugs_graph/conf/.env))
    include ./drugs_graph/conf/.env
    export
endif

.PHONY: build
build:
	sudo docker build . -t dgraph

.PHONY: run
run:
	sudo docker run dgraph > ${DRUGS_GRAPH_DOCKER_OUTPUT_PATH}/${DRUGS_GRAPH_OUTPUT_FILE}
