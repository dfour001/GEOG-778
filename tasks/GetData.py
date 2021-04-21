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


def dl_fm_query(dataPath):
    """ Downloads radio station data from the FCC's FM Query tool """
    print("Downloading FM Query Data")

    fmQueryUrl = "https://transition.fcc.gov/fcc-bin/fmq?call=&fileno=&state=RI&city=&freq=0.0&fre2=107.9&serv=-1&status=3&facid=&asrn=&class=&list=4&NextTab=Results+to+Next+Page%2FTab&dist=&dlat2=&mlat2=&slat2=&NS=N&dlon2=&mlon2=&slon2=&EW=W&size=9"
    
    outputPath = f"{dataPath}\\fmQuery.txt"
    with open(outputPath, 'w') as file:
        file.write(request.urlopen(fmQueryUrl).read().decode())
    print("Done\n")


def dl_service_contours(dataPath):
    """ Downloads service contour data from FCC """
    print("Downloading Service Contour Data")

    dataURL = "ftp://ftp.fcc.gov/pub/Bureaus/MB/Databases/fm_service_contour_data/FM_service_contour_current.zip"
    filePath = f"{dataPath}\\FM_service_contour_current.zip"

    with closing(request.urlopen(dataURL)) as r:
        with open(filePath, 'wb') as f:
            shutil.copyfileobj(r, f)

    print("Unzipping Data")
    with ZipFile(filePath, 'r') as zFile:
        zFile.extractall(dataPath)
    
    print("Done\n")


def dl_format(dataPath):
    """ Downloads programming format data from Wikipedia.  These will be scraped
        from Wikipedia using BeautifulSoup.  Each format is loaded to a dictionary
        then copied to a csv file that will be loaded to the database. """
    print("Downloading format data")

    def get_soup(url):
        """ Returns a BeautifulSoup object for the input url """
        page = request.urlopen(url)
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")

        return soup

    
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
                    freq = row[1]
                    if 'AM' not in freq: # Filter out AM stations
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
    dl_fm_query(dataPath)
    dl_service_contours(dataPath)
    dl_format(dataPath)


if __name__ == "__main__":
    dataPath = os.path.dirname(os.path.abspath(__file__)) + '\data'
    download_data()
