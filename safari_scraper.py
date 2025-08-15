"""
Safari-based stock data scraper using AppleScript automation.

This module uses py-applescript to control Safari and extract Vietnamese stock market data
from VNDirect website using the browser's dev tools and JavaScript execution capabilities.
"""

import time
import json
import re
from typing import Optional, Dict, List, Any, Union
import applescript


class SafariStockScraper:
    """
    A Safari-based web scraper for Vietnamese stock market data using AppleScript automation.
    """
    
    def __init__(self):
        self.safari_script: Optional[applescript.AppleScript] = None
        self.setup_safari_control()
    
    def setup_safari_control(self):
        """Initialize Safari control AppleScript."""
        safari_control_script = '''
        on openURLInSafari(targetURL)
            tell application "Safari"
                activate
                if (count of windows) = 0 then
                    make new document with properties {URL:targetURL}
                else
                    set URL of current tab of front window to targetURL
                end if
                
                -- Wait for page to load
                repeat 30 times
                    delay 1
                    if (do JavaScript "document.readyState" in current tab of front window) = "complete" then
                        exit repeat
                    end if
                end repeat
                
                return true
            end tell
        end openURLInSafari
        
        on executeJavaScript(jsCode)
            tell application "Safari"
                try
                    set result to do JavaScript jsCode in current tab of front window
                    return result
                on error errMsg
                    return "ERROR: " & errMsg
                end try
            end tell
        end executeJavaScript
        
        on waitForElement(selector, maxWaitSeconds)
            tell application "Safari"
                repeat maxWaitSeconds times
                    delay 1
                    try
                        set elementExists to do JavaScript "document.querySelector('" & selector & "') !== null" in current tab of front window
                        if elementExists then
                            return true
                        end if
                    on error
                        -- Continue waiting
                    end try
                end repeat
                return false
            end tell
        end waitForElement
        
        on getPageTitle()
            tell application "Safari"
                return name of current tab of front window
            end tell
        end getPageTitle
        '''
        
        self.safari_script = applescript.AppleScript(safari_control_script)
    
    def scrape_vndirect_index(self, index_symbol: str) -> Optional[Dict[str, Any]]:
        """
        Scrape stock index data from VNDirect website using Safari.
        
        Args:
            index_symbol: The stock index symbol (e.g., 'VNINDEX', 'VN30', 'HNX')
            
        Returns:
            Dictionary containing stock data or None if failed
        """
        try:
            # VNDirect market overview URL
            vndirect_url = "https://www.vndirect.com.vn/portal/thong-ke-thi-truong-chung-khoan/chi-so-chung-khoan.shtml"
            
            print(f"🌐 Opening VNDirect website in Safari...")
            
            # Open URL in Safari
            if self.safari_script is None:
                raise Exception("Safari script not initialized")
                
            success = self.safari_script.call('openURLInSafari', vndirect_url)
            if not success:
                raise Exception("Failed to open URL in Safari")
            
            # Wait for page elements to load
            print("⏳ Waiting for page to load...")
            time.sleep(3)
            
            # Check if we're on the right page
            page_title = self.safari_script.call('getPageTitle')
            print(f"📄 Page title: {page_title}")
            
            # JavaScript to extract index data from VNDirect
            js_extraction_code = f'''
            function extractIndexData() {{
                try {{
                    // Look for index data tables or cards
                    const indexData = {{}};
                    
                    // Method 1: Try to find data in tables
                    const tables = document.querySelectorAll('table');
                    for (let table of tables) {{
                        const rows = table.querySelectorAll('tr');
                        for (let row of rows) {{
                            const cells = row.querySelectorAll('td, th');
                            if (cells.length >= 3) {{
                                const symbolCell = cells[0];
                                const valueCell = cells[1];
                                const changeCell = cells[2];
                                
                                if (symbolCell && symbolCell.textContent.includes('{index_symbol}')) {{
                                    indexData.symbol = '{index_symbol}';
                                    indexData.value = parseFloat(valueCell.textContent.replace(/[^0-9.-]/g, ''));
                                    
                                    const changeText = changeCell.textContent;
                                    const changeMatch = changeText.match(/([+-]?[0-9.]+)/g);
                                    if (changeMatch && changeMatch.length >= 2) {{
                                        indexData.change = parseFloat(changeMatch[0]);
                                        indexData.changePercent = parseFloat(changeMatch[1]);
                                    }}
                                    break;
                                }}
                            }}
                        }}
                        if (indexData.value) break;
                    }}
                    
                    // Method 2: Look for specific index cards or sections
                    if (!indexData.value) {{
                        // Try to find index cards by class names or data attributes
                        const indexCards = document.querySelectorAll('[data-symbol="{index_symbol}"], .index-card, .market-index');
                        for (let card of indexCards) {{
                            const valueElement = card.querySelector('.value, .price, .index-value');
                            const changeElement = card.querySelector('.change, .change-value');
                            const percentElement = card.querySelector('.percent, .change-percent');
                            
                            if (valueElement) {{
                                indexData.symbol = '{index_symbol}';
                                indexData.value = parseFloat(valueElement.textContent.replace(/[^0-9.-]/g, ''));
                                
                                if (changeElement) {{
                                    indexData.change = parseFloat(changeElement.textContent.replace(/[^0-9.-]/g, ''));
                                }}
                                
                                if (percentElement) {{
                                    indexData.changePercent = parseFloat(percentElement.textContent.replace(/[^0-9.-]/g, ''));
                                }}
                                break;
                            }}
                        }}
                    }}
                    
                    // Method 3: Search for text containing the index name
                    if (!indexData.value) {{
                        const allElements = document.querySelectorAll('*');
                        for (let element of allElements) {{
                            if (element.textContent.includes('{index_symbol}') && element.textContent.match(/[0-9,]+\\.[0-9]{{2}}/)) {{
                                const text = element.textContent;
                                const numbers = text.match(/[0-9,]+\\.[0-9]{{2,3}}/g);
                                if (numbers && numbers.length > 0) {{
                                    indexData.symbol = '{index_symbol}';
                                    indexData.value = parseFloat(numbers[0].replace(/,/g, ''));
                                    
                                    // Try to find change info in nearby elements
                                    const parent = element.parentElement;
                                    if (parent) {{
                                        const changeText = parent.textContent;
                                        const changeMatch = changeText.match(/([+-]?[0-9.]+).*?([+-]?[0-9.]+)%/);
                                        if (changeMatch) {{
                                            indexData.change = parseFloat(changeMatch[1]);
                                            indexData.changePercent = parseFloat(changeMatch[2]);
                                        }}
                                    }}
                                    break;
                                }}
                            }}
                        }}
                    }}
                    
                    // Add timestamp
                    indexData.timestamp = new Date().toISOString();
                    indexData.source = 'VNDirect (Safari)';
                    
                    return JSON.stringify(indexData);
                    
                }} catch (error) {{
                    return JSON.stringify({{
                        error: error.message,
                        symbol: '{index_symbol}',
                        timestamp: new Date().toISOString()
                    }});
                }}
            }}
            
            extractIndexData();
            '''
            
            print(f"🔍 Extracting {index_symbol} data using JavaScript...")
            
            # Execute JavaScript in Safari
            if self.safari_script is None:
                raise Exception("Safari script not initialized")
                
            result = self.safari_script.call('executeJavaScript', js_extraction_code)
            
            if isinstance(result, str) and result.startswith('ERROR:'):
                print(f"❌ JavaScript error: {result}")
                return None
            
            # Parse the JSON result
            try:
                if isinstance(result, str):
                    data = json.loads(result)
                elif isinstance(result, dict):
                    data = result
                else:
                    print(f"⚠️  Unexpected result type: {type(result)}")
                    return None
                if 'error' in data:
                    print(f"❌ Extraction error: {data['error']}")
                    return None
                
                if data.get('value'):
                    print(f"✅ Successfully extracted data: {data}")
                    return data
                else:
                    print("⚠️  No value found, trying alternative extraction...")
                    return self._try_alternative_extraction(index_symbol)
                    
            except json.JSONDecodeError as e:
                print(f"❌ JSON parsing error: {e}")
                print(f"Raw result: {result}")
                return None
                
        except Exception as e:
            print(f"❌ Safari scraping error: {e}")
            return None
    
    def _try_alternative_extraction(self, index_symbol: str) -> Optional[Dict[str, Any]]:
        """Try alternative extraction method by getting page source."""
        try:
            # Get page source using JavaScript
            page_source_js = '''
            function getPageContent() {
                return document.body.innerHTML;
            }
            getPageContent();
            '''
            
            if self.safari_script is None:
                return None
                
            page_source = self.safari_script.call('executeJavaScript', page_source_js)
            
            if isinstance(page_source, str) and not page_source.startswith('ERROR:'):
                # Use regex to extract index data from HTML source
                return self._extract_from_html(page_source, index_symbol)
            
            return None
            
        except Exception as e:
            print(f"❌ Alternative extraction error: {e}")
            return None
    
    def _extract_from_html(self, html: str, index_symbol: str) -> Optional[Dict[str, Any]]:
        """Extract index data from HTML source using regex patterns."""
        try:
            # Pattern to find index data in HTML
            patterns = [
                # Pattern 1: Look for index value with symbol
                rf'{index_symbol}.*?([0-9,]+\.[0-9]{{2,3}})',
                # Pattern 2: Look for decimal numbers that could be index values
                r'([0-9,]{1,4}\.[0-9]{2,3})',
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, html, re.IGNORECASE)
                
                for match in matches:
                    try:
                        value = float(match.replace(',', ''))
                        # Vietnamese stock indices are typically in range 500-2000
                        if 500 <= value <= 2000:
                            return {
                                'symbol': index_symbol,
                                'value': value,
                                'change': 0,  # Default values when can't extract
                                'changePercent': 0,
                                'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S'),
                                'source': 'VNDirect (Safari HTML)',
                                'note': 'Partial data extracted from HTML'
                            }
                    except ValueError:
                        continue
            
            return None
            
        except Exception as e:
            print(f"❌ HTML extraction error: {e}")
            return None
    
    def close_safari(self):
        """Close Safari (optional)."""
        try:
            close_script = applescript.AppleScript('''
                tell application "Safari"
                    quit
                end tell
            ''')
            close_script.run()
        except Exception as e:
            print(f"Note: Could not close Safari: {e}")


def fetch_stock_data_safari(symbol: str, start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Fetch stock data using Safari automation (compatible with existing helper.py interface).
    
    Args:
        symbol: Stock symbol (e.g., 'VNINDEX', 'VN30', 'HNX')
        start_date: Start date (unused in Safari scraper, kept for compatibility)
        end_date: End date (unused in Safari scraper, kept for compatibility)
        
    Returns:
        List of dictionaries containing stock data
    """
    scraper = SafariStockScraper()
    
    try:
        data = scraper.scrape_vndirect_index(symbol)
        
        if data and data.get('value'):
            # Convert to list format expected by main.py
            return [{
                'date': data.get('timestamp', ''),
                'close': data.get('value', 0),
                'open': data.get('value', 0),  # Use close as open since we don't have historical data
                'high': data.get('value', 0),
                'low': data.get('value', 0),
                'volume': 0,  # Not available from this scraping method
                'change': data.get('change', 0),
                'changePercent': data.get('changePercent', 0),
                'source': data.get('source', 'Safari'),
            }]
        else:
            print(f"❌ No data retrieved for {symbol}")
            return []
            
    except Exception as e:
        print(f"❌ Safari fetch error: {e}")
        return []
    finally:
        # Optionally close Safari
        # scraper.close_safari()
        pass


if __name__ == "__main__":
    """Test the Safari scraper."""
    print("🧪 Testing Safari Stock Scraper...")
    
    # Test with VN-Index
    print("\n" + "="*50)
    print("Testing VNINDEX...")
    data = fetch_stock_data_safari("VNINDEX")
    
    if data:
        print(f"✅ Success! Retrieved data: {data[0]}")
    else:
        print("❌ Failed to retrieve VNINDEX data")
    
    # Test with VN30
    print("\n" + "="*50)
    print("Testing VN30...")
    data = fetch_stock_data_safari("VN30")
    
    if data:
        print(f"✅ Success! Retrieved data: {data[0]}")
    else:
        print("❌ Failed to retrieve VN30 data")
    
    print("\n🏁 Testing complete!")
