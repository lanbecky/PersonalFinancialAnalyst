"""
Advanced Examples for the Financial Analyst

This file demonstrates advanced usage patterns and complex queries.
"""

from financial_agent import FinancialAgent
from financial_tools import register_tools


def example_multi_company_comparison():
    """Compare multiple companies across different metrics"""
    print("\n" + "="*80)
    print("EXAMPLE 1: Multi-Company Comparison")
    print("="*80 + "\n")
    
    agent = FinancialAgent(max_steps=50, max_iterations=10)
    register_tools(agent)
    
    query = "Compare AAPL, MSFT, GOOGL, and AMZN on market cap"
    
    plan = agent.plan_research(query)
    results = agent.execute_plan(plan)
    
    print("\n" + results["final_answer"])


def example_comprehensive_analysis():
    """Perform comprehensive financial analysis"""
    print("\n" + "="*80)
    print("EXAMPLE 2: Comprehensive Financial Analysis")
    print("="*80 + "\n")
    
    agent = FinancialAgent(max_steps=50, max_iterations=10)
    register_tools(agent)
    
    query = "Perform complete financial analysis of TSLA including income, balance sheet, cash flow, and ratios"
    
    plan = agent.plan_research(query)
    results = agent.execute_plan(plan)
    
    print("\n" + results["final_answer"])


def example_profitability_comparison():
    """Compare profitability metrics"""
    print("\n" + "="*80)
    print("EXAMPLE 3: Profitability Comparison")
    print("="*80 + "\n")
    
    agent = FinancialAgent(max_steps=50, max_iterations=10)
    register_tools(agent)
    
    query = "Compare profitability ratios of META and SNAP"
    
    plan = agent.plan_research(query)
    results = agent.execute_plan(plan)
    
    print("\n" + results["final_answer"])


def example_cash_flow_analysis():
    """Analyze cash flow in depth"""
    print("\n" + "="*80)
    print("EXAMPLE 4: Cash Flow Analysis")
    print("="*80 + "\n")
    
    agent = FinancialAgent(max_steps=50, max_iterations=10)
    register_tools(agent)
    
    query = "Analyze NVDA's cash flow and liquidity position"
    
    plan = agent.plan_research(query)
    results = agent.execute_plan(plan)
    
    print("\n" + results["final_answer"])


def example_valuation_multiple_companies():
    """Compare valuations of multiple companies"""
    print("\n" + "="*80)
    print("EXAMPLE 5: Valuation Comparison")
    print("="*80 + "\n")
    
    agent = FinancialAgent(max_steps=50, max_iterations=10)
    register_tools(agent)
    
    query = "How are NVDA, AMD, and INTC valued? Compare their P/E ratios"
    
    plan = agent.plan_research(query)
    results = agent.execute_plan(plan)
    
    print("\n" + results["final_answer"])


def example_sector_analysis():
    """Analyze companies in the same sector"""
    print("\n" + "="*80)
    print("EXAMPLE 6: Sector Analysis (Tech Giants)")
    print("="*80 + "\n")
    
    agent = FinancialAgent(max_steps=50, max_iterations=10)
    register_tools(agent)
    
    query = "Compare revenue and profitability of tech giants: AAPL, MSFT, GOOGL, META, AMZN"
    
    plan = agent.plan_research(query)
    results = agent.execute_plan(plan)
    
    print("\n" + results["final_answer"])


def example_custom_analysis_workflow():
    """Demonstrate custom analysis workflow"""
    print("\n" + "="*80)
    print("EXAMPLE 7: Custom Analysis Workflow")
    print("="*80 + "\n")
    
    agent = FinancialAgent(max_steps=50, max_iterations=10)
    register_tools(agent)
    
    # Step 1: Get basic info
    query1 = "Get stock info for AAPL"
    plan1 = agent.plan_research(query1)
    results1 = agent.execute_plan(plan1)
    
    # Step 2: Deep dive into financials
    query2 = "Calculate all financial ratios for AAPL"
    plan2 = agent.plan_research(query2)
    results2 = agent.execute_plan(plan2)
    
    # Step 3: Compare with competitor
    query3 = "Compare AAPL and MSFT on profitability"
    plan3 = agent.plan_research(query3)
    results3 = agent.execute_plan(plan3)
    
    print("\nWorkflow completed successfully!")


def example_with_error_handling():
    """Demonstrate error handling and recovery"""
    print("\n" + "="*80)
    print("EXAMPLE 8: Error Handling")
    print("="*80 + "\n")
    
    agent = FinancialAgent(max_steps=50, max_iterations=10)
    register_tools(agent)
    
    # Try with an invalid ticker
    query = "Analyze INVALIDTICKER"
    
    try:
        plan = agent.plan_research(query)
        results = agent.execute_plan(plan)
        
        if results["final_answer"]:
            print("\n" + results["final_answer"])
        else:
            print("\nNo results generated (expected for invalid ticker)")
            
    except Exception as e:
        print(f"\nHandled error: {str(e)}")


def example_performance_tracking():
    """Track performance metrics of the agent"""
    print("\n" + "="*80)
    print("EXAMPLE 9: Performance Tracking")
    print("="*80 + "\n")
    
    agent = FinancialAgent(max_steps=50, max_iterations=10)
    register_tools(agent)
    
    queries = [
        "Get stock info for AAPL",
        "Calculate ratios for MSFT",
        "Compare GOOGL and META"
    ]
    
    performance_stats = []
    
    for query in queries:
        plan = agent.plan_research(query)
        results = agent.execute_plan(plan)
        
        performance_stats.append({
            "query": query,
            "steps": len(results["steps_executed"]),
            "time": results["execution_time"],
            "iterations": results["iterations"]
        })
    
    print("\nPerformance Summary:")
    print("-" * 80)
    for stat in performance_stats:
        print(f"Query: {stat['query']}")
        print(f"  Steps: {stat['steps']}, Time: {stat['time']:.2f}s, Iterations: {stat['iterations']}")


def main():
    """Run all advanced examples"""
    import sys
    
    examples = {
        "1": ("Multi-Company Comparison", example_multi_company_comparison),
        "2": ("Comprehensive Analysis", example_comprehensive_analysis),
        "3": ("Profitability Comparison", example_profitability_comparison),
        "4": ("Cash Flow Analysis", example_cash_flow_analysis),
        "5": ("Valuation Comparison", example_valuation_multiple_companies),
        "6": ("Sector Analysis", example_sector_analysis),
        "7": ("Custom Workflow", example_custom_analysis_workflow),
        "8": ("Error Handling", example_with_error_handling),
        "9": ("Performance Tracking", example_performance_tracking),
    }
    
    print("\n" + "="*80)
    print("ADVANCED EXAMPLES - PERSONAL FINANCIAL ANALYST")
    print("="*80 + "\n")
    
    if len(sys.argv) > 1:
        example_num = sys.argv[1]
        if example_num in examples:
            name, func = examples[example_num]
            print(f"Running Example {example_num}: {name}")
            func()
        elif example_num == "all":
            for num, (name, func) in examples.items():
                print(f"\nRunning Example {num}: {name}")
                func()
                print("\n" + "="*80)
        else:
            print(f"Invalid example number: {example_num}")
            print("\nAvailable examples:")
            for num, (name, _) in examples.items():
                print(f"  {num}: {name}")
            print("\nUsage: python examples_advanced.py [1-9|all]")
    else:
        print("Available examples:")
        for num, (name, _) in examples.items():
            print(f"  {num}: {name}")
        print("\nUsage:")
        print("  python examples_advanced.py <number>  # Run specific example")
        print("  python examples_advanced.py all       # Run all examples")


if __name__ == "__main__":
    main()
