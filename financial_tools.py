"""
Financial Data Tools
Provides access to real-time financial data including income statements, balance sheets, and cash flows.
"""

import yfinance as yf
import pandas as pd
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import time


class FinancialDataTools:
    """
    Collection of tools for fetching and analyzing financial data
    """
    
    def __init__(self):
        self.cache = {}
        self.cache_ttl = 3600  # 1 hour cache
    
    def get_income_statement(self, ticker: str, period: str = "annual") -> Dict[str, Any]:
        """
        Fetch income statement for a company
        
        Args:
            ticker: Stock ticker symbol (e.g., 'AAPL', 'MSFT')
            period: 'annual' or 'quarterly'
            
        Returns:
            Dictionary with income statement data
        """
        cache_key = f"income_{ticker}_{period}"
        
        if self._is_cached(cache_key):
            print(f"  [Cache hit] Using cached income statement for {ticker}")
            return self.cache[cache_key]["data"]
        
        try:
            print(f"  [API] Fetching income statement for {ticker}...")
            stock = yf.Ticker(ticker)
            
            if period == "annual":
                income_stmt = stock.income_stmt
            else:
                income_stmt = stock.quarterly_income_stmt
            
            if income_stmt.empty:
                return {"error": f"No income statement data available for {ticker}"}
            
            # Convert to dictionary format
            result = {
                "ticker": ticker,
                "period": period,
                "currency": self._get_currency(stock),
                "data": income_stmt.to_dict(),
                "summary": {
                    "latest_revenue": self._safe_get(income_stmt, "Total Revenue", 0),
                    "latest_net_income": self._safe_get(income_stmt, "Net Income", 0),
                    "latest_operating_income": self._safe_get(income_stmt, "Operating Income", 0),
                    "latest_gross_profit": self._safe_get(income_stmt, "Gross Profit", 0),
                },
                "fetched_at": datetime.now().isoformat()
            }
            
            self._cache_data(cache_key, result)
            return result
            
        except Exception as e:
            return {"error": f"Failed to fetch income statement: {str(e)}"}
    
    def get_balance_sheet(self, ticker: str, period: str = "annual") -> Dict[str, Any]:
        """
        Fetch balance sheet for a company
        
        Args:
            ticker: Stock ticker symbol
            period: 'annual' or 'quarterly'
            
        Returns:
            Dictionary with balance sheet data
        """
        cache_key = f"balance_{ticker}_{period}"
        
        if self._is_cached(cache_key):
            print(f"  [Cache hit] Using cached balance sheet for {ticker}")
            return self.cache[cache_key]["data"]
        
        try:
            print(f"  [API] Fetching balance sheet for {ticker}...")
            stock = yf.Ticker(ticker)
            
            if period == "annual":
                balance_sheet = stock.balance_sheet
            else:
                balance_sheet = stock.quarterly_balance_sheet
            
            if balance_sheet.empty:
                return {"error": f"No balance sheet data available for {ticker}"}
            
            result = {
                "ticker": ticker,
                "period": period,
                "currency": self._get_currency(stock),
                "data": balance_sheet.to_dict(),
                "summary": {
                    "latest_total_assets": self._safe_get(balance_sheet, "Total Assets", 0),
                    "latest_total_liabilities": self._safe_get(balance_sheet, "Total Liabilities Net Minority Interest", 0),
                    "latest_stockholder_equity": self._safe_get(balance_sheet, "Stockholders Equity", 0),
                    "latest_cash": self._safe_get(balance_sheet, "Cash And Cash Equivalents", 0),
                },
                "fetched_at": datetime.now().isoformat()
            }
            
            self._cache_data(cache_key, result)
            return result
            
        except Exception as e:
            return {"error": f"Failed to fetch balance sheet: {str(e)}"}
    
    def get_cash_flow(self, ticker: str, period: str = "annual") -> Dict[str, Any]:
        """
        Fetch cash flow statement for a company
        
        Args:
            ticker: Stock ticker symbol
            period: 'annual' or 'quarterly'
            
        Returns:
            Dictionary with cash flow data
        """
        cache_key = f"cashflow_{ticker}_{period}"
        
        if self._is_cached(cache_key):
            print(f"  [Cache hit] Using cached cash flow for {ticker}")
            return self.cache[cache_key]["data"]
        
        try:
            print(f"  [API] Fetching cash flow for {ticker}...")
            stock = yf.Ticker(ticker)
            
            if period == "annual":
                cash_flow = stock.cashflow
            else:
                cash_flow = stock.quarterly_cashflow
            
            if cash_flow.empty:
                return {"error": f"No cash flow data available for {ticker}"}
            
            result = {
                "ticker": ticker,
                "period": period,
                "currency": self._get_currency(stock),
                "data": cash_flow.to_dict(),
                "summary": {
                    "latest_operating_cash_flow": self._safe_get(cash_flow, "Operating Cash Flow", 0),
                    "latest_investing_cash_flow": self._safe_get(cash_flow, "Investing Cash Flow", 0),
                    "latest_financing_cash_flow": self._safe_get(cash_flow, "Financing Cash Flow", 0),
                    "latest_free_cash_flow": self._safe_get(cash_flow, "Free Cash Flow", 0),
                },
                "fetched_at": datetime.now().isoformat()
            }
            
            self._cache_data(cache_key, result)
            return result
            
        except Exception as e:
            return {"error": f"Failed to fetch cash flow: {str(e)}"}
    
    def get_stock_info(self, ticker: str) -> Dict[str, Any]:
        """
        Get general stock information and key metrics
        
        Args:
            ticker: Stock ticker symbol
            
        Returns:
            Dictionary with stock info
        """
        cache_key = f"info_{ticker}"
        
        if self._is_cached(cache_key):
            print(f"  [Cache hit] Using cached stock info for {ticker}")
            return self.cache[cache_key]["data"]
        
        try:
            print(f"  [API] Fetching stock info for {ticker}...")
            stock = yf.Ticker(ticker)
            info = stock.info
            
            result = {
                "ticker": ticker,
                "company_name": info.get("longName", "N/A"),
                "sector": info.get("sector", "N/A"),
                "industry": info.get("industry", "N/A"),
                "market_cap": info.get("marketCap", 0),
                "pe_ratio": info.get("trailingPE", 0),
                "forward_pe": info.get("forwardPE", 0),
                "price_to_book": info.get("priceToBook", 0),
                "dividend_yield": info.get("dividendYield", 0),
                "52_week_high": info.get("fiftyTwoWeekHigh", 0),
                "52_week_low": info.get("fiftyTwoWeekLow", 0),
                "current_price": info.get("currentPrice", 0),
                "fetched_at": datetime.now().isoformat()
            }
            
            self._cache_data(cache_key, result)
            return result
            
        except Exception as e:
            return {"error": f"Failed to fetch stock info: {str(e)}"}
    
    def calculate_financial_ratios(self, ticker: str) -> Dict[str, Any]:
        """
        Calculate key financial ratios from financial statements
        
        Args:
            ticker: Stock ticker symbol
            
        Returns:
            Dictionary with calculated ratios
        """
        try:
            print(f"  [Calculate] Computing financial ratios for {ticker}...")
            
            # Get necessary data
            income = self.get_income_statement(ticker)
            balance = self.get_balance_sheet(ticker)
            info = self.get_stock_info(ticker)
            
            if "error" in income or "error" in balance:
                return {"error": "Missing required financial data for ratio calculation"}
            
            # Extract values
            revenue = income["summary"]["latest_revenue"]
            net_income = income["summary"]["latest_net_income"]
            total_assets = balance["summary"]["latest_total_assets"]
            total_equity = balance["summary"]["latest_stockholder_equity"]
            
            # Calculate ratios
            result = {
                "ticker": ticker,
                "profitability": {
                    "net_profit_margin": (net_income / revenue * 100) if revenue else 0,
                    "return_on_assets": (net_income / total_assets * 100) if total_assets else 0,
                    "return_on_equity": (net_income / total_equity * 100) if total_equity else 0,
                },
                "valuation": {
                    "pe_ratio": info.get("pe_ratio", 0),
                    "price_to_book": info.get("price_to_book", 0),
                },
                "calculated_at": datetime.now().isoformat()
            }
            
            return result
            
        except Exception as e:
            return {"error": f"Failed to calculate ratios: {str(e)}"}
    
    def compare_companies(self, tickers: List[str], metric: str = "revenue") -> Dict[str, Any]:
        """
        Compare multiple companies on a specific metric
        
        Args:
            tickers: List of ticker symbols
            metric: Metric to compare (revenue, net_income, market_cap, etc.)
            
        Returns:
            Comparison dictionary
        """
        try:
            print(f"  [Compare] Comparing {len(tickers)} companies on {metric}...")
            
            comparison = {
                "metric": metric,
                "companies": {},
                "comparison_date": datetime.now().isoformat()
            }
            
            for ticker in tickers:
                if metric in ["revenue", "net_income"]:
                    data = self.get_income_statement(ticker)
                    if "error" not in data:
                        value = data["summary"].get(f"latest_{metric}", 0)
                        comparison["companies"][ticker] = value
                        
                elif metric == "market_cap":
                    data = self.get_stock_info(ticker)
                    if "error" not in data:
                        comparison["companies"][ticker] = data.get("market_cap", 0)
            
            # Rank companies
            ranked = sorted(comparison["companies"].items(), key=lambda x: x[1], reverse=True)
            comparison["ranking"] = [{"ticker": t, "value": v, "rank": i+1} for i, (t, v) in enumerate(ranked)]
            
            return comparison
            
        except Exception as e:
            return {"error": f"Failed to compare companies: {str(e)}"}
    
    def _safe_get(self, df: pd.DataFrame, column: str, index: int = 0) -> float:
        """Safely get a value from DataFrame"""
        try:
            if column in df.index:
                values = df.loc[column].values
                if len(values) > index:
                    value = values[index]
                    return float(value) if pd.notna(value) else 0.0
            return 0.0
        except:
            return 0.0
    
    def _get_currency(self, stock) -> str:
        """Get the currency for a stock"""
        try:
            return stock.info.get("currency", "USD")
        except:
            return "USD"
    
    def _is_cached(self, key: str) -> bool:
        """Check if data is in cache and not expired"""
        if key not in self.cache:
            return False
        
        cached_time = self.cache[key]["timestamp"]
        return (time.time() - cached_time) < self.cache_ttl
    
    def _cache_data(self, key: str, data: Any):
        """Cache data with timestamp"""
        self.cache[key] = {
            "data": data,
            "timestamp": time.time()
        }


def register_tools(agent):
    """Register all financial tools with the agent"""
    tools = FinancialDataTools()
    
    agent.register_tool("get_income_statement", tools.get_income_statement)
    agent.register_tool("get_balance_sheet", tools.get_balance_sheet)
    agent.register_tool("get_cash_flow", tools.get_cash_flow)
    agent.register_tool("get_stock_info", tools.get_stock_info)
    agent.register_tool("calculate_financial_ratios", tools.calculate_financial_ratios)
    agent.register_tool("compare_companies", tools.compare_companies)
    
    return tools


if __name__ == "__main__":
    # Test the tools
    tools = FinancialDataTools()
    
    print("Testing Financial Tools...")
    print("\n1. Income Statement for AAPL:")
    income = tools.get_income_statement("AAPL")
    print(f"   Revenue: ${income['summary']['latest_revenue']:,.0f}")
    
    print("\n2. Balance Sheet for AAPL:")
    balance = tools.get_balance_sheet("AAPL")
    print(f"   Total Assets: ${balance['summary']['latest_total_assets']:,.0f}")
    
    print("\n3. Stock Info for AAPL:")
    info = tools.get_stock_info("AAPL")
    print(f"   Market Cap: ${info['market_cap']:,.0f}")
