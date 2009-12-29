import conf
from base import BaseDbObj

class SqliteDbObj(BaseDbObj):
    def __init__(self):
        try:
            import sqlite3 as sqlite
        except ImportError:
            from pysqlite2 import dbapi2 as sqlite

        self.connection = sqlite.connect(self.db_name)
        self.cursor = self.connection.cursor()

    def get_version(self, badware_type):
        self.cursor.execute("select * from %s_version;" %(badware_type))
        row = self.cursor.fetchall()
        if not row:
            return None
        return row[0][0]

    def insert_version_row(self, badware_type, version_number):
        self.cursor.execute("INSERT INTO %s_version (version_number) VALUES "
                            "('%s');" %(badware_type, version_number))        

    def update_version_row(self, badware_type, new_version_number, version_number):
        self.cursor.execute("UPDATE %s_version SET version_number='%s' WHERE "
                            "version_number='%s';" %(badware_type, new_version_number, 
                                                     version_number))

    def insert_rows(self, url_hash_dict):
        for (url_hash, badware_code) in url_hash_dict.items():
            self.cursor.execute("INSERT INTO url_hashes_table (badware_type,url_hash) "
                                "VALUES ('%s','%s');" %(badware_code, url_hash))
        self.connection.commit()
        self.connection.close()

    def delete_rows(self, url_hash_dict):
        for (url_hash, badware_code) in url_hash_dict.items():
            self.cursor.execute("DELETE FROM url_hashes_table WHERE badware_type='%s' "
                                "AND url_hash='%s';" %(badware_code, url_hash))

    def lookup_by_md5(self, md5_hash_list):
        for md5_hash in md5_hash_list:
            self.cursor.execute("SELECT * FROM url_hashes_table WHERE url_hash='%s';" %(md5_hash))
            row = self.cursor.fetchall()
            if not row:
                continue
            # If row is non-empty then the URL is in 
            # database and stop operation by returning 1
            return row[0][0]

class MySqlDbObj(SqliteDbObj):
    def __init__(self):
        try:
            import MySQLDb
        except ImportError:
            raise Exception("Python Db library (MySQLDb) not found.")

        kwargs = {}
        if self.db_user:
            kwargs['user'] = self.db_user
        if self.db_name:
            kwargs['Db'] = self.db_name
        if self.db_password:
            kwargs['passwd'] = self.db_password
        if self.db_host.startswith('/'):
            kwargs['unix_socket'] = self.db_host
        elif self.db_host:
            kwargs['host'] = self.db_host
        if self.db_port:
            kwargs['port'] = int(self.db_port)

        self.connection = MySQLDb.connect(**kwargs)
        self.cursor = self.connection.cursor()


class PostgresqlDbObj(SqliteDbObj):
    def __init__(self):
        try:
            import psycopg2 as Database
        except ImportError:
            try:
                import psycopg as Database
            except ImportError:
                raise Exception("Libraries psycopg2/psycopg not found.")

        conn_string = ""
        if not self.db_name:
            raise Exception("Database name not specified.")
        conn_string += "dbname=%s" %self.db_name
        if self.db_user:
            conn_string += " user=%s %s" %(self.db_user, conn_string)
        if self.db_password:
            conn_string += " password='%s'" %self.db_password
        if self.db_host:
            conn_string += " host=%s" %self.db_host
        if self.db_port:
            conn_string += " port=%s" % self.db_port

        self.connection = Database.connect(conn_string)
        self.cursor = self.connection.cursor()

class MemcachedDbObj(BaseDbObj):
    def __init__(self):
        try:
            import memcache
        except ImportError:
            raise Exception("Could not find the memcached module.")
        if isinstance(self.db_host, (str, unicode)):
            self.db_host = [self.db_host,]
        if isinstance(self.db_port, (int, str, unicode)):
            self.db_port = [self.db_port, ]
        servers = ["%s:%s" %(ii[0], ii[1]) for ii in zip(self.db_host, self.db_port)]
        self.client = memcache.Client(servers)

    def get_version(self, badware_type):
        return self.client.get("%s_version" %(badware_type))

    def insert_version_row(self, badware_type, version_number):
        self.client.set("%s_version" %badware_type, version_number)

    def update_version_row(self, badware_type, new_version_number, version_number):
        self.client.set("%s_version" %badware_type, version_number)

    def insert_rows(self, url_hash_dict):
        self.client.set_multi(url_hash_dict)

    def delete_rows(self, url_hash_dict):
        self.client.delete_multi(url_hash_dict.keys())

    def lookup_by_md5(self, md5_hash_list):
        hash_row = self.client.get_multi(md5_hash_list)
        if not hash_row:
            return None
        return hash_row.values()[0]

DB_BACKENDS = {'sqlite3'     : SqliteDbObj, 
               'mysql'       : MySqlDbObj, 
               'postgresql'  : PostgresqlDbObj, 
               'memcached'   : MemcachedDbObj,}

class DbObj(object):
    def __init__(self):
        backend = getattr(conf, 'DATABASE_ENGINE')
        if not backend in DB_BACKENDS:
            raise Exception("The DATABASE_ENGINE is not among the supported backends.")
        self.backend = DB_BACKENDS[backend]()
