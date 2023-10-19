import requests
from bs4 import BeautifulSoup

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

print(nameValues.get("WBD"))  # Grab specific stock ticker
# print(nameValues) # Print all vals
