# AppleScript Implementation Guide: Step-by-Step Tutorial

## Quick Start Guide

This guide provides practical steps to implement and use the AppleScript Safari scraping solution for Vietnamese stock market data.

## Prerequisites Checklist

### System Requirements
- [ ] macOS 10.14 or later
- [ ] Safari browser installed and updated
- [ ] Python 3.7+ installed
- [ ] Terminal access

### Permission Setup
1. **System Preferences** → **Security & Privacy** → **Privacy** → **Accessibility**
   - Click the lock to make changes
   - Add your Python application or Terminal to the list
   - Ensure the checkbox is checked

2. **Safari Preferences** → **Advanced**
   - Check "Show Develop menu in menu bar"
   - This helps with debugging JavaScript issues

## Installation Steps

### 1. Install Python Dependencies

```bash
# Navigate to your project directory
cd /path/to/vnindex_app

# Create virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate

# Install required packages
pip install pyobjc-core pyobjc-framework-Cocoa
pip install applescript
pip install pandas requests rumps
```

### 2. Verify AppleScript Installation

```bash
# Test basic AppleScript functionality
python3 -c "
import applescript
script = applescript.AppleScript('return \"Hello from AppleScript\"')
print(script.run())
"
```

Expected output: `Hello from AppleScript`

### 3. Test Safari Control

```bash
# Test Safari automation
python3 -c "
import applescript
script = applescript.AppleScript('''
tell application \"Safari\"
    activate
    return name of application \"Safari\"
end tell
''')
print(script.run())
"
```

This should activate Safari and return "Safari".

## File Structure

```
vnindex_app/
├── safari_scraper.py          # Main Safari scraper implementation
├── helper.py                  # Updated with Safari fallback
├── main.py                    # Modified rumps app with Safari option
├── requirements.txt           # Updated dependencies
└── docs/
    ├── applescript_safari_scraping.md    # Detailed documentation
    └── applescript_implementation.md     # This file
```

## Testing the Implementation

### 1. Test Safari Scraper Standalone

```bash
# Run the scraper test
python3 safari_scraper.py
```

Expected behavior:
1. Safari will launch/activate
2. Navigate to VNDirect website
3. Execute JavaScript to extract data
4. Print extracted stock data

### 2. Test with Main Application

```bash
# Run the main VNIndex app
python3 main.py
```

Menu options should now include:
- Use Safari Scraper
- Use API Only

### 3. Test Fallback Functionality

```python
# Test the fallback system
python3 -c "
from helper import fetch_stock_data_with_fallback
data = fetch_stock_data_with_fallback('VNINDEX', '2024-01-01', '2024-01-02')
print(f'Data source: {data[0][\"source\"] if data else \"No data\"}')
"
```

## Common Implementation Patterns

### 1. Basic AppleScript Pattern

```python
import applescript

# Define AppleScript as multi-line string
script_source = '''
tell application "Safari"
    activate
    set URL of current tab of front window to "https://example.com"
    
    repeat 10 times
        delay 1
        if (do JavaScript "document.readyState" in current tab of front window) = "complete" then
            exit repeat
        end if
    end repeat
    
    return do JavaScript "document.title" in current tab of front window
end tell
'''

# Compile and run
script = applescript.AppleScript(script_source)
result = script.run()
print(f"Page title: {result}")
```

### 2. JavaScript Execution Pattern

```python
# Execute JavaScript in Safari
js_code = '''
function extractData() {
    const elements = document.querySelectorAll('.price');
    const prices = Array.from(elements).map(el => el.textContent);
    return JSON.stringify(prices);
}
extractData();
'''

result = safari_script.call('executeJavaScript', js_code)
data = json.loads(result)
```

### 3. Error Handling Pattern

```python
def safe_execute_script(script, method_name, *args):
    try:
        if script is None:
            raise Exception("Script not initialized")
        
        result = script.call(method_name, *args)
        
        if isinstance(result, str) and result.startswith('ERROR:'):
            raise Exception(f"AppleScript error: {result}")
            
        return result
        
    except Exception as e:
        print(f"Script execution failed: {e}")
        return None
```

## Debugging Techniques

### 1. Enable AppleScript Debugging

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Add debug prints to AppleScript
debug_script = '''
tell application "Safari"
    log "Activating Safari..."
    activate
    
    log "Setting URL..."
    set URL of current tab of front window to "https://example.com"
    
    log "Script completed successfully"
    return "OK"
end tell
'''
```

### 2. JavaScript Console Integration

```python
# Get JavaScript console errors
js_debug = '''
function getConsoleErrors() {
    // This approach captures some errors
    const errors = [];
    const originalError = console.error;
    
    console.error = function(...args) {
        errors.push(args.join(' '));
        originalError.apply(console, args);
    };
    
    return JSON.stringify(errors);
}
getConsoleErrors();
'''

errors = safari_script.call('executeJavaScript', js_debug)
print(f"Console errors: {errors}")
```

### 3. Page Source Inspection

```python
# Get full page source for debugging
def debug_page_content():
    page_html = safari_script.call('executeJavaScript', 'document.body.innerHTML')
    
    # Save to file for inspection
    with open('debug_page.html', 'w', encoding='utf-8') as f:
        f.write(page_html)
    
    print("Page source saved to debug_page.html")
```

## Performance Optimization

### 1. Safari Window Management

```python
# Reuse existing Safari window instead of creating new ones
reuse_window_script = '''
tell application "Safari"
    activate
    
    if (count of windows) = 0 then
        make new document with properties {URL:"about:blank"}
    end if
    
    -- Use existing window
    set URL of current tab of front window to targetURL
end tell
'''
```

### 2. Intelligent Waiting

```python
# Wait for specific elements instead of fixed delays
smart_wait_js = '''
function waitForElement(selector, maxTime = 10000) {
    return new Promise((resolve, reject) => {
        const startTime = Date.now();
        
        function check() {
            const element = document.querySelector(selector);
            if (element) {
                resolve(element);
            } else if (Date.now() - startTime >= maxTime) {
                reject(new Error('Element not found within timeout'));
            } else {
                setTimeout(check, 100);
            }
        }
        
        check();
    });
}

// Usage
waitForElement('.price-value')
    .then(element => element.textContent)
    .catch(error => 'TIMEOUT');
'''
```

### 3. Batch Processing

```python
def scrape_multiple_indices(indices):
    """Scrape multiple indices in a single Safari session."""
    scraper = SafariStockScraper()
    results = {}
    
    try:
        for i, index in enumerate(indices):
            print(f"Scraping {index} ({i+1}/{len(indices)})...")
            
            results[index] = scraper.scrape_vndirect_index(index)
            
            # Add delay between requests (except for the last one)
            if i < len(indices) - 1:
                time.sleep(2)
                
    except Exception as e:
        print(f"Batch scraping error: {e}")
    
    return results
```

## Error Recovery Strategies

### 1. Automatic Safari Restart

```python
def restart_safari():
    """Force restart Safari if it becomes unresponsive."""
    try:
        # Quit Safari
        quit_script = applescript.AppleScript('''
            tell application "Safari" to quit
        ''')
        quit_script.run()
        
        time.sleep(2)
        
        # Restart Safari
        start_script = applescript.AppleScript('''
            tell application "Safari" to activate
        ''')
        start_script.run()
        
        time.sleep(3)
        return True
        
    except Exception as e:
        print(f"Safari restart failed: {e}")
        return False
```

### 2. Retry with Exponential Backoff

```python
def retry_with_backoff(func, max_retries=3, base_delay=1):
    """Retry function with exponential backoff."""
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            
            delay = base_delay * (2 ** attempt)
            print(f"Attempt {attempt + 1} failed, retrying in {delay}s...")
            time.sleep(delay)
```

### 3. Fallback Chain

```python
def robust_scrape(symbol):
    """Multi-method scraping with fallback chain."""
    methods = [
        lambda: scrape_method_1(symbol),  # Table extraction
        lambda: scrape_method_2(symbol),  # CSS selector extraction  
        lambda: scrape_method_3(symbol),  # Text pattern matching
        lambda: scrape_method_4(symbol),  # HTML source parsing
    ]
    
    for i, method in enumerate(methods):
        try:
            result = method()
            if result and result.get('value'):
                print(f"Success with method {i + 1}")
                return result
        except Exception as e:
            print(f"Method {i + 1} failed: {e}")
            continue
    
    print("All methods failed")
    return None
```

## Production Deployment

### 1. Configuration Management

```python
# config.py
class ScrapingConfig:
    # Timing settings
    PAGE_LOAD_TIMEOUT = 30
    ELEMENT_WAIT_TIMEOUT = 10
    REQUEST_DELAY = 2
    
    # Target URLs
    VNDIRECT_URL = "https://www.vndirect.com.vn/portal/thong-ke-thi-truong-chung-khoan/chi-so-chung-khoan.shtml"
    
    # Retry settings
    MAX_RETRIES = 3
    BACKOFF_FACTOR = 2
    
    # Debug settings
    SAVE_DEBUG_HTML = False
    VERBOSE_LOGGING = False
```

### 2. Monitoring and Alerting

```python
import time
import logging
from datetime import datetime

class ScrapingMonitor:
    def __init__(self):
        self.success_count = 0
        self.error_count = 0
        self.last_success = None
        self.last_error = None
    
    def record_success(self):
        self.success_count += 1
        self.last_success = datetime.now()
        
    def record_error(self, error):
        self.error_count += 1
        self.last_error = datetime.now()
        logging.error(f"Scraping failed: {error}")
        
        # Alert if too many failures
        if self.error_count > 5:
            self.send_alert(f"High error rate: {self.error_count} errors")
    
    def send_alert(self, message):
        # Implement your preferred alerting method
        # (email, Slack, push notification, etc.)
        print(f"ALERT: {message}")
```

### 3. Logging and Persistence

```python
import json
import os
from datetime import datetime

class DataPersistence:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
    
    def save_scraped_data(self, symbol, data):
        """Save scraped data with timestamp."""
        filename = f"{symbol}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(self.data_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"Data saved to {filepath}")
    
    def load_latest_data(self, symbol):
        """Load most recent data for symbol."""
        pattern = f"{symbol}_*.json"
        files = glob.glob(os.path.join(self.data_dir, pattern))
        
        if not files:
            return None
        
        latest_file = max(files, key=os.path.getctime)
        
        with open(latest_file, 'r') as f:
            return json.load(f)
```

## Integration Examples

### 1. With Flask Web API

```python
from flask import Flask, jsonify
from safari_scraper import SafariStockScraper

app = Flask(__name__)
scraper = SafariStockScraper()

@app.route('/api/stock/<symbol>')
def get_stock_data(symbol):
    try:
        data = scraper.scrape_vndirect_index(symbol.upper())
        return jsonify({
            'success': True,
            'data': data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
```

### 2. With Scheduled Jobs

```python
import schedule
import time
from safari_scraper import SafariStockScraper

def scheduled_scraping():
    """Run every 15 minutes during market hours."""
    scraper = SafariStockScraper()
    indices = ['VNINDEX', 'VN30', 'HNX']
    
    for index in indices:
        try:
            data = scraper.scrape_vndirect_index(index)
            print(f"{index}: {data['value']:.2f} ({data['changePercent']:+.2f}%)")
        except Exception as e:
            print(f"Failed to scrape {index}: {e}")

# Schedule jobs
schedule.every(15).minutes.do(scheduled_scraping)

# Run scheduler
while True:
    schedule.run_pending()
    time.sleep(60)
```

## Troubleshooting Guide

### Issue: Permission Denied
**Symptom**: `execution error: Not authorized to send Apple events to Safari`
**Solution**: Grant Accessibility permissions in System Preferences

### Issue: Safari Doesn't Respond
**Symptom**: Script hangs or Safari doesn't activate
**Solution**: 
```python
# Force activate Safari
activate_script = '''
tell application "Safari"
    activate
    delay 2
end tell
'''
```

### Issue: JavaScript Errors
**Symptom**: `ERROR: ReferenceError: document is not defined`
**Solution**: Ensure page is fully loaded before executing JavaScript

### Issue: No Data Extracted
**Symptom**: Script runs but returns empty results
**Solution**: 
1. Check if website structure changed
2. Update CSS selectors
3. Add debug logging to JavaScript
4. Verify page is loading correctly

### Issue: Memory Usage
**Symptom**: High memory consumption
**Solution**: 
1. Close unnecessary Safari tabs
2. Implement Safari restart after N operations
3. Use batch processing sparingly

## Best Practices

1. **Always implement timeouts** for all operations
2. **Use try-catch blocks** extensively
3. **Implement proper logging** for debugging
4. **Respect rate limits** (2-3 seconds between requests)
5. **Test with different network conditions**
6. **Monitor for website changes** regularly
7. **Have fallback methods** ready
8. **Document your selectors** and update them as needed

This implementation guide provides a solid foundation for using AppleScript + Safari for stock data scraping while maintaining reliability and performance.
