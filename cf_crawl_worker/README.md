# CafeF Stock Data Scraper with Cloudflare Workers

This project uses Cloudflare Workers with the Browser Rendering API to scrape Vietnam stock market data from CafeF's website. It handles JavaScript-rendered pages by executing a headless browser directly in Cloudflare's edge infrastructure.

## Prerequisites

- [Node.js](https://nodejs.org/) (16.x or higher)
- [Wrangler CLI](https://developers.cloudflare.com/workers/wrangler/install-and-update/)
- Cloudflare account with Workers subscription
- Cloudflare account with Browser Rendering API access (Free tier: 10 minutes/day, 3 concurrent browsers)

## Setup

1. Install dependencies:
   ```
   npm install
   ```

2. Log in to your Cloudflare account:
   ```
   npx wrangler login
   ```

3. Enable the Browser Rendering API:
   - Log in to your Cloudflare Dashboard
   - Navigate to Workers & Pages
   - Select your Worker or create a new one
   - Go to Settings > Browser
   - Enable the Browser Binding by adding a binding named "MYBROWSER"

4. Update the `wrangler.toml` file with your specific configurations if needed.

## Development

Run the worker locally for testing:
```
npm run dev
```

Note: Local development with Browser Rendering requires the latest version of Wrangler.

## Deployment

Deploy the worker to Cloudflare:
```
npm run deploy
```

## Usage

Once deployed, you can access the worker with:

```
https://<your-worker-subdomain>.workers.dev/?index=VNINDEX
```

Available index parameters:
- `VNINDEX` (default)
- `VN30`
- `HNX`

## Browser Rendering API

This worker uses Cloudflare's Browser Rendering API, which provides a way to run a headless browser directly within Cloudflare Workers. This allows for rendering JavaScript-dependent web pages and extracting data from them. As of August 2025, the API offers a free tier with 10 minutes of browser usage per day and up to 3 concurrent browsers.

The API works by:
1. Creating a browser binding in your Worker configuration
2. Using the `@cloudflare/puppeteer` library to control the browser
3. Enabling you to navigate to pages, execute JavaScript, and extract data

## Response Format

The API returns JSON with the following structure:

```json
{
  "index": "VNINDEX",
  "value": 1200.34,
  "change": 5.67,
  "changePercent": 0.47,
  "timestamp": "2023-09-21T08:30:00.000Z"
}
```

## Resources

- [Cloudflare Browser Rendering API Documentation](https://developers.cloudflare.com/browser-rendering/)
- [Cloudflare Browser Rendering API Pricing](https://developers.cloudflare.com/browser-rendering/platform/pricing/)
- [Cloudflare Workers Documentation](https://developers.cloudflare.com/workers/)
- [Puppeteer API Documentation](https://pptr.dev/)