#!/usr/bin/env python3

# Description: Project 3 - Elections Scraper for Engeto Online Python Academy
# Author: Jan Polák

import requests
from bs4 import BeautifulSoup
import pprint
BASE_URL = "https://volby.cz/pls/ps2017nss/"

URL = "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2102"
# print(soup.text)
# table = soup.find_all("div", )
# print(soup.div.div.div.contents)

class Municipality():
    def __init__(self):
        self.code = 0
        self.name = ""
        self.registered = 0
        self.envelopes = 0
        self.valid_votes = 0
        self.parties = {}

    def __repr__(self):
        return f"Code {self.code} - Name {self.name} - Registered {self.registered}"


municip_list = []

# extract table from page

# table = soup.find("div", {"id": "content"})

# for cil in table:
#     print(cil)

def get_soup(URL):
    page = requests.get(URL)

    return BeautifulSoup(page.text, 'html.parser')

def get_info(URL):

    soup = get_soup(URL)

    voters = soup.find("td", {"headers": "sa2"}).text
    envelopes = soup.find("td", {"headers": "sa3"}).text
    valid_votes = soup.find("td", {"headers": "sa6"}).text
    # print(soup.find("td", {"headers": "sa1 sb1"}).text)

    # print(f"Voliči {voters}")

    # parties table
    tables = soup.find_all("table", {"class": "table"})[1:]
    # print(tables)

    for table in tables:
        parties = table.find_all("tr")[2:]

        for party in parties:
            # skip empty (hidden) rows
            # if party.find("td", {"class": "hidden_td"}):
            #     print("HIDDEN")
            #     print(party)
            #     continue
            p_name = party.td.findNext('td').text
            p_votes = party.td.findNext('td').findNext('td').text
            print(p_name, p_votes)



get_info("https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=2&xobec=534421&xvyber=2102")




def get_table(URL):

    soup = get_soup(URL)

    # div = soup.find_all('table', attrs={'class':'table'})

    tables = soup.find_all("table", {"class": "table"})

    for table in tables:

        print(10*"-")

        # extract table rows and remove header
        municipalities = table.find_all("tr")[2:]

        for muni in municipalities:

            # skip empty (hidden) rows
            if muni.find("td", {"class": "hidden_td"}):
                print("HIDDEN")
                continue

            mun_tmp = Municipality()
            # get URL
            # print(x[0].a["href"])
            # print(x[0].find('a')["href"])

            try:
                print(muni.find('a')["href"])

            except TypeError:
                print(f"MUNI {muni}")

            municip_url = BASE_URL + muni.find('a')["href"]

            mun_tmp.code = muni.find('a').text
            # get name
            # print(f"Sibling - obec {x[0].a.findNext('td').text}")
            # print(f"Selektor CSS - obec {x[0].select('td:nth-child(2)')[0].text}")
            mun_tmp.name = muni.a.findNext('td').text

            # DELETE
            # try:
            #     print(f'Alt {single_muni.find("td", {"headers": "t3sa1 t3sb2"}).text}')
            # except AttributeError:
            #     print("FUU")
            #     print(single_muni)


            print(mun_tmp.name)
            print(10 * "-")
            municip_list.append(mun_tmp)

    print(municip_list)


# get_table(URL)