import datetime

from helper import fetch_stock_data


def test_fetch_stock_data_success():
    symbol = "VNINDEX"
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.datetime.now() - datetime.timedelta(days=3)).strftime("%Y-%m-%d")
    data = fetch_stock_data(symbol, start_date, today)
    assert isinstance(data, list)
    assert len(data) > 0
    assert all("date" in d and "close" in d for d in data)


def test_fetch_stock_data_invalid_symbol():
    symbol = "INVALIDSYMBOL"
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.datetime.now() - datetime.timedelta(days=3)).strftime("%Y-%m-%d")
    data = fetch_stock_data(symbol, start_date, today)
    assert isinstance(data, list)
    assert len(data) == 0
