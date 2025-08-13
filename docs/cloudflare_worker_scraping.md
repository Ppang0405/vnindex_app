# Using Cloudflare Workers for Web Scraping Vietnam Stock Market Data

## Introduction

This document outlines how to use Cloudflare Workers to scrape web data for Vietnam stock market indices (VNINDEX, VN30, HNX) when direct APIs are unavailable or unreliable. Cloudflare Workers provide a serverless platform that allows you to deploy JavaScript code at the edge, making it ideal for web scraping without requiring dedicated server infrastructure.

## Why Cloudflare Workers for Scraping?

1. **Edge Computing**: Fast response times as code runs close to users
2. **No Server Management**: Serverless architecture eliminates infrastructure concerns
3. **High Performance**: Designed to handle requests efficiently
4. **Caching Capabilities**: Can cache responses to reduce scraping frequency
5. **Circumvent Connection Issues**: Can bypass some network restrictions faced by client applications

## Implementation Approach

### 1. Setting Up a Cloudflare Worker

1. **Create a Cloudflare Account**: Sign up at [Cloudflare](https://dash.cloudflare.com/sign-up)
2. **Install Wrangler CLI**: 
   ```bash
   npm install -g wrangler
   ```
3. **Authenticate Wrangler**:
   ```bash
   wrangler login
   ```
4. **Create a new Worker project**:
   ```bash
   wrangler init vietnam-stock-scraper
   cd vietnam-stock-scraper
   ```

### 2. Writing the Scraper Worker

Create a worker script that uses HTMLRewriter to extract stock market data from websites like CafeF or SSI:

```javascript
// vietnam-stock-scraper/src/index.js

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const targetIndex = url.searchParams.get('index') || 'VNINDEX';
    
    // Map to source website URLs based on index name
    const sourceUrls = {
      'VNINDEX': 'https://cafef.vn/...',
      'VN30': 'https://cafef.vn/...',
      'HNX': 'https://cafef.vn/...'
    };
    
    const targetUrl = sourceUrls[targetIndex];
    if (!targetUrl) {
      return new Response('Invalid index parameter', { status: 400 });
    }
    
    // Fetch the webpage content
    const response = await fetch(targetUrl, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
      }
    });
    
    if (!response.ok) {
      return new Response(`Failed to fetch data: ${response.statusText}`, { status: response.status });
    }
    
    // Create object to store extracted data
    const stockData = {
      index: targetIndex,
      value: null,
      change: null,
      changePercent: null,
      timestamp: new Date().toISOString()
    };
    
    // Process the HTML response using HTMLRewriter
    const rewriter = new HTMLRewriter()
      // Target HTML elements that contain the stock index data
      .on('div.stock-price', (element) => {
        element.onText((text) => {
          stockData.value = parseFloat(text.text.trim().replace(',', ''));
        });
      })
      .on('div.stock-change', (element) => {
        element.onText((text) => {
          stockData.change = parseFloat(text.text.trim().replace(',', ''));
        });
      })
      .on('div.stock-change-percent', (element) => {
        element.onText((text) => {
          stockData.changePercent = parseFloat(text.text.trim().replace('%', '').replace(',', ''));
        });
      });
    
    // Transform the response through the rewriter
    await rewriter.transform(response).text();
    
    // Return the collected data as JSON
    return new Response(JSON.stringify(stockData), {
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Cache-Control': 'max-age=300' // Cache for 5 minutes
      }
    });
  }
};
```

### 3. Deploying the Worker

Deploy your worker to Cloudflare's network:

```bash
wrangler publish
```

After deployment, your scraper will be available at a URL like `https://vietnam-stock-scraper.your-subdomain.workers.dev`.

### 4. Using the Worker in the VNIndex App

Update the main application to use the Cloudflare Worker instead of direct API calls:

```python
def fetch_index(self):
    try:
        # Use Cloudflare Worker endpoint
        worker_url = f"https://vietnam-stock-scraper.your-subdomain.workers.dev/?index={self.current_index}"
        
        response = requests.get(worker_url)
        
        if response.status_code == 200:
            data = response.json()
            
            # Extract the values from the Worker response
            latest_value = data['value']
            change = data['change']
            change_pct = data['changePercent']
            
            # Format the display with an up or down indicator
            if change >= 0:
                self.title = f"{self.current_index}: {latest_value:.2f} 🔺{abs(change_pct):.2f}%"
            else:
                self.title = f"{self.current_index}: {latest_value:.2f} 🔻{abs(change_pct):.2f}%"
                
        else:
            raise Exception(f"Worker returned status code: {response.status_code}")
            
    except Exception as e:
        self.title = f"{self.current_index}: Error"
        print(f"Error fetching data: {e}")
```

## Advanced Techniques

### 1. Metadata Scraping with cloudflare-worker-scraper

The [cloudflare-worker-scraper](https://github.com/mrmartineau/cloudflare-worker-scraper) project provides a more sophisticated approach to scraping metadata from websites. This can be adapted for stock market data by:

1. **Modifying Scraper Rules**: Edit the rules in `src/scraper-rules.ts` to target stock price data
2. **Adding Index-Specific Selectors**: Configure selectors based on website structure
3. **Handling AJAX-loaded Content**: Implement strategies for data that loads asynchronously

### 2. Bypassing Anti-Scraping Measures

1. **Rotate User Agents**: Randomize the User-Agent header to avoid detection
2. **Implement Request Delays**: Add random delays between requests
3. **Use Browser-like Headers**: Send headers that mimic real browsers

### 3. Caching Strategy

Implement caching to:
1. Reduce load on target websites
2. Improve response time
3. Continue providing data during source website outages

```javascript
// Example caching implementation
const CACHE_KEY = `vietnam-stock-${targetIndex}`;
const CACHE_TTL = 300; // 5 minutes

// Try to get from cache first
const cachedResponse = await caches.default.match(CACHE_KEY);
if (cachedResponse) {
  return cachedResponse;
}

// If not in cache, fetch and then cache
const response = await fetch(targetUrl, {...});
const result = processResponse(response);

// Store in cache
await caches.default.put(
  CACHE_KEY, 
  new Response(JSON.stringify(result), {
    headers: {
      'Content-Type': 'application/json',
      'Cache-Control': `max-age=${CACHE_TTL}`
    }
  })
);
```

## Legal and Ethical Considerations

When scraping websites, be aware of:
1. **Terms of Service**: Always check if scraping is allowed
2. **Rate Limiting**: Implement reasonable request frequency
3. **Attribution**: Properly attribute the source of data
4. **Commercial Use**: Be cautious about commercial applications of scraped data

## Conclusion

Cloudflare Workers provide a powerful, serverless platform for scraping stock market data when direct APIs are unavailable. By implementing proper scraping techniques and adhering to ethical standards, you can create a reliable source of Vietnam stock market index data for your applications.

## References

- [Cloudflare Workers Web Scraper](https://workers.cloudflare.com/built-with/projects/web-scraper/)
- [Page Metadata Scraper with Cloudflare Workers](https://github.com/mrmartineau/cloudflare-worker-scraper)
- [Cloudflare Workers Documentation](https://developers.cloudflare.com/workers/)
