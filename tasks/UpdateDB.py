#-------------------------------------------------------------------------------
# Name:        UpdateDB
# Purpose:     Initializes and loads the database with updated data
#
# Author:      Daniel Fourquet
# Created:     Feb 2021
#-------------------------------------------------------------------------------

import psycopg2, psycopg2.extras
import json
import os

basePath = os.path.dirname(os.path.abspath(__file__))
configPath = f'{basePath}\config.json'
dbInitPath = f'{basePath}\dbInit.sql'


# Helper classes to process data for loading to the database
class Station:
    def __init__(self, data):
        pass

class ServiceContour:
    def __init__(self, data):
        pass

class Format:
    def __init__(self, data):
        pass


def connect():
    """ Load the configuration file and return a connection to the database """
    config = json.load(open(configPath))["database"]
    conn = psycopg2.connect(
        dbname=config["dbname"], 
        user=config["user"], 
        password=config["password"],
        host = config["host"],
        port = config["port"]
    )

    return conn


def update_db():
    """ Performs the needed tasks to update the database """
    
    # Connect to the database and create cursor
    conn = connect()
    cur = conn.cursor()

    # Create tables if they don't exist
    dbInit = open(dbInitPath, 'r').read()
    cur.execute(dbInit)

    sql = "insert into formats (callsign, format) values %s"
    data = [('whro','test'), ('wrox', 'test'), ('wrox', 'ha')]
    psycopg2.extras.execute_values(cur, sql, data)

    conn.commit()
    cur.close()
    conn.close()

    print('done')


if __name__ == "__main__":
    print('start test')
    update_db()