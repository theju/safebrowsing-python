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

class MySqlDbObj(BaseDbObj):
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


class PostgresqlDbObj(BaseDbObj):
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


DB_BACKENDS = {'sqlite3': SqliteDbObj, 'mysql': MySqlDbObj, 
               'postgresql': PostgresqlDbObj}


class DbObj(object):
    def __init__(self):
        backend = getattr(conf, 'DATABASE_ENGINE')
        if not backend in DB_BACKENDS:
            raise Exception("The DATABASE_ENGINE is not among the supported backends.")
        self.backend = DB_BACKENDS[backend]()
        

