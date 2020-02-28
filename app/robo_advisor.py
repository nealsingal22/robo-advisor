# app/robo_advisor.py

import requests
import json

#Adapted from Shopping Cart project
def to_usd(my_price):
    return "${0:,.2f}".format(my_price)

request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&apikey=demo"
response = requests.get(request_url)
print(response.status_code)
print(response.request)
print(response.text)

#parse into dictionary object
parsed_respose = json.loads(response.text)

last_refreshed = parsed_respose["Meta Data"]["3. Last Refreshed"]

tsd = parsed_respose["Time Series (Daily)"]
dates = list(tsd.keys())

latest_day = dates[0]

latest_close = tsd[latest_day]["4. close"]

print("-------------------------")
print("SELECTED SYMBOL: XYZ")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: 2018-02-20 02:00pm")
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
print("RECENT HIGH: $101,000.00")
print("RECENT LOW: $99,000.00")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")