# Personal Financial Analyst

An intelligent financial analysis system that formulates complex financial inquiries and translates them into clear, step-by-step research plans. The system utilizes real-time market data to execute these tasks, verifies its own work, and continuously refines results until it arrives at a confident, data-backed answer.

## 🌐 Web Version Available!

Now with a beautiful web interface! Access the financial analyst through your browser with a modern, responsive UI.

- **Live Demo**: Run locally with `python app.py` → `http://localhost:5000`
- **Docker**: `docker-compose up -d` for instant deployment
- **Cloud Ready**: Deploy to Heroku, Railway, Render, or any cloud platform

## 🌟 Core Features

### 1. **Intelligent Task Planning**
Automatically breaks down complex queries into structured research steps using natural language understanding.

### 2. **Autonomous Execution**
Selects and invokes appropriate tools to gather financial data without manual intervention.

### 3. **Self-Verification**
Checks its own work and iterates until the task is complete with validated results.

### 4. **Real-Time Financial Data**
Access to:
- Income statements
- Balance sheets
- Cash flow statements
- Stock information
- Financial ratios
- Company comparisons

### 5. **Safety Mechanisms**
Built-in loop detection and step limits to prevent uncontrolled execution.

## 📋 Requirements

- Python 3.8+
- Internet connection (for real-time financial data)

## 🚀 Installation

1. Install required packages:
```bash
pip install -r requirements.txt
```

That's it! No API keys required - the system uses free financial data sources.

## 💻 Usage

### Web Interface (Recommended)
Run the web application for the best experience:

```bash
python app.py
```

Then open your browser to `http://localhost:5000`

Features:
- 🎨 Beautiful, modern UI
- 📊 Real-time analysis visualization
- 📝 Query history
- 🚀 Fast and responsive
- 📱 Mobile-friendly

### Interactive Mode (CLI)
Run the agent in interactive mode to ask questions:

```bash
python main.py
```

Then type your financial queries:
```
💰 Your query: Compare AAPL and MSFT revenue
💰 Your query: What is TSLA's profitability?
💰 Your query: Calculate financial ratios for GOOGL
```

### Single Query Mode
Run a single query from the command line:

```bash
python main.py --query "Compare AAPL and MSFT revenue"
```

Or simply:
```bash
python main.py Compare AAPL and MSFT revenue
```

### Example Queries Mode
Run pre-built example queries:

```bash
python main.py --examples
```

## 📊 Example Queries

The system understands various types of financial questions:

### Company Comparisons
```
Compare AAPL and MSFT revenue
Which is bigger: GOOGL or META market cap?
TSLA vs RIVN profitability
```

### Financial Ratios
```
Calculate financial ratios for AAPL
What is MSFT's profitability?
Show me GOOGL's ROE and ROA
```

### Cash Flow Analysis
```
Analyze AMZN's cash position
What is AAPL's free cash flow?
Show TSLA's operating cash flow
```

### Valuation Analysis
```
How is NVDA valued?
What is META's P/E ratio?
AAPL valuation metrics
```

### Comprehensive Analysis
```
Analyze MSFT
Full financial analysis of AAPL
Tell me about GOOGL's financials
```

## 🏗️ Architecture

### Core Components

1. **FinancialAgent** (`financial_agent.py`)
   - Main orchestrator
   - Manages task planning and execution
   - Implements verification loops
   - Includes loop detection and safety limits

2. **TaskPlanner** (`task_planner.py`)
   - Analyzes natural language queries
   - Extracts ticker symbols
   - Creates structured research plans
   - Handles dependencies between steps

3. **FinancialDataTools** (`financial_tools.py`)
   - Real-time data fetching via yfinance
   - Income statement retrieval
   - Balance sheet access
   - Cash flow data
   - Financial ratio calculations
   - Company comparisons
   - Built-in caching (1-hour TTL)

4. **ResultVerifier** (`verification.py`)
   - Validates data completeness
   - Checks data consistency
   - Verifies accounting equations
   - Quality assurance checks

5. **AnswerSynthesizer** (`answer_synthesizer.py`)
   - Combines multi-step results
   - Generates human-readable reports
   - Context-aware formatting
   - Comprehensive analysis synthesis

### Execution Flow

```
User Query
    ↓
Task Planner (breaks down into steps)
    ↓
Execution Loop
    ├─→ Execute Step
    ├─→ Verify Result
    ├─→ Check Dependencies
    ├─→ Detect Loops
    └─→ Iterate if needed
    ↓
Answer Synthesis
    ↓
Final Answer
```

## 🔧 Configuration

### Agent Parameters

```python
agent = FinancialAgent(
    max_steps=50,        # Maximum steps per plan
    max_iterations=10    # Maximum verification iterations
)
```

### Safety Limits

- **Max Steps**: 50 (prevents overly complex plans)
- **Max Iterations**: 10 (prevents infinite loops)
- **Loop Detection Window**: 10 recent steps
- **Loop Threshold**: 3 repetitions
- **Max Retries per Step**: 3

### Data Caching

- **Cache TTL**: 3600 seconds (1 hour)
- **Cache Keys**: Based on ticker, period, and data type
- Automatic cache invalidation

## 📁 Project Structure

```
PersonalFinancialAnalyst/
├── main.py                    # Main entry point
├── financial_agent.py         # Core agent orchestrator
├── task_planner.py           # Query analysis and planning
├── financial_tools.py        # Financial data tools
├── verification.py           # Result verification
├── answer_synthesizer.py    # Answer generation
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## 🎯 Key Design Principles

### 1. Modularity
Each component is independent and can be tested/updated separately.

### 2. Extensibility
Easy to add new tools, verification rules, or synthesis strategies.

### 3. Robustness
- Retry logic for failed steps
- Error handling at each level
- Data validation and verification
- Loop detection

### 4. Clarity
- Step-by-step execution visibility
- Human-readable progress output
- Comprehensive final reports

## 🔍 How It Works

### Task Planning Example

**Query:** "Compare AAPL and MSFT revenue"

**Generated Plan:**
1. Compare companies on revenue metric
2. Get detailed info for AAPL
3. Get detailed info for MSFT

### Verification Example

Each step is verified:
- ✓ Data completeness check
- ✓ Required fields present
- ✓ Value ranges reasonable
- ✓ No errors in results

### Loop Detection Example

If the same step executes 3+ times in a 10-step window:
```
⚠ Loop detected! Breaking execution.
```

## 📈 Data Sources

The system uses **yfinance** which provides free access to:
- Yahoo Finance data
- Real-time quotes
- Historical data
- Financial statements
- Company information

**No API key required!**

## ⚡ Performance

- **Caching**: 1-hour cache reduces API calls
- **Parallel-Ready**: Tools are independent
- **Efficient Planning**: Minimal necessary steps
- **Smart Dependencies**: Only fetch what's needed

## 🛡️ Safety Features

### Loop Detection
Prevents infinite loops by tracking execution patterns.

### Step Limits
Maximum 50 steps per plan prevents runaway execution.

### Iteration Limits
Maximum 10 verification iterations prevents endless refinement.

### Retry Limits
Each step can retry up to 3 times before failing.

### Error Handling
Comprehensive error catching and reporting at all levels.

## 🐛 Troubleshooting

### "No data available for ticker X"
- Check ticker symbol is correct
- Some companies may not have complete financial data
- Try a different company

### "Loop detected"
- The system detected repeated execution
- This is a safety feature preventing infinite loops
- Try rephrasing your query

### Connection errors
- Check internet connection
- Yahoo Finance may be temporarily unavailable
- The system will retry automatically

## 🔮 Future Enhancements

Potential additions:
- [ ] Support for more financial data sources
- [ ] Historical trend analysis
- [ ] Industry comparisons
- [ ] Custom ratio definitions
- [ ] Export to PDF/Excel
- [ ] Visualization charts
- [ ] Portfolio analysis
- [ ] AI-powered insights

## 📄 License

This project is provided as-is for educational and research purposes.

## 🙏 Acknowledgments

- **yfinance** for free financial data access
- **pandas** for data manipulation

## 📞 Support

For issues or questions, please review the code and documentation.

---

**Built with Python 3 | Powered by Real-Time Market Data**
