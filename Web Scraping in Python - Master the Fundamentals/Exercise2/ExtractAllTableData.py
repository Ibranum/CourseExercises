import requests
from bs4 import BeautifulSoup

url = "https://finance.yahoo.com/quote/AAPL?p=AAPL"  # Target URL
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

print(nameValues)
