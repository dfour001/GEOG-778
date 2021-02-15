#-------------------------------------------------------------------------------
# Name:        GetData
# Purpose:     Downloads the required data and saves it to the data folder
#
# Author:      Daniel Fourquet
# Created:     Feb 2021
#-------------------------------------------------------------------------------

import os
import shutil
import urllib.request as request
from contextlib import closing
from zipfile import ZipFile


def create_data_folder(dataPath):
    """ Create data folder if it does not exist """
    print("Creating data folder")
    os.makedirs(dataPath, exist_ok=True)
    print("Done\n")


def dl_fcc_data(dataPath):
    """ Downloads service contour data from FCC """
    print("Downloading FCC Data")
    dataURL = "ftp://ftp.fcc.gov/pub/Bureaus/MB/Databases/fm_service_contour_data/FM_service_contour_current.zip"
    filePath = f"{dataPath}\\FM_service_contour_current.zip"

    with closing(request.urlopen(dataURL)) as r:
        with open(filePath, 'wb') as f:
            shutil.copyfileobj(r, f)

    print("Unzipping Data")
    # zFile = ZipFile(f'{dataPath}\FM_service_contour_current.zip')
    # filePath = r'C:\Users\danie\Desktop\GEOG 778\GEOG-778\tasks\data\FC_service_contour_current.zip'
    with ZipFile(filePath, 'r') as zFile:
        zFile.extractall(dataPath)
    
    print("Done\n")


def dl_format(dataPath):
    """ Downloads programming format data from Wikipedia """
    print("Downloading format data")
    pass


def download_data():
    """ Downloads radio station data from FCC and scrapes programming format
        data from Wikipedia and saves the data in the data folder """
    
    # Path to folder where data will be stored
    dataPath = os.path.dirname(os.path.abspath(__file__)) + '\data'

    # Create data folder if it does not exist
    create_data_folder(dataPath)

    # Download data
    dl_fcc_data(dataPath)
    dl_format(dataPath)


if __name__ == "__main__":
    download_data()

