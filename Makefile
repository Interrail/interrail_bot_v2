CURRENT_DIR=$(shell pwd)
include .env

upgrade:
	docker service update --force --image ${REGISTERY}/${PROJECT}:${TAG} ${STACK}_${PROJECT}

services:
	docker stack services ${STACK}

build-image:
	docker build --rm -t ${REGISTERY}/${PROJECT}:${TAG} .

run-prod:
	set -a &&. ./.env && set +a && docker-compose -f docker-compose.yml up -d