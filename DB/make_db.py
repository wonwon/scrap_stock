from class_sqlite import Database

with Database('db_netkeiba.sqlite') as db:
    db.execute('CREATE TABLE stock(\
        id INTEGER PRIMARY KEY AUTOINCREMENT,\
        code INTEGER,\
        date varchar(50),\
        volume integer,\
        open integer,\
        close integer,\
        high integer,\
        low integer,\
        ratio integer,\
        marginbuy integer,\
        marginsale integer\
        )')