# app/robo_advisor.py

import requests
import csv
import os
import json
import datetime
from dotenv import load_dotenv
import matplotlib.pyplot as plt

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

#Evaluating whether or not to buy a stock
def buy_recommendation(low, high, current):
    average = (low + high) / 2
    threshold = average * 1.2
    if (float(current) < threshold):
        return True
    else:
        return False

recommendation = buy_recommendation(recent_low, recent_high, latest_close)

def rec(recommendation):
    if recommendation:
        return "Buy, buy, buy"
    else:
        return "Not a good time to buy"

def explanation(low, high, current, recommendation):
    average = (low + high) / 2
    threshold = average * 1.2
    if (recommendation):
        return ("Based off the most recent price of " +to_usd(float(latest_close)) + " and the moving average of " +to_usd(average)
        + " it would be advisable to buy " + symbol + " as it's below a 20 percent increased threshold of the moving average.")
    else:
        return ("Based off the most recent price of " +to_usd(float(latest_close)) + " and the moving average of " +to_usd(average)
        + " it wouldn't be advisable to buy " + symbol + " as it's above a 20 percent increased threshold of the moving average.")

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
print("RECOMMENDATION: " +rec(recommendation))
print("RECOMMENDATION REASON: " +explanation(recent_low, recent_high, latest_close, recommendation))
print("-------------------------")
print("WRITING DATA TO CSV")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")

#Further Exploration: Create a Data Visualization
closing_prices = []

for date in dates:
    close_price = tsd[date]["4. close"]
    closing_prices.append(float(close_price))

#Adapted from https://medium.com/@pknerd/data-visualization-in-python-line-graph-in-matplotlib-9dfd0016d180
plt.plot(dates, closing_prices, color='orange')
plt.xlabel('Date')
plt.ylabel('Closing Price ($)')
plt.xticks(dates, rotation=90, fontsize=4)
plt.title('Closing prices of ' +symbol+ ' stock')
plt.show()