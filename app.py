"""
Flask Web Application for Personal Financial Analyst
Provides REST API endpoints for financial analysis
"""

from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import os
import json
import time
from datetime import datetime

from financial_agent import FinancialAgent
from financial_tools import register_tools

# Initialize Flask app
app = Flask(__name__, 
            static_folder='static',
            template_folder='templates')

# Enable CORS for API calls
CORS(app)

# Initialize the Financial Agent
agent = FinancialAgent(max_steps=50, max_iterations=10)
register_tools(agent)

# Store query history (in-memory, would use database in production)
query_history = []


@app.route('/')
def index():
    """Serve the main web interface"""
    return render_template('index.html')


@app.route('/api/analyze', methods=['POST'])
def analyze():
    """
    Main API endpoint for financial analysis
    
    Request JSON:
    {
        "query": "Compare AAPL and MSFT revenue"
    }
    
    Response JSON:
    {
        "success": true,
        "query": "...",
        "steps": [...],
        "answer": "...",
        "execution_time": 3.45,
        "timestamp": "..."
    }
    """
    try:
        # Get query from request
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({
                'success': False,
                'error': '請提供查詢內容'
            }), 400
        
        query = data['query'].strip()
        
        if not query:
            return jsonify({
                'success': False,
                'error': '查詢內容不能為空'
            }), 400
        
        # Log the query
        print(f"\n[API] Received query: {query}")
        
        start_time = time.time()
        
        # Plan and execute
        plan = agent.plan_research(query)
        results = agent.execute_plan(plan)
        
        execution_time = time.time() - start_time
        
        # Format response
        response = {
            'success': True,
            'query': query,
            'steps': [
                {
                    'step_id': step['step_id'],
                    'description': step['description'],
                    'status': step['status']
                }
                for step in results['steps_executed']
            ],
            'answer': results['final_answer'],
            'execution_time': round(execution_time, 2),
            'iterations': results.get('iterations', 1),
            'timestamp': datetime.now().isoformat()
        }
        
        # Add to history
        query_history.append({
            'query': query,
            'timestamp': datetime.now().isoformat(),
            'execution_time': execution_time
        })
        
        # Keep only last 100 queries
        if len(query_history) > 100:
            query_history.pop(0)
        
        return jsonify(response)
        
    except Exception as e:
        print(f"[API] Error: {str(e)}")
        import traceback
        traceback.print_exc()
        
        return jsonify({
            'success': False,
            'error': f'分析過程發生錯誤: {str(e)}'
        }), 500


@app.route('/api/examples', methods=['GET'])
def get_examples():
    """Get example queries"""
    examples = [
        {
            'category': '公司比較',
            'queries': [
                'Compare AAPL and MSFT revenue',
                'GOOGL vs META market cap',
                'Which is more profitable: TSLA or FORD?'
            ]
        },
        {
            'category': '財務分析',
            'queries': [
                'What is AAPL\'s profitability?',
                'Analyze MSFT financials',
                'Show me GOOGL\'s financial ratios'
            ]
        },
        {
            'category': '現金流分析',
            'queries': [
                'What is AMZN\'s cash position?',
                'Analyze AAPL\'s cash flow',
                'Show TSLA free cash flow'
            ]
        },
        {
            'category': '估值分析',
            'queries': [
                'How is NVDA valued?',
                'What is META\'s P/E ratio?',
                'Show AAPL valuation metrics'
            ]
        }
    ]
    
    return jsonify({
        'success': True,
        'examples': examples
    })


@app.route('/api/history', methods=['GET'])
def get_history():
    """Get query history"""
    return jsonify({
        'success': True,
        'history': list(reversed(query_history[-20:]))  # Last 20 queries
    })


@app.route('/api/status', methods=['GET'])
def get_status():
    """Get system status"""
    return jsonify({
        'success': True,
        'status': 'online',
        'version': '1.0.0',
        'tools_count': len(agent.tools),
        'tools': list(agent.tools.keys()),
        'queries_processed': len(query_history),
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/tools', methods=['GET'])
def get_tools():
    """Get available tools"""
    tool_descriptions = {
        'get_income_statement': '獲取損益表數據',
        'get_balance_sheet': '獲取資產負債表數據',
        'get_cash_flow': '獲取現金流量表數據',
        'get_stock_info': '獲取股票基本信息',
        'calculate_financial_ratios': '計算財務比率',
        'compare_companies': '比較多家公司'
    }
    
    tools = [
        {
            'name': name,
            'description': tool_descriptions.get(name, '財務分析工具')
        }
        for name in agent.tools.keys()
    ]
    
    return jsonify({
        'success': True,
        'tools': tools
    })


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })


@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': '找不到請求的資源'
    }), 404


@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'error': '伺服器內部錯誤'
    }), 500


if __name__ == '__main__':
    # Create templates and static directories if they don't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    
    print("\n" + "="*80)
    print("  Personal Financial Analyst - Web Application")
    print("="*80)
    print(f"\n✓ Agent initialized with {len(agent.tools)} tools")
    print(f"✓ Server starting...")
    print(f"\n📊 Access the application at: http://localhost:5000")
    print("="*80 + "\n")
    
    # Run the Flask app
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
