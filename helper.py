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


def fetch_stock_data_safari_fallback(symbol, start_date, end_date):
    """
    Safari-based fallback for fetching stock data when API fails.
    This function imports and uses the Safari scraper as a fallback method.
    """
    try:
        from safari_scraper import fetch_stock_data_safari
        print(f"🌐 API failed, trying Safari scraper for {symbol}...")
        return fetch_stock_data_safari(symbol, start_date, end_date)
    except ImportError:
        print("❌ Safari scraper not available (py-applescript not installed)")
        return []
    except Exception as e:
        print(f"❌ Safari scraper error: {e}")
        return []


def fetch_stock_data_with_fallback(symbol, start_date, end_date):
    """
    Fetch stock data with Safari scraper as fallback when API fails.
    
    First tries the VNDIRECT API, then falls back to Safari scraping if API fails.
    """
    # Try API first
    data = fetch_stock_data(symbol, start_date, end_date)
    
    # If API failed or returned no data, try Safari scraper
    if not data:
        print(f"🔄 No data from API, trying Safari scraper...")
        data = fetch_stock_data_safari_fallback(symbol, start_date, end_date)
    
    return data
