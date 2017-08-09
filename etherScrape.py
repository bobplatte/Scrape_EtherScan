import requests
from bs4 import BeautifulSoup

base_url = "https://etherscan.io/blocks"

raw = requests.get(base_url)

data = raw.text

soup = BeautifulSoup(data, "lxml")

'''
# Get total number of pages to loop through

page_header = soup.find("span", style = "padding: 2px 4px 4px 3px; border: 1px solid #D4D4D4; line-height: 30px; background-color: #EAEAEA; margin-top:2px; height: 2px;")

total_pages = int(page_header.find_all("b")[1].string)

print(total_pages)

'''


'''
# Search for tag inside descriptions
# Saved for future reference

soup.find_all("a", title = True, class_="address-tag")
for i in r:
    print(i["title"])
'''

rows = soup.find("tbody").find_all("tr")

for row in rows:
    block = row.find_all("td")
    for i in range(len(block)):
        if i == 0:
            block_number = block[i].string
            print("Block: " + block_number)
        if i == 1:
            time = block[i].find("span", title = True)
            print(time["title"])
        if i == 2:
            txs = block[i].string
            print("Transactions included: " + txs)
        if i == 4:
            address = block[i].find("a").string
            print("Winning miner: " + address)
        if i == 7:
            hRate = block[i].string
            print("Network hasrate: " + hRate)
        if i == 8:
            reward_raw = block[i].contents
            reward = reward_raw[0] + "." + reward_raw[2]
            print("Mining reward: " + reward)
        else:
            pass
    print("\n\n")
