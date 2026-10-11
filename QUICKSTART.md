# Quick Start Guide

Get started with the Personal Financial Analyst in 5 minutes!

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `yfinance` - For real-time financial data
- `pandas` - For data manipulation
- `numpy` - For numerical operations

## Step 2: Test the System

Run the test suite to verify everything works:

```bash
python test_system.py
```

You should see all tests pass:
```
✓ Task Planner test passed
✓ Financial Tools test passed
✓ Verification test passed
✓ Integrated system test passed
```

## Step 3: Try Example Queries

Run the built-in examples:

```bash
python main.py --examples
```

This will execute several demo queries showing different capabilities.

## Step 4: Run Your First Query

### Option A: Interactive Mode

```bash
python main.py
```

Then type your query:
```
💰 Your query: Compare AAPL and MSFT revenue
```

### Option B: Command Line

```bash
python main.py --query "What is TSLA's profitability?"
```

Or simply:
```bash
python main.py Compare AAPL and MSFT
```

## What You Can Ask

### Company Comparisons
```
Compare AAPL and MSFT revenue
GOOGL vs META market cap
Which is more profitable: TSLA or FORD?
```

### Financial Analysis
```
What is AAPL's profitability?
Analyze MSFT financials
Show me GOOGL's financial ratios
```

### Cash & Liquidity
```
What is AMZN's cash position?
Analyze AAPL's cash flow
Show TSLA free cash flow
```

### Valuation
```
How is NVDA valued?
What is META's P/E ratio?
Show AAPL valuation metrics
```

## Understanding the Output

### Execution Flow

1. **Query Received**
   ```
   Query: Compare AAPL and MSFT revenue
   ```

2. **Plan Created**
   ```
   Total Steps: 3
   1. Compare companies on revenue
   2. Get detailed info for AAPL
   3. Get detailed info for MSFT
   ```

3. **Steps Executed**
   ```
   [Step 1] Compare companies on revenue
   Tool: compare_companies
   ✓ Step completed successfully
   ```

4. **Results Verified**
   ```
   ✓ All steps verified successfully
   ```

5. **Final Answer**
   ```
   ## Analysis: Compare AAPL and MSFT revenue
   
   ### Comparison by Revenue
   1. AAPL: $385,000,000,000
   2. MSFT: $211,000,000,000
   ```

## Common Issues

### ModuleNotFoundError
**Problem:** Missing dependencies
**Solution:** 
```bash
pip install -r requirements.txt
```

### "No data available"
**Problem:** Invalid ticker symbol
**Solution:** Check the ticker is correct (e.g., AAPL not APPLE)

### Connection errors
**Problem:** No internet or Yahoo Finance down
**Solution:** Check connection and retry

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore the code in each module
- Try different types of queries
- Customize the agent parameters

## Tips

1. **Use official ticker symbols** (AAPL, MSFT, GOOGL, etc.)
2. **Be specific in queries** - mention what you want to know
3. **Combine multiple tickers** - "Compare AAPL, MSFT, and GOOGL"
4. **Check cache** - repeated queries within 1 hour use cached data

## Examples by Complexity

### Simple (1-2 steps)
```
Get stock info for AAPL
What is MSFT's market cap?
```

### Medium (3-5 steps)
```
Compare AAPL and MSFT revenue
Calculate financial ratios for GOOGL
```

### Complex (5+ steps)
```
Compare AAPL, MSFT, and GOOGL on profitability
Analyze AMZN's financial health
```

## Help

### Command Line Options
```bash
python main.py --help
```

### Interactive Commands
```
exit    - Exit interactive mode
quit    - Exit interactive mode
q       - Exit interactive mode
```

---

**You're ready to start! 🚀**

Try running:
```bash
python main.py --query "Compare AAPL and MSFT"
```
