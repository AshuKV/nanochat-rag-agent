#!/usr/bin/env python3
"""Examples of programmatic usage of the Pharma Database API."""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.query_engine import QueryEngine
from config.config import Config
import json


def basic_usage():
    """Basic usage example."""
    print("=" * 60)
    print("EXAMPLE 1: Basic Usage")
    print("=" * 60)
    
    # Initialize query engine
    engine = QueryEngine()
    
    # Ask a question
    result = engine.query("How many products are in the database?")
    
    # Access results
    print(f"Query: {result['query']}")
    print(f"Success: {result['success']}")
    print(f"Response: {result['response']}")
    print(f"Result Count: {result['result_count']}")
    print()


def advanced_usage():
    """Advanced usage with options."""
    print("=" * 60)
    print("EXAMPLE 2: Advanced Usage")
    print("=" * 60)
    
    engine = QueryEngine()
    
    # Query with options
    result = engine.query(
        "Find products for diabetes",
        return_sql=True,          # Include SQL in response
        natural_response=True     # Generate natural language response
    )
    
    if result['success']:
        print(f"Generated SQL: {result['sql']}")
        print(f"Found {result['result_count']} results")
        print(f"\nNatural Response:\n{result['response']}")
        
        # Access raw data
        print(f"\nRaw Results (first 2):")
        for item in result['raw_results'][:2]:
            print(f"  - {item.get('product_name', 'Unknown')}")
    else:
        print(f"Error: {result['error']}")
    print()


def batch_queries():
    """Process multiple queries in batch."""
    print("=" * 60)
    print("EXAMPLE 3: Batch Queries")
    print("=" * 60)
    
    engine = QueryEngine()
    
    queries = [
        "How many products are there?",
        "Find products for pain relief",
        "List antibiotics",
        "What are side effects of Dolo 650?"
    ]
    
    results = []
    for query in queries:
        result = engine.query(query, natural_response=False)
        results.append({
            'query': query,
            'count': result['result_count'],
            'success': result['success']
        })
    
    print("Batch Results:")
    for r in results:
        status = "✓" if r['success'] else "✗"
        print(f"  {status} {r['query']}: {r['count']} results")
    print()


def export_to_json():
    """Export query results to JSON."""
    print("=" * 60)
    print("EXAMPLE 4: Export Results to JSON")
    print("=" * 60)
    
    engine = QueryEngine()
    
    result = engine.query("Find products for diabetes")
    
    if result['success']:
        # Export to JSON file
        output_file = "diabetes_products.json"
        with open(output_file, 'w') as f:
            json.dump(result['raw_results'], f, indent=2)
        
        print(f"✓ Exported {result['result_count']} products to {output_file}")
    print()


def custom_response_format():
    """Custom formatting of results."""
    print("=" * 60)
    print("EXAMPLE 5: Custom Response Formatting")
    print("=" * 60)
    
    engine = QueryEngine()
    
    result = engine.query("Find products for heart conditions")
    
    if result['success']:
        # Custom formatting
        print(f"Found {result['result_count']} products:\n")
        
        for idx, product in enumerate(result['raw_results'][:5], 1):
            print(f"{idx}. {product.get('product_name', 'Unknown')}")
            uses = product.get('uses', 'N/A')
            print(f"   Uses: {uses[:100]}...")
            print()
    print()


def error_handling():
    """Demonstrate error handling."""
    print("=" * 60)
    print("EXAMPLE 6: Error Handling")
    print("=" * 60)
    
    engine = QueryEngine()
    
    # Intentionally vague query that might fail
    result = engine.query("xyzabc123")
    
    if result['success']:
        print(f"Success: {result['response']}")
    else:
        print(f"Error occurred: {result['error']}")
        print(f"Fallback response: {result['response']}")
    print()


def accessing_metadata():
    """Access query metadata."""
    print("=" * 60)
    print("EXAMPLE 7: Accessing Metadata")
    print("=" * 60)
    
    engine = QueryEngine()
    
    result = engine.query("How many products contain aspirin?")
    
    # Access all metadata
    print(f"Timestamp: {result['timestamp']}")
    print(f"Original Query: {result['query']}")
    print(f"Success: {result['success']}")
    print(f"SQL: {result.get('sql', 'N/A')}")
    print(f"Result Count: {result['result_count']}")
    print(f"Has Error: {result['error'] is not None}")
    print()


def use_suggestions():
    """Get and use query suggestions."""
    print("=" * 60)
    print("EXAMPLE 8: Using Suggestions")
    print("=" * 60)
    
    engine = QueryEngine()
    
    # Get suggestions
    suggestions = engine.get_suggestions()
    
    print("Available suggestions:")
    for idx, suggestion in enumerate(suggestions[:5], 1):
        print(f"  {idx}. {suggestion}")
    
    # Use first suggestion
    print(f"\nTrying suggestion: {suggestions[0]}")
    result = engine.query(suggestions[0])
    print(f"Result: {result['response'][:100]}...")
    print()


def main():
    """Run all examples."""
    try:
        Config.validate()
        
        print("\n" + "=" * 60)
        print("PHARMA DATABASE - PROGRAMMATIC USAGE EXAMPLES")
        print("=" * 60 + "\n")
        
        basic_usage()
        advanced_usage()
        batch_queries()
        export_to_json()
        custom_response_format()
        error_handling()
        accessing_metadata()
        use_suggestions()
        
        print("=" * 60)
        print("✓ All examples completed!")
        print("=" * 60)
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure you have:")
        print("1. Run 'python setup.py' to create the database")
        print("2. Set up your .env file with API keys")


if __name__ == "__main__":
    main()

