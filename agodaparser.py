#!/usr/bin/env python3
# pylint: disable=C0103, C0325, C0301

"""
Zipped Agoda Hotel Data File Parser
-----------------------------------

This utility unzips and parses the Agoda hotel data file, in-memory,
and makes the data available
"""

import csv
import zipfile
import io
import sys

class AgodaParser(object):
    """Class to manage parsing and searching of parsed data"""

    def __init__(self, zipdatafile):
        """Read and parse Agoda hotel data from a zip file"""
        if not zipfile.is_zipfile(zipdatafile):
            print("ERROR: '{0}' is not a valid zip file".format(zipdatafile))
            sys.exit(1)

        zipfh = zipfile.ZipFile(zipdatafile, mode='r')

        datafile = zipfh.infolist()[0]
        with zipfh.open(datafile, mode='rU') as datafh:
            datafh.read(3) # strips the BOM

            csvReader = csv.DictReader(io.TextIOWrapper(datafh), delimiter=',', quotechar='"')
            self.result = []

            for row in csvReader:
                if not float == type(row['rates_from']):
                    try:
                        rates_from = float(row['rates_from'])
                    except ValueError:
                        #print("ERROR: Unable to convert '{0}' to float for '{1}'".format(row['rates_from'], row['hotel_name']))
                        #print("DEBUG: '{0}'".format(row))
                        rates_from = 'Rates Not Available'
                else:
                    rates_from = row['rates_from']
                row['rates_from'] = rates_from
                self.result.append(row)

        zipfh.close()

    def get_all(self):
        """Return the full list of hotels as a list of dictionaries"""
        return self.result

    def find(self, hotel_id=None):
        """Locate a specific hotel by id"""
        if None == hotel_id:
            raise ValueError("Missing a hotel id")
        hotel_id = str(hotel_id)
        return next((item for item in self.result if item["hotel_id"] == hotel_id), None)

    def find_url(self, url=None):
        """Locate a specific hotel by url snippet"""
        if None == url:
            raise ValueError("Missing a hotel url")
        return next((item for item in self.result if item["url"] in url), None)

if __name__ == "__main__":
    import argparse
    argparser = argparse.ArgumentParser(description='Parse zipped Agoda hotel data file')
    argparser.add_argument("zipped_datafile", help="Agoda hotel datafile, in .zip format")
    args = argparser.parse_args()
    zipdatafile = args.zipped_datafile
    parsed = AgodaParser(zipdatafile)
    for entryrow in parsed.get_all():
        if 'Rates Not Available' == entryrow['rates_from']:
            print("{0} - '{1}': No rates available".format(entryrow['hotel_id'], entryrow['hotel_name']))
        else:
            print("{0} - '{1}' from '{2}' '{3}'".format(entryrow['hotel_id'], entryrow['hotel_name'], entryrow['rates_currency'], entryrow['rates_from']))

