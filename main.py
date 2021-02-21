import requests
import datetime as dt
import os
from twilio.rest import Client

from dotenv import load_dotenv
load_dotenv()

# Stock data
ALPHA_API_KEY = os.getenv('ALPHA_API_KEY')
STOCK_ENDPOINT = "https://www.alphavantage.co/query"

# News data
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

# SMS client & data
TWILIO_ACCOUNT_SID= os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUM = os.getenv('TWILIO_PHONE_NUM')
TO_NUM = os.getenv('PERSONAL_NUM')

# Stock to analyse
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

# Other
NUM_ARTICLES = 1


def main():
    change = latest_change(STOCK)

    if abs(change) >= 5 or True:
        articles = get_news(COMPANY_NAME, change, NUM_ARTICLES)
        send_sms(articles)
    else:
        print("Less than 5% change")


def latest_change(stock):
    stock_params = {
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol": stock,
        "outputsize": "compact",
        "apikey": ALPHA_API_KEY
    }

    response = requests.get(STOCK_ENDPOINT, stock_params).json()
    results = response['Time Series (Daily)']

    last_date = list(results.keys())[0]
    last_date_parsed = [int(val) for val in last_date.split("-")]
    previous_date = str(dt.date(*last_date_parsed) - dt.timedelta(days=1))

    last_adjusted_close = float(results[last_date]['5. adjusted close'])
    previous_adjusted_close = float(results[previous_date]['5. adjusted close'])

    delta_pct = (1 - last_adjusted_close / previous_adjusted_close) * 100

    return round(delta_pct, 2)


def get_news(company: str, change: float, num_articles: int):

    if change > 0:
        up_down = "🔺"
    else:
        up_down = "🔻"

    news_params = {
        "qInTitle": company
    }

    headers = {
        "X-Api-Key": NEWS_API_KEY
    }

    response = requests.get(url=NEWS_ENDPOINT, params=news_params, headers=headers).json()
    top_articles = [f"{STOCK}: {up_down} {change}%\nHeadline: {result['title']}\nBrief: {result['description']}" for result in response['articles'][:num_articles]]

    return top_articles


def send_sms(articles):

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    for article in articles:
        message = client.messages \
            .create(
            body=article,
            from_=TWILIO_PHONE_NUM,
            to=TO_NUM
        )

    print(f"Twilio SMS status: {message.status}")


if __name__ == '__main__':
    main()
