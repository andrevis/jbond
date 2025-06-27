#!/bin/bash

db_name=$1
db_user=$2
db_pass=$3


psql -U postgres -c "CREATE USER ${db_user} PASSWORD '${db_pass}';"
psql -U postgres -c "CREATE DATABASE ${db_name} OWNER=${db_user};"