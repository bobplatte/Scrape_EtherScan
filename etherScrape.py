import requests
from bs4 import BeautifulSoup
import csv

base_url = "https://etherscan.io/blocks"

raw = requests.get(base_url)

data = raw.text

soup = BeautifulSoup(data, "lxml")

# Get total number of pages to loop through
page_header = soup.find("span", style = "padding: 2px 4px 4px 3px; border: 1px solid #D4D4D4; line-height: 30px; background-color: #EAEAEA; margin-top:2px; height: 2px;")

total_pages = int(page_header.find_all("b")[1].string)

print("There are " + str(total_pages) + " total pages\n\n")


'''
# Search for tag inside descriptions
# Saved for future reference

soup.find_all("a", title = True, class_="address-tag")
for i in r:
    print(i["title"])
'''

with open("etherData.csv", 'a') as f:
    writer = csv.writer(f, quoting = csv.QUOTE_NONNUMERIC)
    writer.writerow(["Block", "Date", "Transactions", "Miner",
                    "Difficulty", "Hashrate", "Reward"])

    for x in range(3):

        print("************ Page " + str(x + 1) + " ************")

        raw = requests.get(base_url + "?p=" + str(x))

        data = raw.text

        soup = BeautifulSoup(data, "lxml")

        rows = soup.find("tbody").find_all("tr")

        for row in rows:
            block = row.find_all("td")
            eth_data = []
            for i in range(len(block)):

                if i == 0:
                    block_number = block[i].string
                    eth_data.append(block_number)
                if i == 1:
                    time = block[i].find("span", title = True)
                    eth_data.append(time["title"])
                if i == 2:
                    txs = block[i].string
                    eth_data.append(txs)
                if i == 4:
                    address = block[i].find("a").string
                    eth_data.append(address)
                if i == 6:
                    difficulty = block[i].string
                    eth_data.append(difficulty)
                if i == 7:
                    hRate = block[i].string
                    eth_data.append(hRate)
                if i == 8:
                    reward_raw = block[i].contents
                    reward = reward_raw[0] + "." + reward_raw[2]
                    eth_data.append(reward)
                else:
                    pass
            writer.writerow(eth_data)
