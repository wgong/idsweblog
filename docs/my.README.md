*** workflow

$ docker-compose build
$ docker-compose up
$ docker-compose down


* issue =====================
ingestion_1_d625657adb25 |   File "ingestion.py", line 6, in <module>
ingestion_1_d625657adb25 |     from utils import parse_log, is_get_request
ingestion_1_d625657adb25 | ModuleNotFoundError: No module named 'utils'

** fix
add in ingestion/Dockerfile
COPY utils.py .

?? not working

* issue =====================
ingestion/weblogs.log is too big

** fix
to simplify debug, trim it down to 4 lines

* issue =====================
db_1_45bd2fa92737 | /usr/local/bin/docker-entrypoint.sh: running /docker-entrypoint-initdb.d/init-tables.sh
db_1_45bd2fa92737 | FATAL:  role "dbusr" does not exist
db_1_45bd2fa92737 | psql: FATAL:  role "dbusr" does not exist

** fix
# bring up db container
$ docker-compose up db

# find container name= weblog_db_1_45bd2fa92737
$ docker ps

# get into CONTAINER
$ docker exec -it weblog_db_1_45bd2fa92737 bash

create user/pwd in postgresql manually
$ psql -U postgres
alter user postgres password 'postgres';
\q

$ psql -U dbuser testdb
alter user dbuser password 'dbuser';

CREATE TABLE  weblogs (
       day    date,
       status varchar(3)
       );

\q

# stop db container
$ docker stop 6708542d62b9

* issue =====================
processing_1_a7cd1a491239 | psycopg2.OperationalError: could not translate host name "db" to address: Name or service not known

** fix
change host='db' to host='localhost'

conn = psycopg2.connect(host='localhost', database=os.environ['POSTGRES_DB'], user=os.environ['POSTGRES_USER'], password=os.environ['POSTGRES_PASSWORD'])

how to persist postgresql db data

db:
  image: "postgres:9.6.5"
  volumes:
    #- ./docker-entrypoint-initdb.d/init-tables.sh:/docker-entrypoint-initdb.d/init-tables.sh
    - /var/dbdata/pgdata:/var/lib/postgresql/data

** extra-credit task
$ docker-compose up db
$ docker ps # get container_id=weblog_db_1_7c4480eab75e

# alter table by connecting to postgresql container directly
$ docker exec -it weblog_db_1_7c4480eab75e bash

root@ec7bf38746e7:/# psql -U dbuser testdb

testdb=# \dS weblogs
          Table "public.weblogs"
 Column |         Type         | Modifiers
--------+----------------------+-----------
 day    | date                 |
 status | character varying(3) |

alter table weblogs add source varchar(10);
\q
