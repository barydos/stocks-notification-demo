import requests
import datetime as dt
import os

from dotenv import load_dotenv
load_dotenv()

ALPHA_API_KEY = os.getenv('ALPHA_API_KEY')
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"


def main():
    if abs(latest_change(STOCK)) >= 5:
        get_news(COMPANY_NAME)


def latest_change(stock):
    stock_url = "https://www.alphavantage.co/query"
    stock_params = {
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol": stock,
        "outputsize": "compact",
        "apikey": ALPHA_API_KEY
    }

    response = requests.get(stock_url, stock_params).json()
    results = response['Time Series (Daily)']

    last_date = list(results.keys())[0]
    last_date_parsed = [int(val) for val in last_date.split("-")]
    previous_date = str(dt.date(*last_date_parsed) - dt.timedelta(days=1))

    last_adjusted_close = float(results[last_date]['5. adjusted close'])
    previous_adjusted_close = float(results[previous_date]['5. adjusted close'])

    delta_pct = (1 - last_adjusted_close / previous_adjusted_close) * 100

    return delta_pct


def get_news(company: str):
    print(company)


def send_sms():
    pass


if __name__ == '__main__':
    main()


# - + - + DONE + - + -
# STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number.


#Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
