###################################
# Import dependencies
###################################
import requests
from bs4 import BeautifulSoup
import csv

###################################
# Define constants
###################################

base_url = "https://etherscan.io/blocks"

# Find total number of pages to scrape
raw = requests.get(base_url)
data = raw.text
soup = BeautifulSoup(data, "lxml")

# Find last page number using unique style code
page_header = soup.find("span", style = "padding: 2px 4px 4px 3px; border: 1px solid #D4D4D4; line-height: 30px; background-color: #EAEAEA; margin-top:2px; height: 2px;")
total_pages = int(page_header.find_all("b")[1].string)

# Desplay to console the total pages
print("There are " + str(total_pages) + " total pages\n\n")

###################################
# Scrape and write to csv file
###################################
with open("etherData.csv", 'a') as f:
    writer = csv.writer(f, quoting = csv.QUOTE_NONNUMERIC)
    writer.writerow(["Block", "Date", "Transactions", "Miner",
                    "Difficulty", "Hashrate", "Reward"])

    # Sample range for testing.
    # To scrape all data loop through range(total_pages)
    for x in range(20):

        # Print to console so you don't lose your mind
        if (x+1)%10 == 0:
            print("Scraping from page " + str(x + 1))

        # Get raw data from each new webpage
        raw = requests.get(base_url + "?p=" + str(x))
        data = raw.text
        soup = BeautifulSoup(data, "lxml")

        # Get table data
        table = soup.find("tbody").find_all("tr")

        # Loop by row
        for row in table:

            # Number of data points per block
            block = row.find_all("td")

            # Empty list to fill and write to csv
            eth_data = []

            # Scrape the data we want.
            # Note len(block) = 9 (Height, Age, ... , Reward)
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
                    if len(reward_raw) == 1:
                        reward = reward_raw[0]
                    else:
                        reward = reward_raw[0] + "." + reward_raw[2]
                    eth_data.append(reward)
                else:
                    pass

            # Write to csv
            writer.writerow(eth_data)
