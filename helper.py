import datetime

import requests


def fetch_stock_data(symbol, start_date, end_date):
    """Fetch stock data from VNDIRECT API"""
    url = "https://finfo-api.vndirect.com.vn/v4/stock_prices/"
    query = f"code:{symbol}~date:gte:{start_date}~date:lte:{end_date}"
    delta = datetime.datetime.strptime(end_date, "%Y-%m-%d") - datetime.datetime.strptime(
        start_date, "%Y-%m-%d"
    )
    params = {"sort": "date", "size": delta.days + 1, "page": 1, "q": query}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("data", [])
    else:
        print(f"API Error: {response.status_code} - {response.text}")
        return []
