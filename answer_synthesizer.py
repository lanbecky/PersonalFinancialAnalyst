"""
Answer Synthesizer
Synthesizes final answers from completed research steps.
"""

from typing import Dict, Any, List
from financial_agent import ResearchPlan, ResearchStep, TaskStatus


class AnswerSynthesizer:
    """
    Combines results from multiple research steps into coherent answers
    """
    
    def synthesize(self, plan: ResearchPlan) -> str:
        """
        Synthesize final answer from research plan
        
        Args:
            plan: Completed ResearchPlan
            
        Returns:
            Human-readable answer string
        """
        # Collect completed steps
        completed = [s for s in plan.steps if s.status in [TaskStatus.COMPLETED, TaskStatus.VERIFIED]]
        
        if not completed:
            return "No results to synthesize."
        
        # Build answer based on query type
        query_lower = plan.query.lower()
        
        if "compare" in query_lower or "versus" in query_lower or "vs" in query_lower:
            return self._synthesize_comparison(plan, completed)
        elif "ratio" in query_lower or "profitability" in query_lower:
            return self._synthesize_ratios(plan, completed)
        elif "cash" in query_lower or "liquidity" in query_lower:
            return self._synthesize_liquidity(plan, completed)
        elif "valuation" in query_lower or "worth" in query_lower:
            return self._synthesize_valuation(plan, completed)
        else:
            return self._synthesize_general(plan, completed)
    
    def _synthesize_comparison(self, plan: ResearchPlan, steps: List[ResearchStep]) -> str:
        """Synthesize comparison analysis"""
        answer_parts = [f"## Analysis: {plan.query}\n"]
        
        # Find comparison step
        comparison_step = next((s for s in steps if s.tool_name == "compare_companies"), None)
        
        if comparison_step and comparison_step.result:
            result = comparison_step.result
            metric = result.get("metric", "unknown")
            ranking = result.get("ranking", [])
            
            answer_parts.append(f"\n### Comparison by {metric.replace('_', ' ').title()}\n")
            
            for rank_data in ranking:
                ticker = rank_data["ticker"]
                value = rank_data["value"]
                rank = rank_data["rank"]
                
                answer_parts.append(f"{rank}. **{ticker}**: ${value:,.0f}")
            
            # Add detailed info for each company
            answer_parts.append("\n### Detailed Information\n")
            
            for step in steps:
                if step.tool_name == "get_stock_info" and step.result:
                    info = step.result
                    ticker = info.get("ticker")
                    company = info.get("company_name")
                    sector = info.get("sector")
                    market_cap = info.get("market_cap", 0)
                    pe_ratio = info.get("pe_ratio", 0)
                    
                    answer_parts.append(f"\n**{ticker} - {company}**")
                    answer_parts.append(f"  - Sector: {sector}")
                    answer_parts.append(f"  - Market Cap: ${market_cap:,.0f}")
                    answer_parts.append(f"  - P/E Ratio: {pe_ratio:.2f}")
        
        return "\n".join(answer_parts)
    
    def _synthesize_ratios(self, plan: ResearchPlan, steps: List[ResearchStep]) -> str:
        """Synthesize ratio analysis"""
        answer_parts = [f"## Analysis: {plan.query}\n"]
        
        for step in steps:
            if step.tool_name == "calculate_financial_ratios" and step.result:
                result = step.result
                ticker = result.get("ticker")
                profitability = result.get("profitability", {})
                valuation = result.get("valuation", {})
                
                answer_parts.append(f"\n### {ticker} Financial Ratios\n")
                
                answer_parts.append("**Profitability:**")
                answer_parts.append(f"  - Net Profit Margin: {profitability.get('net_profit_margin', 0):.2f}%")
                answer_parts.append(f"  - Return on Assets (ROA): {profitability.get('return_on_assets', 0):.2f}%")
                answer_parts.append(f"  - Return on Equity (ROE): {profitability.get('return_on_equity', 0):.2f}%")
                
                answer_parts.append("\n**Valuation:**")
                answer_parts.append(f"  - P/E Ratio: {valuation.get('pe_ratio', 0):.2f}")
                answer_parts.append(f"  - Price to Book: {valuation.get('price_to_book', 0):.2f}")
        
        return "\n".join(answer_parts)
    
    def _synthesize_liquidity(self, plan: ResearchPlan, steps: List[ResearchStep]) -> str:
        """Synthesize liquidity analysis"""
        answer_parts = [f"## Analysis: {plan.query}\n"]
        
        # Group steps by ticker
        ticker_data = {}
        
        for step in steps:
            if step.result and "ticker" in step.result:
                ticker = step.result["ticker"]
                if ticker not in ticker_data:
                    ticker_data[ticker] = {}
                
                if step.tool_name == "get_balance_sheet":
                    ticker_data[ticker]["balance"] = step.result
                elif step.tool_name == "get_cash_flow":
                    ticker_data[ticker]["cashflow"] = step.result
        
        for ticker, data in ticker_data.items():
            answer_parts.append(f"\n### {ticker} Liquidity Analysis\n")
            
            if "balance" in data:
                balance = data["balance"]
                summary = balance.get("summary", {})
                cash = summary.get("latest_cash", 0)
                total_assets = summary.get("latest_total_assets", 0)
                
                answer_parts.append(f"**Balance Sheet:**")
                answer_parts.append(f"  - Cash & Equivalents: ${cash:,.0f}")
                answer_parts.append(f"  - Total Assets: ${total_assets:,.0f}")
                answer_parts.append(f"  - Cash Ratio: {(cash/total_assets*100) if total_assets else 0:.2f}%")
            
            if "cashflow" in data:
                cashflow = data["cashflow"]
                summary = cashflow.get("summary", {})
                operating_cf = summary.get("latest_operating_cash_flow", 0)
                free_cf = summary.get("latest_free_cash_flow", 0)
                
                answer_parts.append(f"\n**Cash Flow:**")
                answer_parts.append(f"  - Operating Cash Flow: ${operating_cf:,.0f}")
                answer_parts.append(f"  - Free Cash Flow: ${free_cf:,.0f}")
        
        return "\n".join(answer_parts)
    
    def _synthesize_valuation(self, plan: ResearchPlan, steps: List[ResearchStep]) -> str:
        """Synthesize valuation analysis"""
        answer_parts = [f"## Analysis: {plan.query}\n"]
        
        for step in steps:
            if step.tool_name == "get_stock_info" and step.result:
                info = step.result
                ticker = info.get("ticker")
                company = info.get("company_name")
                market_cap = info.get("market_cap", 0)
                pe_ratio = info.get("pe_ratio", 0)
                forward_pe = info.get("forward_pe", 0)
                pb_ratio = info.get("price_to_book", 0)
                current_price = info.get("current_price", 0)
                
                answer_parts.append(f"\n### {ticker} - {company}\n")
                answer_parts.append(f"**Current Valuation:**")
                answer_parts.append(f"  - Current Price: ${current_price:.2f}")
                answer_parts.append(f"  - Market Cap: ${market_cap:,.0f}")
                answer_parts.append(f"  - P/E Ratio (Trailing): {pe_ratio:.2f}")
                answer_parts.append(f"  - P/E Ratio (Forward): {forward_pe:.2f}")
                answer_parts.append(f"  - Price to Book: {pb_ratio:.2f}")
        
        return "\n".join(answer_parts)
    
    def _synthesize_general(self, plan: ResearchPlan, steps: List[ResearchStep]) -> str:
        """Synthesize general comprehensive analysis"""
        answer_parts = [f"## Analysis: {plan.query}\n"]
        
        # Group by ticker
        ticker_data = {}
        
        for step in steps:
            if step.result and isinstance(step.result, dict):
                ticker = step.result.get("ticker")
                if ticker:
                    if ticker not in ticker_data:
                        ticker_data[ticker] = {
                            "info": None,
                            "income": None,
                            "balance": None,
                            "cashflow": None,
                            "ratios": None
                        }
                    
                    if step.tool_name == "get_stock_info":
                        ticker_data[ticker]["info"] = step.result
                    elif step.tool_name == "get_income_statement":
                        ticker_data[ticker]["income"] = step.result
                    elif step.tool_name == "get_balance_sheet":
                        ticker_data[ticker]["balance"] = step.result
                    elif step.tool_name == "get_cash_flow":
                        ticker_data[ticker]["cashflow"] = step.result
                    elif step.tool_name == "calculate_financial_ratios":
                        ticker_data[ticker]["ratios"] = step.result
        
        # Build comprehensive report for each ticker
        for ticker, data in ticker_data.items():
            answer_parts.append(f"\n{'='*60}")
            
            # Company Info
            if data["info"]:
                info = data["info"]
                answer_parts.append(f"\n### {ticker} - {info.get('company_name')}\n")
                answer_parts.append(f"**Company Overview:**")
                answer_parts.append(f"  - Sector: {info.get('sector')}")
                answer_parts.append(f"  - Industry: {info.get('industry')}")
                answer_parts.append(f"  - Market Cap: ${info.get('market_cap', 0):,.0f}")
                answer_parts.append(f"  - Current Price: ${info.get('current_price', 0):.2f}")
            
            # Financial Highlights
            if data["income"]:
                income = data["income"]["summary"]
                answer_parts.append(f"\n**Income Statement (Latest):**")
                answer_parts.append(f"  - Revenue: ${income.get('latest_revenue', 0):,.0f}")
                answer_parts.append(f"  - Net Income: ${income.get('latest_net_income', 0):,.0f}")
                answer_parts.append(f"  - Gross Profit: ${income.get('latest_gross_profit', 0):,.0f}")
            
            if data["balance"]:
                balance = data["balance"]["summary"]
                answer_parts.append(f"\n**Balance Sheet (Latest):**")
                answer_parts.append(f"  - Total Assets: ${balance.get('latest_total_assets', 0):,.0f}")
                answer_parts.append(f"  - Total Liabilities: ${balance.get('latest_total_liabilities', 0):,.0f}")
                answer_parts.append(f"  - Stockholder Equity: ${balance.get('latest_stockholder_equity', 0):,.0f}")
            
            if data["cashflow"]:
                cashflow = data["cashflow"]["summary"]
                answer_parts.append(f"\n**Cash Flow (Latest):**")
                answer_parts.append(f"  - Operating Cash Flow: ${cashflow.get('latest_operating_cash_flow', 0):,.0f}")
                answer_parts.append(f"  - Free Cash Flow: ${cashflow.get('latest_free_cash_flow', 0):,.0f}")
            
            if data["ratios"]:
                ratios = data["ratios"]
                profitability = ratios.get("profitability", {})
                answer_parts.append(f"\n**Key Ratios:**")
                answer_parts.append(f"  - Net Profit Margin: {profitability.get('net_profit_margin', 0):.2f}%")
                answer_parts.append(f"  - ROA: {profitability.get('return_on_assets', 0):.2f}%")
                answer_parts.append(f"  - ROE: {profitability.get('return_on_equity', 0):.2f}%")
        
        answer_parts.append(f"\n{'='*60}")
        
        return "\n".join(answer_parts)


if __name__ == "__main__":
    print("Answer Synthesizer module loaded")
