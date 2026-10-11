"""
Task Planner
Breaks down complex financial queries into structured research steps.
"""

import re
from typing import List, Dict, Any
from financial_agent import ResearchStep, TaskStatus


class TaskPlanner:
    """
    Intelligent task planner that analyzes queries and creates execution plans
    """
    
    def __init__(self, available_tools: List[str]):
        self.available_tools = available_tools
        self.query_patterns = self._build_patterns()
    
    def plan(self, query: str) -> List[ResearchStep]:
        """
        Create a research plan from a natural language query
        
        Args:
            query: Natural language financial question
            
        Returns:
            List of ResearchStep objects
        """
        query_lower = query.lower()
        steps = []
        step_id = 1
        
        # Extract tickers from query
        tickers = self._extract_tickers(query)
        
        # Determine query type and create appropriate steps
        if self._is_comparison_query(query_lower):
            steps.extend(self._plan_comparison(tickers, query_lower, step_id))
            
        elif self._is_ratio_analysis_query(query_lower):
            steps.extend(self._plan_ratio_analysis(tickers, query_lower, step_id))
            
        elif self._is_profitability_query(query_lower):
            steps.extend(self._plan_profitability_analysis(tickers, query_lower, step_id))
            
        elif self._is_liquidity_query(query_lower):
            steps.extend(self._plan_liquidity_analysis(tickers, query_lower, step_id))
            
        elif self._is_valuation_query(query_lower):
            steps.extend(self._plan_valuation_analysis(tickers, query_lower, step_id))
            
        else:
            # Default comprehensive analysis
            steps.extend(self._plan_comprehensive_analysis(tickers, query_lower, step_id))
        
        return steps
    
    def _extract_tickers(self, query: str) -> List[str]:
        """Extract stock ticker symbols from query"""
        # Common patterns for tickers
        patterns = [
            r'\b([A-Z]{1,5})\b',  # All caps words
            r'ticker[s]?\s*[:=]?\s*([A-Z, ]+)',  # "ticker: AAPL" or "tickers: AAPL, MSFT"
        ]
        
        tickers = set()
        for pattern in patterns:
            matches = re.findall(pattern, query)
            for match in matches:
                # Split by comma if multiple tickers
                if ',' in match:
                    tickers.update([t.strip() for t in match.split(',')])
                else:
                    tickers.add(match.strip())
        
        # Filter out common false positives
        exclude = {'I', 'A', 'IS', 'ARE', 'IT', 'THE', 'VS', 'AND', 'OR', 'FOR', 'TO', 'OF', 'IN'}
        tickers = [t for t in tickers if t not in exclude and len(t) <= 5]
        
        return list(tickers)
    
    def _is_comparison_query(self, query: str) -> bool:
        """Detect if query is asking for company comparison"""
        keywords = ['compare', 'comparison', 'versus', 'vs', 'better', 'difference between']
        return any(kw in query for kw in keywords)
    
    def _is_ratio_analysis_query(self, query: str) -> bool:
        """Detect if query is asking for financial ratios"""
        keywords = ['ratio', 'ratios', 'roe', 'roa', 'margin', 'profitability metrics']
        return any(kw in query for kw in keywords)
    
    def _is_profitability_query(self, query: str) -> bool:
        """Detect if query is about profitability"""
        keywords = ['profit', 'profitable', 'earnings', 'revenue', 'income']
        return any(kw in query for kw in keywords)
    
    def _is_liquidity_query(self, query: str) -> bool:
        """Detect if query is about liquidity/cash position"""
        keywords = ['cash', 'liquidity', 'cash flow', 'working capital']
        return any(kw in query for kw in keywords)
    
    def _is_valuation_query(self, query: str) -> bool:
        """Detect if query is about valuation"""
        keywords = ['valuation', 'valued', 'worth', 'market cap', 'p/e', 'pe ratio']
        return any(kw in query for kw in keywords)
    
    def _plan_comparison(self, tickers: List[str], query: str, start_id: int) -> List[ResearchStep]:
        """Plan steps for company comparison"""
        steps = []
        current_id = start_id
        
        # Determine what metric to compare
        metric = "revenue"
        if "market cap" in query or "valuation" in query:
            metric = "market_cap"
        elif "profit" in query or "earnings" in query:
            metric = "net_income"
        
        # Step 1: Get comparison
        steps.append(ResearchStep(
            step_id=current_id,
            description=f"Compare companies on {metric}",
            tool_name="compare_companies",
            parameters={"tickers": tickers, "metric": metric}
        ))
        current_id += 1
        
        # Step 2: Get detailed info for each company
        for ticker in tickers:
            steps.append(ResearchStep(
                step_id=current_id,
                description=f"Get detailed info for {ticker}",
                tool_name="get_stock_info",
                parameters={"ticker": ticker},
                dependencies=[start_id]
            ))
            current_id += 1
        
        return steps
    
    def _plan_ratio_analysis(self, tickers: List[str], query: str, start_id: int) -> List[ResearchStep]:
        """Plan steps for financial ratio analysis"""
        steps = []
        current_id = start_id
        
        for ticker in tickers:
            # Calculate ratios
            steps.append(ResearchStep(
                step_id=current_id,
                description=f"Calculate financial ratios for {ticker}",
                tool_name="calculate_financial_ratios",
                parameters={"ticker": ticker}
            ))
            current_id += 1
        
        return steps
    
    def _plan_profitability_analysis(self, tickers: List[str], query: str, start_id: int) -> List[ResearchStep]:
        """Plan steps for profitability analysis"""
        steps = []
        current_id = start_id
        
        for ticker in tickers:
            # Get income statement
            steps.append(ResearchStep(
                step_id=current_id,
                description=f"Get income statement for {ticker}",
                tool_name="get_income_statement",
                parameters={"ticker": ticker, "period": "annual"}
            ))
            income_step_id = current_id
            current_id += 1
            
            # Calculate ratios
            steps.append(ResearchStep(
                step_id=current_id,
                description=f"Calculate profitability ratios for {ticker}",
                tool_name="calculate_financial_ratios",
                parameters={"ticker": ticker},
                dependencies=[income_step_id]
            ))
            current_id += 1
        
        return steps
    
    def _plan_liquidity_analysis(self, tickers: List[str], query: str, start_id: int) -> List[ResearchStep]:
        """Plan steps for liquidity analysis"""
        steps = []
        current_id = start_id
        
        for ticker in tickers:
            # Get balance sheet
            steps.append(ResearchStep(
                step_id=current_id,
                description=f"Get balance sheet for {ticker}",
                tool_name="get_balance_sheet",
                parameters={"ticker": ticker, "period": "annual"}
            ))
            balance_step_id = current_id
            current_id += 1
            
            # Get cash flow
            steps.append(ResearchStep(
                step_id=current_id,
                description=f"Get cash flow statement for {ticker}",
                tool_name="get_cash_flow",
                parameters={"ticker": ticker, "period": "annual"},
                dependencies=[balance_step_id]
            ))
            current_id += 1
        
        return steps
    
    def _plan_valuation_analysis(self, tickers: List[str], query: str, start_id: int) -> List[ResearchStep]:
        """Plan steps for valuation analysis"""
        steps = []
        current_id = start_id
        
        for ticker in tickers:
            # Get stock info for valuation metrics
            steps.append(ResearchStep(
                step_id=current_id,
                description=f"Get valuation metrics for {ticker}",
                tool_name="get_stock_info",
                parameters={"ticker": ticker}
            ))
            info_step_id = current_id
            current_id += 1
            
            # Calculate ratios
            steps.append(ResearchStep(
                step_id=current_id,
                description=f"Calculate financial ratios for {ticker}",
                tool_name="calculate_financial_ratios",
                parameters={"ticker": ticker},
                dependencies=[info_step_id]
            ))
            current_id += 1
        
        return steps
    
    def _plan_comprehensive_analysis(self, tickers: List[str], query: str, start_id: int) -> List[ResearchStep]:
        """Plan steps for comprehensive financial analysis"""
        steps = []
        current_id = start_id
        
        if not tickers:
            # Default to a common stock if no ticker found
            tickers = ["AAPL"]
        
        for ticker in tickers:
            # Get all financial statements
            steps.append(ResearchStep(
                step_id=current_id,
                description=f"Get stock info for {ticker}",
                tool_name="get_stock_info",
                parameters={"ticker": ticker}
            ))
            info_step_id = current_id
            current_id += 1
            
            steps.append(ResearchStep(
                step_id=current_id,
                description=f"Get income statement for {ticker}",
                tool_name="get_income_statement",
                parameters={"ticker": ticker, "period": "annual"},
                dependencies=[info_step_id]
            ))
            current_id += 1
            
            steps.append(ResearchStep(
                step_id=current_id,
                description=f"Get balance sheet for {ticker}",
                tool_name="get_balance_sheet",
                parameters={"ticker": ticker, "period": "annual"},
                dependencies=[info_step_id]
            ))
            current_id += 1
            
            steps.append(ResearchStep(
                step_id=current_id,
                description=f"Get cash flow for {ticker}",
                tool_name="get_cash_flow",
                parameters={"ticker": ticker, "period": "annual"},
                dependencies=[info_step_id]
            ))
            current_id += 1
            
            steps.append(ResearchStep(
                step_id=current_id,
                description=f"Calculate financial ratios for {ticker}",
                tool_name="calculate_financial_ratios",
                parameters={"ticker": ticker},
                dependencies=[info_step_id]
            ))
            current_id += 1
        
        return steps
    
    def _build_patterns(self) -> Dict[str, Any]:
        """Build regex patterns for query analysis"""
        return {
            "tickers": r'\b([A-Z]{1,5})\b',
            "comparison": r'(compare|versus|vs|better)',
            "metrics": r'(revenue|profit|earnings|cash|market cap)',
        }


if __name__ == "__main__":
    # Test the planner
    planner = TaskPlanner(available_tools=[
        "get_income_statement",
        "get_balance_sheet",
        "get_cash_flow",
        "get_stock_info",
        "calculate_financial_ratios",
        "compare_companies"
    ])
    
    test_queries = [
        "Compare AAPL and MSFT revenue",
        "What is TSLA's profitability?",
        "Calculate financial ratios for GOOGL",
        "Analyze AMZN's cash position"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        steps = planner.plan(query)
        print(f"Generated {len(steps)} steps:")
        for step in steps:
            print(f"  {step.step_id}. {step.description} ({step.tool_name})")
