import requests

def fetch_from_cloudflare_worker(index_name="VNINDEX", worker_url=None):
    """
    Fetch stock data from Cloudflare Worker with Browser Rendering API
    
    Args:
        index_name: VNINDEX, VN30, or HNX
        worker_url: Your deployed worker URL (e.g., https://cafef-stock-scraper.your-subdomain.workers.dev)
        
    Returns:
        dict: Stock data with index, value, change, changePercent, and timestamp
    """
    if not worker_url:
        raise ValueError("worker_url must be provided")
    
    try:
        # Format the URL with the index parameter
        url = f"{worker_url}/?index={index_name}"
        
        # Send the request to the worker
        response = requests.get(url, timeout=15)  # Longer timeout since browser rendering takes time
        response.raise_for_status()  # Raise exception for error status codes
        
        # Parse and return the JSON response
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Cloudflare Worker: {e}")
        return None
