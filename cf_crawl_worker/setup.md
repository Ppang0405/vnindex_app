# Setting Up the Browser Rendering API

As of 2023, the Cloudflare Browser Rendering API is available for Cloudflare Workers but requires specific setup. Here's how to get it working:

## Accessing the Browser Rendering API

The Browser Rendering API is a feature that requires activation on your Cloudflare account:

1. Log in to your [Cloudflare Dashboard](https://dash.cloudflare.com/)
2. Navigate to "Workers & Pages"
3. Select your Worker (or create a new one)
4. Go to Settings > Browser
5. Add a new browser binding (named "BROWSER" in our configuration)

## Current Limitations

- Browser Rendering API is currently in an early access phase
- Full browser automation features require a paid Cloudflare Workers subscription
- There may be usage limitations based on your account plan

## Configuration Options

The `wrangler.toml` configuration has been updated to match the current API requirements:

```toml
[browser]
binding = "BROWSER"
type = "browser"
```

This replaces the older `[[browser_bindings]]` syntax.

## Package Versions

We've updated the `@cloudflare/puppeteer` package to the latest stable version compatible with the current Browser Rendering API. If you encounter issues, try:

```bash
npm uninstall @cloudflare/puppeteer
npm install @cloudflare/puppeteer@latest
```

## Local Development

To test the worker locally with browser functionality:

1. Ensure you have the latest Wrangler version:
   ```bash
   npm install -g wrangler@latest
   ```

2. Run the development server:
   ```bash
   npx wrangler dev
   ```

Note: Browser bindings might have limited functionality in local development compared to deployed Workers.

## Troubleshooting Common Issues

1. **Access Denied to Browser Binding**
   - Verify your account has access to Browser Rendering features
   - Check that the browser binding is correctly set in the dashboard

2. **Timeout Errors**
   - Browser operations have execution time limits
   - Complex scraping operations may need optimization

3. **JavaScript Execution Errors**
   - The browser environment has some limitations
   - Test with simpler page.evaluate() scripts first

4. **Debugging Tips**
   - Use console.log() statements for debugging
   - The logs are visible in the Cloudflare Dashboard under "Workers > Your Worker > Logs"

## Additional Resources

- [Official Browser Rendering Documentation](https://developers.cloudflare.com/workers/runtime-apis/browser)
- [Puppeteer API Documentation](https://pptr.dev/)
