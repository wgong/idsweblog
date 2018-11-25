#!/bin/bash
set -e
#        alter table weblogs add source varchar(10);

psql -v ON_ERROR_STOP=1 --username dbuser --dbname testdb <<-EOSQL
        CREATE TABLE  weblogs (day date, status varchar(3), source varchar(10));
EOSQL
