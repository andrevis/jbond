db_name=$1
db_user=$2
db_pass=$3

CREATE USER $db_user PASSWORD '$db_pass';
CREATE DATABASE $db_user OWNER=$db_user;