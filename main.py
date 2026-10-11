"""
Personal Financial Analyst - Main Entry Point

This is the main script to run the financial analyst agent.
It demonstrates autonomous execution with task planning, verification, and real-time data.
"""

import sys
from financial_agent import FinancialAgent
from financial_tools import register_tools


def print_banner():
    """Print welcome banner"""
    print("\n" + "="*80)
    print("  PERSONAL FINANCIAL ANALYST")
    print("  Intelligent Task Planning | Autonomous Execution | Self-Verification")
    print("="*80 + "\n")


def run_query(agent, query: str):
    """Run a financial query through the agent"""
    print(f"\n{'>'*80}")
    print(f"QUERY: {query}")
    print(f"{'>'*80}\n")
    
    try:
        # Plan the research
        plan = agent.plan_research(query)
        
        # Execute the plan
        results = agent.execute_plan(plan)
        
        # Display final answer
        print("\n" + "="*80)
        print("FINAL ANSWER")
        print("="*80)
        print(results["final_answer"])
        print("\n" + "="*80)
        print(f"Execution completed in {results['execution_time']:.2f}s")
        print(f"Total iterations: {results['iterations']}")
        print(f"Steps executed: {len(results['steps_executed'])}")
        print("="*80 + "\n")
        
        return results
        
    except Exception as e:
        print(f"\n✗ Error executing query: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def interactive_mode(agent):
    """Run in interactive mode"""
    print("\nInteractive Mode - Enter your financial queries")
    print("Type 'exit' or 'quit' to stop\n")
    
    while True:
        try:
            query = input("\n💰 Your query: ").strip()
            
            if not query:
                continue
            
            if query.lower() in ['exit', 'quit', 'q']:
                print("\nGoodbye! 👋\n")
                break
            
            run_query(agent, query)
            
        except KeyboardInterrupt:
            print("\n\nInterrupted by user. Goodbye! 👋\n")
            break
        except Exception as e:
            print(f"\n✗ Error: {str(e)}\n")


def run_examples(agent):
    """Run example queries"""
    examples = [
        "Compare AAPL and MSFT revenue",
        "What is TSLA's profitability?",
        "Calculate financial ratios for GOOGL",
        "Analyze AMZN's cash position",
        "How is NVDA valued?"
    ]
    
    print("\n" + "="*80)
    print("RUNNING EXAMPLE QUERIES")
    print("="*80 + "\n")
    
    for i, query in enumerate(examples, 1):
        print(f"\n[Example {i}/{len(examples)}]")
        run_query(agent, query)
        
        # Add delay between queries
        if i < len(examples):
            import time
            print("\nWaiting 2 seconds before next query...")
            time.sleep(2)


def main():
    """Main entry point"""
    print_banner()
    
    # Initialize agent
    print("Initializing Financial Agent...")
    agent = FinancialAgent(max_steps=50, max_iterations=10)
    
    # Register financial tools
    print("Registering financial data tools...")
    register_tools(agent)
    
    print(f"✓ Agent ready with {len(agent.tools)} tools available\n")
    print(f"  Tools: {', '.join(agent.tools.keys())}")
    
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--examples":
            run_examples(agent)
        elif sys.argv[1] == "--query":
            if len(sys.argv) > 2:
                query = " ".join(sys.argv[2:])
                run_query(agent, query)
            else:
                print("Error: --query requires a query string")
                sys.exit(1)
        elif sys.argv[1] in ["--help", "-h"]:
            print("\nUsage:")
            print("  python main.py                    # Interactive mode")
            print("  python main.py --examples         # Run example queries")
            print("  python main.py --query <query>    # Run a single query")
            print("  python main.py --help             # Show this help")
            print()
        else:
            # Treat all arguments as a query
            query = " ".join(sys.argv[1:])
            run_query(agent, query)
    else:
        # Interactive mode
        interactive_mode(agent)


if __name__ == "__main__":
    main()
