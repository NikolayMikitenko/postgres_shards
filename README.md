# postgres_shards

## Simple table without partitions
### Create table
```
CREATE TABLE books (
id bigint not null,
category_id  int not null,
author character varying not null,
title character varying not null,
year int not null )
```

## Table patitioned by shards
### Create table on main shard
```
CREATE TABLE books (
id bigint not null,
category_id  int not null,
author character varying not null,
title character varying not null,
year int not null )
```

### Create table on shard 1
```
CREATE TABLE books (
id bigint not null,
category_id  int not null,
author character varying not null,
title character varying not null,
year int not null,
CONSTRAINT category_id_check CHECK ( category_id = 1 )
);
```

### Create table on shard 2
```
CREATE TABLE books (
id bigint not null,
category_id  int not null,
author character varying not null,
title character varying not null,
year int not null,
CONSTRAINT category_id_check CHECK ( category_id = 2 )
);
```

### Create index on table shard field
```
CREATE INDEX books_category_id_idx ON books USING btree(category_id);
```

### Create foreign data wrapper
```
CREATE EXTENSION postgres_fdw;
CREATE SERVER shard_1 FOREIGN DATA WRAPPER postgres_fdw OPTIONS( host 'postgres_shard_slave1', port '5432', dbname 'postgres' );
CREATE SERVER shard_2 FOREIGN DATA WRAPPER postgres_fdw OPTIONS( host 'postgres_shard_slave2', port '5432', dbname 'postgres' );
CREATE USER MAPPING FOR postgres SERVER shard_1 OPTIONS (user 'postgres', password 'postgres');
CREATE USER MAPPING FOR postgres SERVER shard_2 OPTIONS (user 'postgres', password 'postgres');
```

### Create foreign tables on main
```
CREATE FOREIGN TABLE books_shard_1 (
id bigint not null,
category_id  int not null,
author character varying not null,
title character varying not null,
year int not null )
SERVER shard_1
OPTIONS (schema_name 'public', table_name 'books');

CREATE FOREIGN TABLE books_shard_2 (
id bigint not null,
category_id  int not null,
author character varying not null,
title character varying not null,
year int not null )
SERVER shard_2
OPTIONS (schema_name 'public', table_name 'books');
```

## Perfomance test
### Without sharding
Change port in file perfomance.py to 25432 and run it:
```
python perfomance.py 
```
Output:
```
125.51816272735596
125.36468172073364
125.39356565475464
125.43316340446472
125.51160907745361
```

### With sharding
Change port in file perfomance.py to 25432 and run it:
```
python perfomance.py 
```
Output:
```
126.666579246521
126.83892488479614
126.8474497795105
127.01895332336426
127.48405337333679
```
