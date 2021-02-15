#-------------------------------------------------------------------------------
# Name:        GetData
# Purpose:     Downloads the required data and saves it to the data folder
#
# Author:      Daniel Fourquet
# Created:     Feb 2021
#-------------------------------------------------------------------------------

from bs4 import BeautifulSoup
import os
import shutil
import urllib.request as request
from contextlib import closing
from zipfile import ZipFile
import csv


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
    """ Downloads programming format data from Wikipedia.  These will be scraped
        from Wikipedia using BeautifulSoup.  Each format is loaded to a dictionary
        then copied to a csv file that will be loaded to the database. """

    def get_soup(url):
        """ Returns a BeautifulSoup object for the input url """
        page = request.urlopen(url)
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")

        return soup

    print("Downloading format data")
    formatList = [] # List of radio format dictionaries [{Callsign: str, Format: str}]

    # Load formatList with radio station formats for each url in wikiUrls.txt
    with open(os.path.dirname(os.path.abspath(__file__)) + '\wikiUrls.txt', 'r') as wikiUrls:
        for url in wikiUrls.readlines():
            print(f'Reading {url.strip()}')
            soup = get_soup(url)
            table = soup.table
            tableRows = table.find_all('tr')
            for tr in tableRows:
                td = tr.find_all('td')
                row = [d.text for d in td]
                
                if len(row) > 0:
                    stationDict = {}
                    stationDict['callsign'] = row[0]
                    stationDict['format'] = row[-1][:-1]
                    formatList.append(stationDict)
    
    # Save formatList as csv file in data folder
    outputCSV = f'{dataPath}\\formats.csv'
    with open(outputCSV, 'w', newline='') as csvFile:
        fieldnames = ['callsign', 'format']
        writer = csv.DictWriter(csvFile, fieldnames)
        writer.writeheader()
        writer.writerows(formatList)


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
    dataPath = os.path.dirname(os.path.abspath(__file__)) + '\data'
    dl_format(dataPath)

