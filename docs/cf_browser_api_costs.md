# Cloudflare Browser Rendering API Cost Analysis

This document analyzes the costs associated with using Cloudflare's Browser Rendering API for the Vietnam Stock Market data scraping project as of August 2025.

## Current API Pricing Structure

### Free Plan
- **Daily Usage Limit**: 10 minutes of browser usage
- **Concurrent Browsers**: Up to 3 concurrent browser instances
- **Additional Usage**: Not available (hard limit)

### Paid Workers Plan
- **Monthly Usage Included**: 10 hours of browser usage
- **Concurrent Browsers**: Up to 10 concurrent browser instances (monthly average)
- **Base Cost**: $5/month for Workers Paid plan
- **Additional Usage**:
  - $0.09 per additional browser hour
  - $2.00 per additional concurrent browser (if exceeding 10)

## Project Usage Requirements

Our stock market data scraper has the following characteristics:

- **Daily API Calls**: 360 calls per day
- **Estimated Time per Call**: 4-7 seconds
  - Browser launch: ~0.5 seconds
  - Page navigation: ~2-3 seconds
  - Content loading & rendering: ~1-3 seconds
  - Data extraction: ~0.2 seconds

## Cost Calculations

### Daily Resource Usage
- **Total Browser Time**: 
  - Minimum: 360 calls × 4 seconds = 1,440 seconds = 24 minutes/day
  - Maximum: 360 calls × 7 seconds = 2,520 seconds = 42 minutes/day

### Monthly Resource Usage
- **Total Browser Time**:
  - Minimum: 24 minutes × 30 days = 720 minutes = 12 hours/month
  - Maximum: 42 minutes × 30 days = 1,260 minutes = 21 hours/month

### Monthly Cost Breakdown
1. **Base Paid Workers Plan**: $5.00/month
2. **Included Browser Hours**: 10 hours/month
3. **Additional Browser Hours**:
   - Minimum scenario: (12 - 10) = 2 hours × $0.09/hour = $0.18/month
   - Maximum scenario: (21 - 10) = 11 hours × $0.09/hour = $0.99/month
4. **Concurrent Browser Surcharge**: $0 (assuming no more than 10 concurrent sessions)

### Total Estimated Monthly Cost
- **Minimum Scenario**: $5.18/month
- **Maximum Scenario**: $5.99/month
- **Annual Cost Range**: $62.16 - $71.88/year

## Cost Optimization Strategies

While the current cost projections are reasonable, the following strategies could reduce costs if needed:

1. **Implement Caching**:
   - Cache results for 5-15 minutes to reduce API calls
   - This could reduce the number of calls by 70-80%

2. **Batch Multiple Indices**:
   - Fetch VNINDEX, VN30, and HNX in a single browser session
   - This would reduce calls by approximately 66%

3. **Optimize Browser Performance**:
   - Set shorter timeouts for faster completion
   - Use more specific selectors instead of waiting for network idle
   - Disable unnecessary browser features

## Conclusion

At 360 calls per day, the Cloudflare Browser Rendering API would cost approximately $5.18-$5.99 per month, which is cost-effective compared to hosting our own browser automation infrastructure. The pricing structure is scalable and predictable, making it suitable for our usage patterns.

The Workers Paid plan is required since our daily usage exceeds the Free plan's 10-minute limit by approximately 2.4-4.2 times. However, the additional costs beyond the base plan are minimal, keeping the overall expense reasonable.
