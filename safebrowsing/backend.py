from platform import node
import conf

class BaseDbObj(object):
    db_engine   = getattr(conf, 'DATABASE_ENGINE')
    db_name     = getattr(conf, 'DATABASE_NAME')
    db_user     = getattr(conf, 'DATABASE_USER')
    db_password = getattr(conf, 'DATABASE_PASSWORD')
    db_host     = getattr(conf, 'DATABASE_HOST', node())
    db_port     = getattr(conf, 'DATABASE_PORT')
    api_key     = getattr(conf, 'API_KEY')

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

    def insert_row(self, badware_code, url_hash):
        self.cursor.execute("INSERT INTO url_hashes_table (badware_type,url_hash) "
                            "VALUES ('%s','%s');" %(badware_code, url_hash))

    def delete_row(self, badware_code, url_hash):
        self.cursor.execute("DELETE FROM url_hashes_table WHERE badware_type='%s' "
                            "AND url_hash='%s';" %(badware_code, url_hash))

    def lookup_by_md5(self, md5_hash):
        if isinstance(md5, (str, unicode)):
            md5_hash = [md5_hash,]
        for md5h in md5_hash:
            self.cursor.execute("SELECT * FROM url_hashes_table WHERE url_hash='%s';" %(md5h))
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

    def insert_row(self, badware_code, url_hash):
        self.client.set(url_hash, badware_code)

    def delete_row(self, badware_code, url_hash):
        self.client.delete(url_hash, badware_code)

    def lookup_by_md5(self, md5_hash):
        if isinstance(md5_hash, (str, unicode)):
            md5_hash = [md5_hash,]
        for md5h in md5_hash:
            row = self.client.get(md5h)
            if not row:
                continue
            return row

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
