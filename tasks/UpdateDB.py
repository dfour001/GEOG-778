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
from requests import get, exceptions


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
        # self.dist_40dBu = None # For testing
        self.dist_40dBu = self.get_CURVES_distance(40, self.haatHorizonal, self.erpHorizontal)

    def as_tuple(self):
        """ Returns data as tuple to be consumed by psycopg2's
            execute_values function """
        return (self.callsign,self.frequency,self.service,self.directional,
                self.fmStatus,self.city,self.state,self.country,
                self.fileNumber,self.erpHorizontal,self.erpVertical,
                self.haatHorizonal,self.haatVertical,self.ID,self.dist_40dBu,
                self.lat,self.latD,self.latM,self.latS,self.lng,self.lngD,
                self.lngM,self.lngS,self.licensee)

    def get_CURVES_distance(self, dBu, HAAT, ERP):
        """ Uses the CURVES api from the FCC to estimate the distance
            that the FM signal will decay to the input dBu value, given
            the Hight Above Average Terrain (HAAT) and Effective Radiation 
            Power (ERP).  Returns the distance in KM.

            Inputs:
                dBu - Field strength to which the distance will be estimated
                HAAT - Hight above average terrain
                ERP - Effective radiation power
        """

        try:
            # If erpHorizontal is invalid, try vertical
            if '-' in ERP:
                ERP = self.erpVertical

            # Strip the units
            ERP = ERP.split(' ')[0]

            url = f'https://geo.fcc.gov/api/contours/distance.json?computationMethod=0&serviceType=fm&haat={HAAT}&field={dBu}&erp={ERP}&curve=0&outputcache=true'
            r = get(url)
            r.raise_for_status()
            rDict = json.loads(r.text)
            distance = rDict['distance']

            return distance

        except exceptions.HTTPError as e:
            print(f'Error on {self.ID} {self.frequency} {self.callsign}')
            print(e)
            return None


class ServiceContour():
    def __init__(self, data):
        self.id = data["ID"]
        self.service = data["service"]
        self.geom = self.create_geom(data["coords"])

    def as_tuple(self):
        """ Returns data as tuple to be consumed by psycopg2's
            execute_values function """
        return (self.id, self.service, self.geom)

    def create_geom(self, coords):
        # Create a list of coordinates in this format: 'lat lng' to
        # build a wkt linestring
        coordList = []
        for coord in coords:
            try:
                c = coord.split(',')
                coordList.append(f'{c[1].strip()} {c[0].strip()}')
            except:
                pass

        # Build wkt linestring
        outputCoords = ''
        for coord in coordList:
            outputCoords += f'{coord}, '
        
        # Must end on same coord as begin
        outputCoords += f'{coordList[0]}'

        outputWKT = f'LINESTRING({outputCoords})'
        outputGEOM = f"ST_Polygon('{outputWKT}'::geometry, 4326)"
        
        return outputWKT        


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
    """ Commented out to skip FCC calculations for testing
    with open(fmQueryPath, 'r') as file:
        print("Loading stations data...")

        # Load values as list of tuples
        values = []
        for i, line in enumerate(file.readlines()):
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
                # print(f'    Error on {row}')
                continue
            

        # Insert values list to stations table
        sql = "insert into stations values %s"
        psycopg2.extras.execute_values(cur, sql, values)
        print("Done\n")
    """

    # Load service contours
    with open(serviceContoursPath, 'r') as file:
        print("Loading service contours...")
        # Load values as list of tuples
        values = []
        for i, line in enumerate(file.readlines()[1:]):
            try:
                row = line.split("|")
                data = {
                    "ID": row[0].strip(),
                    "service": row[1].strip(),
                    "coords": row[5:-1]
                }
                record = ServiceContour(data)
                values.append(record.as_tuple())

                
            except:
                print(f'Error on {row}.')

        # Insert values list to stations table
        sql = "insert into servicecontours (applicationid, service, wtk) values %s"
        psycopg2.extras.execute_values(cur, sql, values)
        cur.execute('update servicecontours set geom = ST_Transform(ST_Polygon(wtk::geometry, 4326),5069);')
        print("Done\n")



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