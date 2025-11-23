#!/bin/sh

echo "--> Waiting for db to be ready"
./wait-for-it.sh db:5432

echo "--> Starting celery process"
celery -A orgniaztional_ticking_api.tasks worker -l info --without-gossip --without-mingle --without-heartbeat
