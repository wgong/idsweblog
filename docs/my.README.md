
## general workflow

    $ docker ps
    $ docker-compose build
    $ docker-compose up
    $ docker-compose down

## test

open browser at http://localhost:8080/

## debugging

### ModuleNotFoundError: `utils`

ingestion_1_d625657adb25 |   File "ingestion.py", line 6, in <module>
ingestion_1_d625657adb25 |     from utils import parse_log, is_get_request
ingestion_1_d625657adb25 | ModuleNotFoundError: No module named 'utils'

**fix**

- add in ingestion/Dockerfile

    COPY utils.py .

### NameError: name 'sys' is not defined in ingestion.py

**fix**

- add `import sys`

### simplify debugging process

**fix**

- trim `ingestion/weblogs.log` 52MB file size down to 4 lines

- improve print()


### role "dbusr" does not exist
db_1_45bd2fa92737 | /usr/local/bin/docker-entrypoint.sh: running /docker-entrypoint-initdb.d/init-tables.sh
db_1_45bd2fa92737 | FATAL:  role "dbusr" does not exist
db_1_45bd2fa92737 | psql: FATAL:  role "dbusr" does not exist

**fix**

- bring up db container

    $ docker-compose up db

- find container name= weblog_db_1_45bd2fa92737

    $ docker ps

- log into CONTAINER

    $ docker exec -it weblog_db_1_45bd2fa92737 bash

- create user/pwd in postgresql + database manually

    $ psql -U postgres

    alter user postgres password 'postgres';
    alter user dbuser password 'dbuser';

    CREATE DATABASE testdb;
    \l
    \c testdb;

    CREATE TABLE  weblogs (
           day    date,
           status varchar(3)
           );

    \q

    $ psql -U dbuser testdb

    \dS weblogs;

 Column |         Type         | Modifiers
--------+----------------------+-----------
 day    | date                 |
 status | character varying(3) |

    \q

- stop db container

    $ docker stop 6708542d62b9

### persist postgresql db data

**fix**

db:
  image: "postgres:9.6.5"
  volumes:
    #- ./docker-entrypoint-initdb.d/init-tables.sh:/docker-entrypoint-initdb.d/init-tables.sh
    - /var/dbdata/pgdata:/var/lib/postgresql/data

### extra-credit task

- alter table by connecting to postgresql container directly

    $ docker-compose up db
    $ docker ps # get container_id=weblog_db_1_7c4480eab75e
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

- revise ingestion/ingestion.py to add source to rabbitmq json msg
- revise processing/processing.py to add source to SQL INSERT statement
- revise app.py by adding extra SQL queries for source=`remote`
- revise template/index.html to use HTML table
