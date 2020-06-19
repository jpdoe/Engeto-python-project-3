#!/usr/bin/env python3

# Description: Project 3 - Elections Scraper for Engeto Online Python Academy
# Author: Jan Polák

import requests
import csv_writter
from bs4 import BeautifulSoup

BASE_URL = "https://volby.cz/pls/ps2017nss/"

URL = "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2102"


class Municipality():
    def __init__(self):
        self.code = 0
        self.name = ""
        self.registered = 0
        self.envelopes = 0
        self.valid_votes = 0
        self.parties = {}

    def __repr__(self):
        return f"Code {self.code}\n" \
               f"Name {self.name}\n" \
               f"Registered {repr(self.registered)}\n" \
               f"Envelopes {self.envelopes}\n" \
               f"Votes {self.valid_votes}\n" \
               f"Parties {self.parties}\n"

    def csv_output(self):
        return {"code": self.code, "name": self.name, "registered": self.registered, "envelopes": self.envelopes,
                "valid": self.valid_votes, "parties": self.parties}


municip_list = []


# extract table from page

# table = soup.find("div", {"id": "content"})

# for cil in table:
#     print(cil)

def get_soup(URL):
    page = requests.get(URL)

    return BeautifulSoup(page.text, 'html.parser')


def norm_int(string):
    # replace unicode non-breakable space
    return int(string.replace(u'\xa0', u''))


def get_info(URL, muni):
    soup = get_soup(URL)
    parties_dic = {}
    muni["registered"] = norm_int(soup.find("td", {"headers": "sa2"}).text)
    muni["envelopes"] = norm_int(soup.find("td", {"headers": "sa3"}).text)
    muni["valid"] = norm_int(soup.find("td", {"headers": "sa6"}).text)

    # parties table
    tables = soup.find_all("table", {"class": "table"})[1:]
    # print(tables)

    for table in tables:
        parties = table.find_all("tr")[2:]

        for party in parties:
            p_name = party.td.findNext('td').text

            p_votes = norm_int(party.td.findNext('td').findNext('td').text)
            print(p_name, repr(p_votes))

            muni[p_name] = p_votes

    # return parties_dic


def get_table(URL):
    soup = get_soup(URL)


    tables = soup.find_all("table", {"class": "table"})

    for table in tables:

        # extract table rows and remove header
        municipalities = table.find_all("tr")[2:]

        for muni in municipalities:

            # skip empty (hidden) rows
            if muni.find("td", {"class": "hidden_td"}):
                print("HIDDEN")
                continue

            mun_tmp = {"code": "", "name": "", "registered": 0, "envelopes": 0,
                "valid": 0}

            try:
                print(muni.find('a')["href"])

            except TypeError:
                print(f"MUNI {muni}")

            municip_url = BASE_URL + muni.find('a')["href"]

            mun_tmp["code"] = muni.find('a').text
            # get name
            mun_tmp["name"] = muni.a.findNext('td').text

            get_info(municip_url, mun_tmp)

            municip_list.append(mun_tmp)

    return municip_list


zzz = get_table("https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=8&xnumnuts=5201")
# zzz = get_table("https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=14&xnumnuts=8102")
#
# for item in zzz:
#     print(item.keys())
print(zzz)

csv_writter.write_csv("bla.csv", zzz)