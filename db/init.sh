#!/bin/bash

db_name=$1
db_user=$2
db_pass=$3

# psql -U postgres -c "DROP DATABASE ${db_name};"
# psql -U postgres -c "DROP USER ${db_user};"

psql -U postgres ${db_pass} << EOF
CREATE USER ${db_user} PASSWORD '${db_pass}';
CREATE DATABASE ${db_name} OWNER=${db_user};
\c ${db_name};


CREATE TABLE IF NOT EXISTS options (
    id SERIAL,
    name VARCHAR(100),
    value text);
EOF
