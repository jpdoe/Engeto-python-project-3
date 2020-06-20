#!/usr/bin/env python3

# Description: Project 3 - Elections Scraper for Engeto Online Python Academy
# Author: Jan Polák

import requests
import sys
from bs4 import BeautifulSoup

import csv_writter

BASE_URL = "https://volby.cz/pls/ps2017nss/"

# TODO add parameters check
URL = sys.argv[1]
CSV_FILE = sys.argv[2]


municip_list = []


def get_soup(url):
    try:
        page = requests.get(url)
        return BeautifulSoup(page.text, "html.parser")

    except requests.exceptions.ConnectionError as e:
        sys.exit(f"Problem with connection: {e}")


def norm_int(string):

    # replace unicode non-breakable space
    try:
        return int(string.replace("\xa0", ""))
    except ValueError as e:
        sys.exit(f"Problem with value: {e}")


def get_municip_info(url, muni):
    # prepare alphabet soup
    soup = get_soup(url)

    muni["registered"] = norm_int(soup.find("td", {"headers": "sa2"}).text)
    muni["envelopes"] = norm_int(soup.find("td", {"headers": "sa3"}).text)
    muni["valid"] = norm_int(soup.find("td", {"headers": "sa6"}).text)

    # parties table
    tables = soup.find_all("table", {"class": "table"})[1:]

    for table in tables:

        # extract table rows and remove header
        parties = table.find_all("tr")[2:]

        for party in parties:
            party_name = party.td.findNext("td").text

            # skip empty row
            if party_name == "-":
                continue
            # get number of votes for party
            muni[party_name] = norm_int(party.td.findNext("td").findNext("td").text)


def get_data(url):
    soup = get_soup(url)

    tables = soup.find_all("table", {"class": "table"})

    for table in tables:

        # extract table rows and remove header
        municip_rows = table.find_all("tr")[2:]

        for row in municip_rows:

            # skip empty rows
            if row.find("td").text == "-":
                continue

            mun_tmp = {
                "code": "",
                "name": "",
                "registered": 0,
                "envelopes": 0,
                "valid": 0,
            }

            municip_url = BASE_URL + row.find("a")["href"]

            # get code & name
            mun_tmp["code"] = row.find("a").text
            mun_tmp["name"] = row.a.findNext("td").text

            # get municipality info
            get_municip_info(municip_url, mun_tmp)

            municip_list.append(mun_tmp)

    return municip_list



if __name__ == '__main__':

    data = get_data(URL)

    print(data)

    csv_writter.write_csv(CSV_FILE, data)
