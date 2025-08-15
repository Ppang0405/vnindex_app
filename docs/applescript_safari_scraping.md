# AppleScript Safari Scraping for Vietnamese Stock Market Data

## Overview

This document outlines an innovative approach to scraping Vietnamese stock market data using AppleScript automation with Safari browser. This method leverages the `py-applescript` library to control Safari from Python, enabling sophisticated web scraping that can bypass many common anti-bot measures.

## Why AppleScript + Safari?

### Advantages

1. **Native Browser Automation**: Uses a real Safari browser instance, making it indistinguishable from human browsing
2. **JavaScript Execution**: Full access to Safari's JavaScript engine for dynamic content extraction
3. **Anti-Detection**: Harder to detect than headless browsers or HTTP clients
4. **macOS Integration**: Deep integration with macOS system, leveraging Apple's automation frameworks
5. **Dev Tools Access**: Can potentially use Safari's developer tools capabilities
6. **No External Dependencies**: Uses Safari that's already installed on macOS
7. **Persistent Sessions**: Can maintain session state across multiple requests

### Disadvantages

1. **macOS Only**: Limited to macOS systems due to AppleScript dependency
2. **GUI Required**: Requires a GUI environment (not suitable for headless servers)
3. **Slower**: Overhead of browser automation makes it slower than direct API calls
4. **Resource Intensive**: Browser instances consume more memory and CPU
5. **Stability**: Browser crashes or UI changes can break the automation

## Technical Architecture

### Components

```
Python Application
    ↓
py-applescript Library
    ↓
NSAppleScript (macOS)
    ↓
Safari AppleScript Interface
    ↓
Safari Browser
    ↓
JavaScript Execution
    ↓
VNDirect Website
```

### Key Libraries

- **py-applescript**: Python wrapper for NSAppleScript
- **applescript**: Alternative Python AppleScript library
- **PyObjC**: Python-Objective-C bridge (dependency)

## Implementation Details

### 1. Safari Control Script

The core of the implementation is an AppleScript that provides methods to:

```applescript
on openURLInSafari(targetURL)
    tell application "Safari"
        activate
        -- Navigate to URL and wait for load
    end tell
end openURLInSafari

on executeJavaScript(jsCode)
    tell application "Safari"
        set result to do JavaScript jsCode in current tab of front window
        return result
    end tell
end executeJavaScript
```

### 2. JavaScript Extraction Logic

The JavaScript code executed in Safari performs multiple extraction strategies:

#### Method 1: Table-based Extraction
```javascript
// Look for index data in HTML tables
const tables = document.querySelectorAll('table');
for (let table of tables) {
    // Search for rows containing index symbols
    // Extract value, change, and percentage data
}
```

#### Method 2: CSS Selector Extraction
```javascript
// Target specific elements by class names or data attributes
const indexCards = document.querySelectorAll('[data-symbol="VNINDEX"]');
// Extract structured data from card elements
```

#### Method 3: Text Pattern Matching
```javascript
// Search for text patterns containing index values
const allElements = document.querySelectorAll('*');
for (let element of allElements) {
    if (element.textContent.includes('VNINDEX')) {
        // Extract numbers using regex patterns
    }
}
```

### 3. Python Integration

```python
class SafariStockScraper:
    def __init__(self):
        self.safari_script = applescript.AppleScript(safari_control_script)
    
    def scrape_vndirect_index(self, index_symbol):
        # Open VNDirect website
        self.safari_script.call('openURLInSafari', vndirect_url)
        
        # Execute JavaScript extraction
        result = self.safari_script.call('executeJavaScript', js_code)
        
        # Parse and return structured data
        return json.loads(result)
```

## Data Flow

### 1. Request Initiation
```python
# Python application requests VNINDEX data
data = scraper.scrape_vndirect_index("VNINDEX")
```

### 2. Safari Automation
```
1. Python → AppleScript: "Open VNDirect URL"
2. AppleScript → Safari: Launch/activate Safari
3. Safari → VNDirect: HTTP request for webpage
4. VNDirect → Safari: HTML response
5. Safari: Render page and execute JavaScript
```

### 3. Data Extraction
```
1. Python → AppleScript: "Execute JavaScript extraction"
2. AppleScript → Safari: Run JavaScript in current tab
3. JavaScript: Parse DOM and extract index data
4. Safari → AppleScript: Return extracted data
5. AppleScript → Python: Return JSON string
```

### 4. Data Processing
```python
# Parse JSON response
data = json.loads(result)

# Structure for main application
return [{
    'date': data.get('timestamp', ''),
    'close': data.get('value', 0),
    'change': data.get('change', 0),
    'changePercent': data.get('changePercent', 0),
    'source': 'VNDirect (Safari)',
}]
```

## Target Website Analysis

### VNDirect Website Structure

**URL**: `https://www.vndirect.com.vn/portal/thong-ke-thi-truong-chung-khoan/chi-so-chung-khoan.shtml`

**Data Location Strategies**:

1. **HTML Tables**: Index data often appears in `<table>` elements
2. **Index Cards**: Modern UI uses card-based layouts with CSS classes
3. **JavaScript Variables**: Data might be embedded in page scripts
4. **API Endpoints**: Dynamic loading via AJAX calls

**Common Selectors**:
- `.index-card`, `.market-index` - Card containers
- `.value`, `.price`, `.index-value` - Price values
- `.change`, `.change-value` - Change amounts
- `.percent`, `.change-percent` - Percentage changes
- `[data-symbol="VNINDEX"]` - Data attributes

## Error Handling and Resilience

### 1. Multiple Extraction Methods
The scraper implements a fallback hierarchy:
1. Table-based extraction (most reliable)
2. CSS selector extraction (modern sites)
3. Text pattern matching (fallback)
4. HTML source parsing (last resort)

### 2. Wait Strategies
```applescript
-- Wait for page load
repeat 30 times
    delay 1
    if (do JavaScript "document.readyState" in current tab of front window) = "complete" then
        exit repeat
    end if
end repeat
```

### 3. Error Recovery
```python
try:
    data = json.loads(result)
    if 'error' in data:
        # Try alternative extraction method
        return self._try_alternative_extraction(index_symbol)
except json.JSONDecodeError:
    # Parse raw HTML if JSON parsing fails
    return self._extract_from_html(page_source, index_symbol)
```

## Integration with VNIndex App

### 1. Fallback Architecture
```python
def fetch_stock_data_with_fallback(symbol, start_date, end_date):
    # Try API first
    data = fetch_stock_data(symbol, start_date, end_date)
    
    # If API failed, try Safari scraper
    if not data:
        data = fetch_stock_data_safari_fallback(symbol, start_date, end_date)
    
    return data
```

### 2. User Interface Integration
The main app provides menu options:
- "Use Safari Scraper" - Force Safari scraping mode
- "Use API Only" - Use API with Safari fallback
- Visual indicators: 🌐 (Safari) vs 📡 (API)

### 3. Threading
```python
def update_index_value(self, _=None):
    thread = threading.Thread(target=self.fetch_index)
    thread.start()
```

## Performance Considerations

### 1. Speed Comparison
- **API Call**: ~200-500ms
- **Safari Scraping**: ~3-8 seconds (including browser startup)

### 2. Resource Usage
- **Memory**: +100-200MB for Safari process
- **CPU**: Higher during JavaScript execution
- **Network**: Same as API (single HTTP request)

### 3. Optimization Strategies
- Reuse existing Safari windows/tabs
- Implement intelligent caching
- Batch multiple symbol requests
- Minimize JavaScript execution time

## Security and Ethics

### 1. Rate Limiting
```python
import time

# Implement delays between requests
time.sleep(2)  # 2-second delay between scraping attempts
```

### 2. User-Agent Handling
Safari automatically provides legitimate user-agent strings, making requests appear as normal browsing.

### 3. Respectful Scraping
- Honor robots.txt guidelines
- Implement reasonable request frequencies
- Don't overwhelm target servers
- Provide attribution in user interface

### 4. Terms of Service
Always review target website's terms of service before implementing automated scraping.

## Installation and Setup

### 1. Prerequisites
```bash
# macOS with Safari installed
# Python 3.7+ with pip

# Required system frameworks (usually pre-installed)
# - Foundation.framework
# - CoreFoundation.framework
# - ApplicationServices.framework
```

### 2. Python Dependencies
```bash
# Install PyObjC (Python-Objective-C bridge)
pip install pyobjc

# Install AppleScript wrapper
pip install applescript
# OR alternative
pip install py-applescript

# Other dependencies
pip install pandas requests rumps
```

### 3. Permissions
macOS may require permissions for:
- Accessibility access for AppleScript
- Safari automation permissions
- Screen recording (if using advanced features)

## Usage Examples

### 1. Basic Usage
```python
from safari_scraper import SafariStockScraper

scraper = SafariStockScraper()
data = scraper.scrape_vndirect_index("VNINDEX")

if data:
    print(f"VNINDEX: {data['value']:.2f} ({data['changePercent']:.2f}%)")
```

### 2. Integration with Existing Code
```python
# Replace existing fetch function
from helper import fetch_stock_data_with_fallback

data = fetch_stock_data_with_fallback("VNINDEX", "2024-01-01", "2024-01-02")
```

### 3. Batch Processing
```python
indices = ["VNINDEX", "VN30", "HNX"]
results = {}

for index in indices:
    results[index] = scraper.scrape_vndirect_index(index)
    time.sleep(2)  # Rate limiting
```

## Troubleshooting

### 1. Common Issues

**AppleScript Permission Denied**
- Solution: Grant Accessibility permissions in System Preferences → Security & Privacy → Privacy → Accessibility

**Safari Not Responding**
- Solution: Force quit Safari and restart the scraping process

**JavaScript Execution Timeout**
- Solution: Increase wait times or improve network connection

**No Data Extracted**
- Solution: Website structure may have changed; update CSS selectors

### 2. Debugging Techniques

**Enable Verbose Logging**
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

**Inspect Page Source**
```python
# Get current page HTML
page_source = safari_script.call('executeJavaScript', 'document.body.innerHTML')
print(page_source[:1000])  # First 1000 characters
```

**Test JavaScript in Safari Console**
Open Safari → Developer → JavaScript Console and test extraction code manually.

## Future Enhancements

### 1. Advanced Features
- **Screenshot Capture**: Visual confirmation of scraping
- **Multi-tab Management**: Parallel scraping of multiple indices
- **Proxy Support**: Route through different IP addresses
- **CAPTCHA Handling**: Automated or manual CAPTCHA solving

### 2. Error Recovery
- **Automatic Retry**: Retry failed requests with exponential backoff
- **Browser Restart**: Automatically restart Safari if it becomes unresponsive
- **Fallback URLs**: Try alternative data sources if primary fails

### 3. Data Enhancement
- **Historical Data**: Scrape historical price charts
- **Real-time Updates**: Implement WebSocket connections for live data
- **News Integration**: Extract related news and market sentiment

## Comparison with Other Methods

| Method | Speed | Reliability | Detection Risk | Platform Support |
|--------|-------|-------------|----------------|------------------|
| Direct API | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Safari/AppleScript | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| Selenium | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Playwright | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| HTTP + BeautifulSoup | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ |

## Conclusion

The AppleScript + Safari approach provides a unique solution for web scraping that combines the reliability of browser automation with the stealth capabilities of native application integration. While it has platform limitations, it offers significant advantages for macOS-based applications requiring robust, human-like web scraping capabilities.

This method is particularly valuable when:
- Direct APIs are unreliable or unavailable
- Anti-bot measures block traditional scraping methods
- JavaScript-heavy sites require full browser rendering
- Maintaining session state is important
- Stealth scraping is a priority

The implementation demonstrates how modern applications can leverage platform-specific capabilities to create more robust and reliable data acquisition systems.
