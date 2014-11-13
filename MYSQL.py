import mysql.connector
from mysql.connector import errorcode
import logging

database = 'alpha'

TABLES = {}

TABLES['info'] = (
        "CREATE TABLE `info` ("
        "  `id` mediumint unsigned NOT NULL,"
        "  `name` varchar(20) NOT NULL,"
        "  `author` varchar(10) NOT NULL,"
        # this should be a enum/int type, save it for later!!!
        "  `market` varchar(6) NOT NULL,"
        # the fitting universe
        "  `uid` smallint unsigned NOT NULL,"
        # this should be a enum/int type, save it for later!!!
        "  `category` varchar(20) NOT NULL,"
        "  `entrydate` date NOT NULL,"
        "  `status` enum('FAIL', 'PROD', 'OSTEST', 'HOLD') NOT NULL,"
        "  `proddate` date,"
        "  `enddate` date,"
        "  PRIMARY KEY (`id`), UNIQUE KEY `id` (`id`)"
        ") ENGINE=InnoDB")

TABLES['score'] = (
        "CREATE TABLE `score` ("
        "  `id` mediumint unsigned NOT NULL,"
        "  `date` date NOT NULL,"
        "  `sid` varchar(6) NOT NULL,"
        "  `score` float,"
        "  PRIMARY KEY (`id`, `date`, `sid`)"
        ") ENGINE=InnoDB")

TABLES['uinfo'] = (
        "CREATE TABLE `uinfo` ("
        "  `id` smallint unsigned NOT NULL,"
        "  `name` varchar(20) NOT NULL,"
        "  PRIMARY KEY (`id`), UNIQUE KEY `id` (`id`)"
        ") ENGINE=InnoDB")

TABLES['universe'] = (
        "CREATE TABLE `universe` ("
        "  `id` smallint unsigned NOT NULL,"
        "  `date` date NOT NULL,"
        "  `sid` varchar(6) NOT NULL,"
        "  `valid` bool NOT NULL,"
        "  PRIMARY KEY (`id`, `date`, `sid`), UNIQUE KEY (`id`, `date`, `sid`)"
        ") ENGINE=InnoDB")

TABLES['performance'] = (
        "CREATE TABLE `performance` ("
        "  `id` mediumint unsigned NOT NULL,"
        "  `uid` smallint unsigned NOT NULL,"
        "  `date` date NOT NULL,"
        "  `ic` float,"
        "  `ic_5` float,"
        "  `ic_20` float,"
        "  `turnover` float,"
        "  `ac` float,"
        "  `ac_5` float,"
        "  `ac_20` float,"
        "  `returns` float,"
        "  PRIMARY KEY (`id`, `uid`, 'date'), UNIQUE KEY ('id', 'uid', 'date')"
        ") ENGINE=InnoDB")


def create_database(cursor):
    try:
        cursor.execute(
                "CREATE DATABASE {0} DEFAULT CHARACTER SET 'utf8'".format(database))
    except mysql.connector.Error as err:
        logging.error('Failed to create database:\n{0}'.format(err))
        exit(1)


if __name__ == '__main__':

    connection = mysql.connector.connect(user='wang', password='lwang')
    cursor = connection.cursor()

    try:
        connection.database = database
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cursor)
            connection.database = database
        else:
            logging.error(err)
            exit(1)

    for name, ddl in TABLES.iteritems():
        try:
            logging.info('Creating table {0!r} ...'.format(name))
            cursor.execute(ddl)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                logging.error('... {0!r} already exists'.format(name))
            else:
                logging.error(err)
                exit(1)
        logging.info('OK')

    cursor.close()
    connection.close()
