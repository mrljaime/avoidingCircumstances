# coding=utf-8

import pymysql.cursors
import requires


class DBConnection:
    """
    Database wrapper
    """
    host = None
    port = None
    database = None
    username = None
    password = None

    conn = None

    def __init__(self, host, port, database, username, password):
        """
        DBConnection constructor
        :param host:
        :param port:
        :param database:
        :param username:
        :param password:
        """

        self.host = host
        self.port = port
        self.database = database
        self.username = username
        self.password = password

        self.start_connection()

    def start_connection(self):
        """"
        Start connection to MySQL/MariaDB
        """
        try:
            self.conn = pymysql.connect(host=self.host,
                                        user=self.username,
                                        passwd=self.password,
                                        db=self.database,
                                        port=self.port,
                                        cursorclass=pymysql.cursors.DictCursor)

            requires.logger.debug("New connection to database")

        except ValueError as error:
            requires.logger.error("THere's an error trying to obtain connection to database")

    def ping(self):
        """
        Ping and reconnect to database if connection is lose
        :return:
        """
        try:
            self.conn.ping(True)
            requires.logger.debug("On ping to database with reconnect True")
        except ValueError as error:
            requires.lgger.error("There's an error on ping to database: %s" % error)

    def exec_query(self, **args):
        """
        Execute query that doesn't return values
        :param args:
        :return affected rows
        """
        self.ping()
        affected = 0

        try:

            with self.conn.cursor() as cursor:
                affected = cursor.execute(args[0], (args[1:]))

        except ValueError as error:
            requires.logger.error("There's an error executing query: %s" % error)

        self.conn.commit()

        return affected

    def query(self, query, values=None):
        """
        :param query:
        :param values:

        :return :rtype dict:
        """
        self.ping()
        requires.logger.debug("On query to database")
        result = None

        try:
            requires.logger.debug("Before open cursor")
            with self.conn.cursor() as cursor:
                requires.logger.debug("On open cursor")
                try:
                    cursor.execute(query, values)
                except ValueError as error:
                    requires.logger.error("There's an error executing query: %s" % error)

                result = cursor.fetchall()

        except ValueError:
            requires.logger.error("There's an error doing query to database")

        return result

    def testing_insert(self):
        self.ping()
        try:
            with self.conn.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
                cursor.execute(sql, ('webmaster@python.org', 'very-secret'))

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            self.conn.commit()

            with self.conn.cursor() as cursor:
                # Read a single record
                sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                cursor.execute(sql, ('webmaster@python.org',))
                result = cursor.fetchone()
                print(result)
        finally:
            pass