#-------------------------------------------------------------------------------
# Name:        UpdateDB
# Purpose:     Initializes and loads the database with updated data
#
# Author:      Daniel Fourquet
# Created:     Feb 2021
#-------------------------------------------------------------------------------

import psycopg2, psycopg2.extras
import csv
import json
import os


basePath = os.path.dirname(os.path.abspath(__file__))

# Config file for db connection
configPath = f'{basePath}\\config.json'

# DDL file for creating required tables
dbInitPath = f'{basePath}\\dbInit.sql'

# Input data paths
fmQueryPath = f'{basePath}\\data\\fmQuery.txt'
serviceContoursPath = f'{basePath}\\data\\FM_service_contour_current.txt'
formatsPath = f'{basePath}\\data\\formats.csv'
serviceRadiiPath = None




# Helper classes to process data for loading to the database
class Station:
    def __init__(self, data):
        self.callsign = data['callsign']
        self.frequency = data['frequency']
        self.service = data['service']
        self.directional = data['directional']
        self.fmStatus = data['fmStatus']
        self.city = data['city']
        self.state = data['state']
        self.country = data['country']
        self.fileNumber = data['fileNumber']
        self.erpHorizontal = data['erpHorizontal']
        self.erpVertical = data['erpVertical']
        self.haatHorizonal = data['haatHorizonal']
        self.haatVertical = data['haatVertical']
        self.ID = data['ID']
        self.lat = data['lat']
        self.latD = float(data['latD'])
        self.latM = float(data['latM'])
        self.latS = float(data['latS'])
        self.lng = data['lng']
        self.lngD = float(data['lngD'])
        self.lngM = float(data['lngM'])
        self.lngS = float(data['lngS'])
        self.licensee = data['licensee']

    def as_tuple(self):
        """ Returns data as tuple to be consumed by psycopg2's
            execute_values function """
        return (self.callsign,self.frequency,self.service,self.directional,
                self.fmStatus,self.city,self.state,self.country,
                self.fileNumber,self.erpHorizontal,self.erpVertical,
                self.haatHorizonal,self.haatVertical,self.ID,self.lat,
                self.latD,self.latM,self.latS,self.lng,self.lngD,self.lngM,
                self.lngS,self.licensee)


class ServiceContour:
    def __init__(self, data):
        pass

    def as_tuple(self):
        """ Returns data as tuple to be consumed by psycopg2's
            execute_values function """


class Format:
    def __init__(self, data):
        self.callsign = data['callsign']
        self.format = data['format']
    
    def as_tuple(self):
        """ Returns data as tuple to be consumed by psycopg2's
            execute_values function """
        return (self.callsign, self.format)


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
    """ Performs the needed tasks to update the database 
        1 - Create tables
            a - Stations
            b - ServiceContours
            c - EstimatedServiceRadii
            d - Formats
        
        2 - Load data into tables

        3 - Refresh MVs
    """
    
    # Connect to the database and create cursor
    conn = connect()
    cur = conn.cursor()

    # Create tables if they don't exist.  dbInit.sql will drop all tables
    # if they exist and create them again to be loaded with fresh data
    dbInit = open(dbInitPath, 'r').read()
    cur.execute(dbInit)

    # Load stations data
    with open(fmQueryPath, 'r') as file:
        print("Loading stations data...")

        # Load values as list of tuples
        values = []
        for line in file.readlines():
                row = line.split("|")
                try:
                    data = {
                        "callsign": row[1].strip(),
                        "frequency": row[2].strip(),
                        "service": row[3].strip(),
                        "directional": row[5].strip(),
                        "fmStatus": row[9].strip(),
                        "city": row[10].strip(),
                        "state": row[11].strip(),
                        "country": row[12].strip(),
                        "fileNumber": row[13].strip(),
                        "erpHorizontal": row[14].strip(),
                        "erpVertical": row[15].strip(),
                        "haatHorizonal": row[16].strip(),
                        "haatVertical": row[17].strip(),
                        "ID": row[18].strip(),
                        "lat": row[19].strip(),
                        "latD": row[20].strip(),
                        "latM": row[21].strip(),
                        "latS": row[22].strip(),
                        "lng": row[23].strip(),
                        "lngD": row[24].strip(),
                        "lngM": row[25].strip(),
                        "lngS": row[26].strip(),
                        "licensee": row[27].strip()
                    }
                    station = Station(data)
                    values.append(station.as_tuple())
                except:
                    print(f'    Error on {row}')

        # Insert values list to stations table
        sql = "insert into stations values %s"
        psycopg2.extras.execute_values(cur, sql, values)
        print("Done\n")


    # Load service contours


    # Load service radii


    # Load formats
    with open(formatsPath, newline='') as csvFile:
        print("Loading formats data...")
        r = csv.DictReader(csvFile)
        
        # Load values as list of tuples
        values = []
        for row in r:
            record = Format(row)
            values.append(record.as_tuple())

        # Insert values list to formats table
        sql = "insert into formats (callsign, format) values %s"
        psycopg2.extras.execute_values(cur, sql, values)
        print("Done\n")

    conn.commit()
    cur.close()
    conn.close()

    print('done')


if __name__ == "__main__":
    print('start test')
    update_db()