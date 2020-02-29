# app/robo_advisor.py

import requests
import csv
import os
import json
import datetime
from dotenv import load_dotenv

#Adapted from Shopping Cart project
def to_usd(my_price):
    return "${0:,.2f}".format(my_price)

load_dotenv()

#Adapted from https://stackoverflow.com/questions/19859282/check-if-a-string-contains-a-number
#Created a preliminary check
def testTicker(inputString):
    return any(char.isdigit() for char in inputString) or len(inputString) >=5

#Improved basic while sourced from https://github.com/ashishpatel310/Robo-Advisor-Project/blob/master/app/robo_advisor.py
while True:
    symbol = input('Please enter a valid stock ticker (ex. MSFT): ')
    if testTicker(symbol):
        print("Sorry this doesn't seem to be a valid ticker")
        continue
    else:    
        try:
            api_key = os.environ.get("ALPHAVANTAGE_API_KEY")
            request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"
            response = requests.get(request_url)
            #parse into dictionary object
            parsed_respose = json.loads(response.text)
            last_refreshed = parsed_respose["Meta Data"]["3. Last Refreshed"]
        except KeyError:
            print("Sorry, that is not a valid ticker. Please try again!")
            continue
        else:
            break

tsd = parsed_respose["Time Series (Daily)"]
dates = list(tsd.keys())

latest_day = dates[0]

latest_close = tsd[latest_day]["4. close"]

high_prices = []
low_prices = []

for date in dates:
    high_price = tsd[date]["2. high"]
    high_prices.append(float(high_price))
    low_price = tsd[date]["3. low"]
    low_prices.append(float(low_price))

recent_high = max(high_prices)
recent_low = min(low_prices)

csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")
csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]

with open(csv_file_path, "w") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
    writer.writeheader()
    for date in dates:
        daily_prices = tsd[date]
        writer.writerow({
            "timestamp": date,
            "open": daily_prices["1. open"],
            "high": daily_prices["2. high"],
            "low": daily_prices["3. low"],
            "close": daily_prices["4. close"],
            "volume": daily_prices["5. volume"]
        })

# Source Code: https://stackoverflow.com/questions/1759455/how-can-i-account-for-period-am-pm-using-strftime
now = datetime.datetime.now()
time = now.strftime("%I:%M %p")
day = datetime.date.today()

print("-------------------------")
print(f"SELECTED SYMBOL: {symbol.upper()}")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print(f"REQUEST AT: {day} {time}")
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print(f"RECENT LOW: {to_usd(float(recent_low))}")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("WRITING DATA TO CSV")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")

