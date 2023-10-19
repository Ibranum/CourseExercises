from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

url = "https://finance.yahoo.com/crypto/"

options = Options()
options.add_argument("--headless=new")
# service = webdriver.ChromeService(
# executable_path='chrome.app')
driver = webdriver.Chrome(
    options=options)

yahooCrypto = driver.get(url)
# driver.implicitly_wait(10)
pageSource = driver.page_source
# print(pageSource)

# value = "Bitcoin USD"
# if value in pageSource:
# print("Yes")
# else:
# print("No")

# Get table
xPathName = '/html/body/div[1]/div/div/div[1]/div/div[2]/div/div/div[6]/div/div/section/div/div[2]/div[1]/table/tbody'
colName = (driver.find_elements(By.TAG_NAME, "td"))
# print(colName[1].text)

# Parse data, get rid of whitespace.
newData = []
for i in range(len(colName)):
    if colName[i].text == (" "):
        pass
    elif colName[i].text == (""):
        pass
    else:
        newData.append(colName[i].text)  # Use text

# print(newData)

# Format data into associated table rows. List within list.
cryptoPrices = []
for i in range(0, len(newData), 10):
    cryptoPrices.append(newData[i:i+10])
    # print("loop")

print(cryptoPrices)


driver.quit()  # Close application
