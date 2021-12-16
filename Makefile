ifneq (,$(wildcard ./.env))
    include .env
    export
endif

.PHONY : install init_db upgrade_db build purge_db

build : install start_db

install :
	pip install -r requirements.txt

init_db :
	mkdir databases
	flask db init --multidb

upgrade_db :
	flask db migrate
	flask db upgrade

start_db : init_db upgrade_db

purge_db :
ifeq ($(FLASK_ENV), production)
		echo "You cannot do it in a production environment"
else ifeq ($(FLASK_ENV), '')
		echo "You cannot do it in a production environment"
else
		rm -rf migrations;
		rm -rf databases;
endif