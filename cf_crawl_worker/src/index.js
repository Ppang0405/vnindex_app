import puppeteer from '@cloudflare/puppeteer';

/**
 * Cloudflare Worker for scraping stock market data from CafeF
 * Uses Browser Rendering API to execute JavaScript and extract data
 */
export default {
  async fetch(request, env) {
    try {
      // Parse request URL and get parameters
      const url = new URL(request.url);
      const targetIndex = url.searchParams.get('index') || 'VNINDEX';
      
      // Map to source website URLs based on index name
      const sourceUrls = {
        'VNINDEX': 'https://liveboard.cafef.vn',
        'VN30': 'https://liveboard.cafef.vn/?center=1',
        'HNX': 'https://liveboard.cafef.vn/?center=2'
      };
      
      const targetUrl = sourceUrls[targetIndex];
      if (!targetUrl) {
        return new Response('Invalid index parameter', { status: 400 });
      }
      
      // Launch browser using the Browser Rendering API
      console.log(`Launching browser for ${targetUrl}...`);
      const browser = await puppeteer.launch(env.MYBROWSER);
      const page = await browser.newPage();
      
      // Navigate to target URL and wait for content to load
      await page.goto(targetUrl, { waitUntil: 'networkidle0' });
      console.log('Page loaded, waiting for data...');
      
      // Wait for stock data to be rendered
      await page.waitForSelector('.stock-data', { timeout: 10000 }).catch(() => {
        console.log('Stock data selector not found, continuing anyway');
      });
      
      // Extract stock data using page.evaluate to run JS in the browser context
      const stockData = await page.evaluate((index) => {
        // This function runs in the browser context
        const result = {
          index: index,
          value: null,
          change: null,
          changePercent: null,
          timestamp: new Date().toISOString()
        };
        
        // Extract data based on CafeF's DOM structure
        // These selectors need to be adjusted based on actual page structure
        try {
          if (index === 'VNINDEX') {
            // VNINDEX selectors
            const valueElement = document.querySelector('#vn-index .index-point');
            const changeElement = document.querySelector('#vn-index .index-change');
            const percentElement = document.querySelector('#vn-index .index-percent');
            
            if (valueElement) result.value = parseFloat(valueElement.textContent.trim().replace(',', ''));
            if (changeElement) result.change = parseFloat(changeElement.textContent.trim().replace(',', ''));
            if (percentElement) {
              const percentText = percentElement.textContent.trim();
              result.changePercent = parseFloat(percentText.replace('%', '').replace('(', '').replace(')', '').replace(',', ''));
            }
          } else if (index === 'VN30') {
            // VN30 selectors
            const valueElement = document.querySelector('#vn30-index .index-point');
            const changeElement = document.querySelector('#vn30-index .index-change');
            const percentElement = document.querySelector('#vn30-index .index-percent');
            
            if (valueElement) result.value = parseFloat(valueElement.textContent.trim().replace(',', ''));
            if (changeElement) result.change = parseFloat(changeElement.textContent.trim().replace(',', ''));
            if (percentElement) {
              const percentText = percentElement.textContent.trim();
              result.changePercent = parseFloat(percentText.replace('%', '').replace('(', '').replace(')', '').replace(',', ''));
            }
          } else if (index === 'HNX') {
            // HNX selectors
            const valueElement = document.querySelector('#hnx-index .index-point');
            const changeElement = document.querySelector('#hnx-index .index-change');
            const percentElement = document.querySelector('#hnx-index .index-percent');
            
            if (valueElement) result.value = parseFloat(valueElement.textContent.trim().replace(',', ''));
            if (changeElement) result.change = parseFloat(changeElement.textContent.trim().replace(',', ''));
            if (percentElement) {
              const percentText = percentElement.textContent.trim();
              result.changePercent = parseFloat(percentText.replace('%', '').replace('(', '').replace(')', '').replace(',', ''));
            }
          }
        } catch (e) {
          console.error('Error extracting data:', e);
        }
        
        return result;
      }, targetIndex);
      
      // Close the browser
      await browser.close();
      console.log(`Browser closed. Data extracted: ${JSON.stringify(stockData)}`);
      
      // Return the collected data as JSON
      return new Response(JSON.stringify(stockData), {
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Cache-Control': 'max-age=300' // Cache for 5 minutes
        }
      });
    } catch (error) {
      console.error('Worker error:', error);
      return new Response(`Error: ${error.message}`, { status: 500 });
    }
  }
};
