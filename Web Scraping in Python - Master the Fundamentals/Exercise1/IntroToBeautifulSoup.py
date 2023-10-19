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
print(trs[0].contents[1].text)
