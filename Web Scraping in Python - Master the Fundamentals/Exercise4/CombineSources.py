import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
import datetime
import os.path


# Modified the program requirements so that I'm not spamming Yahoo w/ requests.
# Will only lookup 1 ticker at a time. Two requests total.


def YahooExtract(ticker):
    # print("func YahooExtract")

    url = "https://finance.yahoo.com/quote/" + ticker + "?p=" + ticker  # Target URL
    prop = "Previous Close"

    r = requests.get(url)  # The request itself
    t = r.text  # HTML text

    # Provide HTML to BS, choose to parse with HTML
    soup = BeautifulSoup(t, features="html.parser")

    trs = soup.find_all("tr")  # find all in <tr> tags
    # print(trs[0].find("td", attrs={"data-test": "PREV_CLOSE-value"}))
    # print(trs[0].contents[1].text)

    nameValues = {}

    class Found(Exception):  # to exit double-nested for loop below
        pass

    try:
        for x in range(len(trs)):
            for i in range(len(trs[x].contents)):
                if trs[x].contents[i].text == "Symbol":
                    raise Found
                # print(trs[x].contents[i].text)
                name = trs[x].contents[0].text
                value = trs[x].contents[1].text
                nameValues[name] = value

    except Found:
        pass
    except:
        print("Error - failed to pull information for stock.")

    # print(nameValues)
    return nameValues


def WikiExtract(ticker):
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"  # Target URL
    prop = "Previous Close"

    r = requests.get(url)  # The request itself
    t = r.text  # HTML text

    # Provide HTML to BS, choose to parse with HTML
    soup = BeautifulSoup(t, features="html.parser")

    # find all in <tr> tags
    table = soup.find(lambda tag: tag.name == 'table' and tag.has_attr(
        'id') and tag['id'] == "constituents")  # find table with specific ID

    table = table.find_all("tr")
    # start table index 1, contents index 1. Contents needs to skip an int w/ each iteration, 1 -> 3, 3 -> 5.
    # print(table[1].contents[3].text)

    nameValues = {}

    try:
        for x in range(1, len(table)):
            for i in range(1, len(table[x].contents)):
                symbol = table[x].contents[1].text.rstrip("\n")
                security = table[x].contents[3].text.rstrip("\n")
                sector = table[x].contents[5].text.rstrip("\n")
                subIndustry = table[x].contents[7].text.rstrip("\n")
                hqLoc = table[x].contents[9].text.rstrip("\n")
                added = table[x].contents[11].text.rstrip("\n")
                cik = table[x].contents[13].text.rstrip("\n")
                founded = table[x].contents[15].text.rstrip("\n")
                nameValues[symbol] = [symbol, security, sector,
                                      subIndustry, hqLoc, added, cik, founded]
    except:
        print("Error - failed to pull information for stock.")

    # print(nameValues.get("WBD"))  # Grab specific stock ticker
    # print(nameValues) # Print all vals
    histTicker = {}
    specificStock = nameValues.get(ticker)
    columnNames = ["Symbol", "Security", "GICS Sector", "GICS Sub-Industry",
                   "Headquarters Location", "Date Added", "CIK", "Founded"]

    for i in range(len(specificStock)):
        histTicker[columnNames[i]] = specificStock[i]

    return histTicker


def tickerUpdate(ticker):

    wikiData = WikiExtract(ticker)
    # wikiData = wikiData.get(ticker)
    # print(wikiData)

    yahooData = YahooExtract(ticker)
    # print(yahooData)

    now = str(datetime.datetime.now())
    temp = {}
    time = "Time"
    temp[time] = now

    data = wikiData | yahooData | temp  # Merge all together.
    print(data)

    df = pd.DataFrame([data])

    checkExist = os.path.isfile("test.csv")
    if checkExist:
        print("File already exists")
    else:
        df.to_csv("test.csv", sep='\t')
        print("Wrote to CSV")


def main():
    ticker = "WBD"  # Put whatever ticker you want the data on here.

    i = 0
    while i < 500:  # Maxes out eventually, just in case.
        tickerUpdate(ticker)
        sleep(900)  # Running every 15 minutes.
        i = i + 1


if __name__ == "__main__":
    main()
