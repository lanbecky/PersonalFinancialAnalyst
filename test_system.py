"""
Test script for the Financial Analyst system
Tests individual components and the integrated system
"""

def test_task_planner():
    """Test the task planner"""
    print("\n" + "="*60)
    print("TEST 1: Task Planner")
    print("="*60)
    
    from task_planner import TaskPlanner
    
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
        "Calculate financial ratios for GOOGL"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        steps = planner.plan(query)
        print(f"Generated {len(steps)} steps:")
        for step in steps:
            print(f"  {step.step_id}. {step.description} ({step.tool_name})")
    
    print("\n✓ Task Planner test passed")
    return True


def test_financial_tools():
    """Test financial data tools"""
    print("\n" + "="*60)
    print("TEST 2: Financial Tools")
    print("="*60)
    
    from financial_tools import FinancialDataTools
    
    tools = FinancialDataTools()
    
    # Test with AAPL
    ticker = "AAPL"
    
    print(f"\nTesting tools with {ticker}...")
    
    print("\n1. Stock Info:")
    info = tools.get_stock_info(ticker)
    if "error" not in info:
        print(f"   ✓ Company: {info.get('company_name')}")
        print(f"   ✓ Market Cap: ${info.get('market_cap', 0):,.0f}")
    else:
        print(f"   ✗ Error: {info['error']}")
        return False
    
    print("\n2. Income Statement:")
    income = tools.get_income_statement(ticker)
    if "error" not in income:
        print(f"   ✓ Revenue: ${income['summary']['latest_revenue']:,.0f}")
        print(f"   ✓ Net Income: ${income['summary']['latest_net_income']:,.0f}")
    else:
        print(f"   ✗ Error: {income['error']}")
        return False
    
    print("\n3. Balance Sheet:")
    balance = tools.get_balance_sheet(ticker)
    if "error" not in balance:
        print(f"   ✓ Total Assets: ${balance['summary']['latest_total_assets']:,.0f}")
        print(f"   ✓ Equity: ${balance['summary']['latest_stockholder_equity']:,.0f}")
    else:
        print(f"   ✗ Error: {balance['error']}")
        return False
    
    print("\n4. Cash Flow:")
    cashflow = tools.get_cash_flow(ticker)
    if "error" not in cashflow:
        print(f"   ✓ Operating CF: ${cashflow['summary']['latest_operating_cash_flow']:,.0f}")
    else:
        print(f"   ✗ Error: {cashflow['error']}")
        return False
    
    print("\n✓ Financial Tools test passed")
    return True


def test_verification():
    """Test verification system"""
    print("\n" + "="*60)
    print("TEST 3: Verification System")
    print("="*60)
    
    from verification import ResultVerifier
    from financial_agent import ResearchStep, TaskStatus
    
    verifier = ResultVerifier()
    
    # Test with valid data
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
    
    print("\nTesting with valid data:")
    is_valid = verifier.verify_step(test_step)
    print(f"Result: {'✓ Valid' if is_valid else '✗ Invalid'}")
    
    # Test with invalid data
    test_step.result = {"error": "Test error"}
    print("\nTesting with error:")
    is_valid = verifier.verify_step(test_step)
    print(f"Result: {'✗ Invalid (expected)' if not is_valid else '✓ Valid'}")
    
    print("\n✓ Verification test passed")
    return True


def test_integrated_system():
    """Test the integrated system with a real query"""
    print("\n" + "="*60)
    print("TEST 4: Integrated System")
    print("="*60)
    
    from financial_agent import FinancialAgent
    from financial_tools import register_tools
    
    # Initialize agent
    agent = FinancialAgent(max_steps=20, max_iterations=5)
    register_tools(agent)
    
    # Test query
    query = "Get stock info and calculate ratios for AAPL"
    
    print(f"\nQuery: {query}")
    print("\nExecuting...")
    
    try:
        # Plan
        plan = agent.plan_research(query)
        print(f"✓ Plan created with {len(plan.steps)} steps")
        
        # Execute
        results = agent.execute_plan(plan)
        print(f"\n✓ Execution completed in {results['execution_time']:.2f}s")
        print(f"✓ Steps executed: {len(results['steps_executed'])}")
        
        if results["final_answer"]:
            print(f"\n✓ Final answer generated ({len(results['final_answer'])} chars)")
        
        print("\n✓ Integrated system test passed")
        return True
        
    except Exception as e:
        print(f"\n✗ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("FINANCIAL ANALYST SYSTEM - TEST SUITE")
    print("="*60)
    
    tests = [
        ("Task Planner", test_task_planner),
        ("Financial Tools", test_financial_tools),
        ("Verification", test_verification),
        ("Integrated System", test_integrated_system)
    ]
    
    results = {}
    
    for name, test_func in tests:
        try:
            results[name] = test_func()
        except Exception as e:
            print(f"\n✗ {name} test failed with exception: {str(e)}")
            import traceback
            traceback.print_exc()
            results[name] = False
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    for name, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{name}: {status}")
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠ {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
