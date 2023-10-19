import requests

url = "https://finance.yahoo.com/quote/AAPL?p=AAPL"  # Target URL

prop = "Previous Close"

r = requests.get(url)  # The request itself

# print(r)
# print(r.status_code)

t = r.text
# The value being looked for follows this identifier
ind = t.index("Previous Close")

# redText = t[ind:ind+200]  # Reduced text of response to 200 characters
# print(redText)

targetVal = t[ind:].split("</span>")[1]
val = targetVal.split("PREV_CLOSE-value\">")[-1]
val = val.split("</td>")[0]
print(val)
