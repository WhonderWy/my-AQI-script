#!/usr/bin/env python3

# Original Author: William
# Date created: 2019/12/12
# Reason: The air quality settled down around my area and I wasn"t worrying about breathing for once so I considered writing a simple script.
# What this does:
# A simple script that outputs necessary data to terminal or elsewhere based on config.

from bs4 import BeautifulSoup

CONFIG = "config.json"
settings = {}

SCALE = {
    "VERY GOOD": 33,
    "GOOD": 66,
    "FAIR": 99,
    "POOR": 149,
    "VERY POOR": 199,
    "HAZARDOUS": 200,
    "scale": 33,
}

fields = {
    "Ozone O3 hourly": None,
    "Ozone O3 four hourly": None,
    "Nitrogen Dioxide NO2": None,
    "Visibility NEPH": None,
    "Carbon Monoxide CO2": None,
    "Sulfur Dioxide SO2": None,
    "Particles PM10": None,
    "Particles PM2.5": None,
    "Site AQI": None,
    "Regional AQI": None,
}

# class Settings():
# 	def __init__(self):
# 		pass


def read_config():
    import json

    global settings

    with open(CONFIG, "r+") as config:
        settings = json.load(config)


def print_config():
    for field in settings:
        print(field)


def get_html():
    import requests

    html_data = requests.get(str(settings["site"]))

    return html_data.text


def get_values():
    global fields

    soup = BeautifulSoup(markup=get_html(), features="lxml")
    table = soup.find_all("table", class_="aqi")[0]
    # site = table.find_all(id="site")
    targets = table.find_all("tr")

    for row in targets:
        # Incidentally, it"s #43
        # class_="Site"
        if row.text.find(settings["location"]):
            text = row.text.splitlines()
            for line, key in text, fields:
                if settings["location"] != line:
                    fields[key] = line
        # current = row.find_all("td", settings["location"])
        # if current:
        #     columns = row.find_all("td")
        #     for column, key in zip(columns, fields):
        #         fields[key] = column.get_text()


def print_data():
    scale = None
    for field in settings["interested_fields"]:
        value = get_values()
        for level in SCALE:
            if value < SCALE[level]:
                scale = level
                break
        string = f"{field:<20} is {scale:^10} at {value:>5}"
        print(string)


def send_notification():
    import platform

    osName = platform.system()
    if osName == "Linux":
        pass
    elif osName == "Windows":
        pass
    else:
        pass


if __name__ == "__main__":
    read_config()
    get_values()
    print_data()
