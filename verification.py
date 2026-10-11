"""
Result Verification
Validates and verifies the results of financial data fetching and analysis.
"""

from typing import Dict, Any, Optional
from financial_agent import ResearchStep


class ResultVerifier:
    """
    Verifies the quality and completeness of research results
    """
    
    def __init__(self):
        self.verification_rules = self._build_verification_rules()
    
    def verify_step(self, step: ResearchStep) -> bool:
        """
        Verify a single research step
        
        Args:
            step: ResearchStep to verify
            
        Returns:
            True if step result is valid, False otherwise
        """
        if step.result is None:
            return False
        
        # Check for error in result
        if isinstance(step.result, dict) and "error" in step.result:
            print(f"  ✗ Verification failed: {step.result['error']}")
            return False
        
        # Tool-specific verification
        tool_name = step.tool_name
        
        if tool_name == "get_income_statement":
            return self._verify_income_statement(step.result)
        elif tool_name == "get_balance_sheet":
            return self._verify_balance_sheet(step.result)
        elif tool_name == "get_cash_flow":
            return self._verify_cash_flow(step.result)
        elif tool_name == "get_stock_info":
            return self._verify_stock_info(step.result)
        elif tool_name == "calculate_financial_ratios":
            return self._verify_ratios(step.result)
        elif tool_name == "compare_companies":
            return self._verify_comparison(step.result)
        
        # Default: check if result is not empty
        return bool(step.result)
    
    def _verify_income_statement(self, result: Dict[str, Any]) -> bool:
        """Verify income statement data"""
        if not isinstance(result, dict):
            return False
        
        # Check required fields
        required_fields = ["ticker", "period", "data", "summary"]
        if not all(field in result for field in required_fields):
            print("  ✗ Missing required fields in income statement")
            return False
        
        # Check summary has key metrics
        summary = result.get("summary", {})
        if not summary.get("latest_revenue"):
            print("  ✗ Missing revenue data")
            return False
        
        # Validate data is not empty
        if not result.get("data"):
            print("  ✗ Empty income statement data")
            return False
        
        print("  ✓ Income statement verified")
        return True
    
    def _verify_balance_sheet(self, result: Dict[str, Any]) -> bool:
        """Verify balance sheet data"""
        if not isinstance(result, dict):
            return False
        
        required_fields = ["ticker", "period", "data", "summary"]
        if not all(field in result for field in required_fields):
            print("  ✗ Missing required fields in balance sheet")
            return False
        
        summary = result.get("summary", {})
        
        # Basic accounting equation check: Assets = Liabilities + Equity
        assets = summary.get("latest_total_assets", 0)
        liabilities = summary.get("latest_total_liabilities", 0)
        equity = summary.get("latest_stockholder_equity", 0)
        
        if assets > 0:
            # Allow 1% tolerance for rounding
            balance = abs(assets - (liabilities + equity))
            tolerance = assets * 0.01
            
            if balance > tolerance:
                print(f"  ⚠ Balance sheet equation off: {balance:,.0f} (tolerance: {tolerance:,.0f})")
                # Don't fail, just warn
        
        print("  ✓ Balance sheet verified")
        return True
    
    def _verify_cash_flow(self, result: Dict[str, Any]) -> bool:
        """Verify cash flow data"""
        if not isinstance(result, dict):
            return False
        
        required_fields = ["ticker", "period", "data", "summary"]
        if not all(field in result for field in required_fields):
            print("  ✗ Missing required fields in cash flow")
            return False
        
        summary = result.get("summary", {})
        
        # Check that we have operating cash flow
        if "latest_operating_cash_flow" not in summary:
            print("  ✗ Missing operating cash flow")
            return False
        
        print("  ✓ Cash flow verified")
        return True
    
    def _verify_stock_info(self, result: Dict[str, Any]) -> bool:
        """Verify stock info data"""
        if not isinstance(result, dict):
            return False
        
        # Check essential fields
        if not result.get("ticker"):
            print("  ✗ Missing ticker in stock info")
            return False
        
        if not result.get("company_name") or result.get("company_name") == "N/A":
            print("  ✗ Invalid company name")
            return False
        
        # Check for reasonable market cap (> 0)
        market_cap = result.get("market_cap", 0)
        if market_cap <= 0:
            print("  ⚠ Market cap is zero or negative")
            # Don't fail, some stocks might have issues
        
        print("  ✓ Stock info verified")
        return True
    
    def _verify_ratios(self, result: Dict[str, Any]) -> bool:
        """Verify calculated financial ratios"""
        if not isinstance(result, dict):
            return False
        
        # Check for ratio categories
        if "profitability" not in result:
            print("  ✗ Missing profitability ratios")
            return False
        
        profitability = result.get("profitability", {})
        
        # Validate ratio ranges (basic sanity checks)
        net_margin = profitability.get("net_profit_margin", 0)
        if abs(net_margin) > 100:
            print(f"  ⚠ Unusual profit margin: {net_margin:.1f}%")
            # Don't fail, some companies can have extreme margins
        
        print("  ✓ Financial ratios verified")
        return True
    
    def _verify_comparison(self, result: Dict[str, Any]) -> bool:
        """Verify company comparison results"""
        if not isinstance(result, dict):
            return False
        
        # Check required fields
        if "companies" not in result or "ranking" not in result:
            print("  ✗ Missing comparison data")
            return False
        
        companies = result.get("companies", {})
        if len(companies) < 2:
            print("  ✗ Comparison needs at least 2 companies")
            return False
        
        print(f"  ✓ Comparison verified ({len(companies)} companies)")
        return True
    
    def _build_verification_rules(self) -> Dict[str, Any]:
        """Build verification rules for different data types"""
        return {
            "income_statement": {
                "required_fields": ["ticker", "period", "data", "summary"],
                "required_summary": ["latest_revenue"]
            },
            "balance_sheet": {
                "required_fields": ["ticker", "period", "data", "summary"],
                "required_summary": ["latest_total_assets"]
            },
            "cash_flow": {
                "required_fields": ["ticker", "period", "data", "summary"],
                "required_summary": ["latest_operating_cash_flow"]
            }
        }


class DataQualityChecker:
    """
    Additional quality checks for financial data
    """
    
    def check_data_freshness(self, result: Dict[str, Any], max_age_days: int = 365) -> bool:
        """Check if data is recent enough"""
        from datetime import datetime, timedelta
        
        if "fetched_at" not in result:
            return True  # No timestamp, can't check
        
        try:
            fetched_time = datetime.fromisoformat(result["fetched_at"])
            age = datetime.now() - fetched_time
            
            if age.days > max_age_days:
                print(f"  ⚠ Data is {age.days} days old")
                return False
            
            return True
        except:
            return True
    
    def check_completeness(self, result: Dict[str, Any], expected_fields: list) -> bool:
        """Check if all expected fields are present"""
        missing = [field for field in expected_fields if field not in result]
        
        if missing:
            print(f"  ⚠ Missing fields: {', '.join(missing)}")
            return False
        
        return True
    
    def check_consistency(self, results: list) -> bool:
        """Check consistency across multiple results"""
        if not results:
            return True
        
        # Check all results are for the same period
        periods = set(r.get("period") for r in results if "period" in r)
        if len(periods) > 1:
            print(f"  ⚠ Inconsistent periods: {periods}")
            return False
        
        return True


if __name__ == "__main__":
    # Test verification
    from financial_agent import ResearchStep, TaskStatus
    
    verifier = ResultVerifier()
    
    # Test with sample result
    test_step = ResearchStep(
        step_id=1,
        description="Get income statement for AAPL",
        tool_name="get_income_statement",
        parameters={"ticker": "AAPL"},
        result={
            "ticker": "AAPL",
            "period": "annual",
            "data": {"Total Revenue": {"2023": 385000000000}},
            "summary": {"latest_revenue": 385000000000}
        }
    )
    
    print("Testing verification...")
    is_valid = verifier.verify_step(test_step)
    print(f"Result: {'Valid' if is_valid else 'Invalid'}")
