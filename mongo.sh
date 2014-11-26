#!/bin/sh

{
    echo "This will repair MongoDB"

    sudo rm /var/lib/mongodb/mongod.lock
	mongod --dbpath /data/db --repair --repairpath /data/db0
	sudo service mongod restart

}
