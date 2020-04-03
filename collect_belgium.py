# coding: utf-8

import locale
from pathlib import Path
import urllib.request
from datetime import datetime

if __name__ == '__main__':
    # use system decimal_point
    locale.setlocale(locale.LC_ALL, "")
    decimal_char = locale.localeconv()["decimal_point"]
    sep_char = ","

    url_list = [
        {"url": "https://epistat.sciensano.be/data/covid19be_cases_agesex.csv", "name": "covid19be_cases_agesex"},
        {"url": "https://epistat.sciensano.be/data/covid19be_cases_muni.csv", "name": "covid19be_cases_muni"},
        {"url": "https://epistat.sciensano.be/data/covid19be_cases_muni_cum.csv", "name": "covid19be_cases_muni_cum"},
        {"url": "https://epistat.sciensano.be/data/covid19be_hosp.csv", "name": "covid19be_hosp"},
        {"url": "https://epistat.sciensano.be/data/covid19be_mort.csv", "name": "covid19be_mort"},
        {"url": "https://epistat.sciensano.be/data/covid19be_tests.csv", "name": "covid19be_tests"}
    ]

    # purpose: download siensano data every day
    dt_string = datetime.now().strftime("%d-%m-%Y")
    dest_path = Path("data/be")
    dest_path.mkdir(parents=True, exist_ok=True)

    for item in url_list:
        print("processing", item["name"])
        response = urllib.request.urlopen(item["url"])
        data = response.read()  # a `bytes` object
        text = data.decode('iso-8859-1')
        with open(dest_path.joinpath("%s_%s.csv" % (item["name"], dt_string)), 'w', newline="\n",
                  encoding="utf8") as csv_file:
            csv_file.write(text)
        # with open(dest_path.joinpath("covid19be_cases_agesex_%s.csv" % dt_string), 'wb') as csv_file:
        #     csv_file.write(text.encode('utf-8'))
