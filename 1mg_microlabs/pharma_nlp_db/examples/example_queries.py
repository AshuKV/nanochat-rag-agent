#!/usr/bin/env python3
"""Example queries demonstrating the system's capabilities."""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.query_engine import QueryEngine
from config.config import Config
import json


def run_example_queries():
    """Run a series of example queries."""
    
    print("=" * 70)
    print("PHARMA DATABASE - EXAMPLE QUERIES DEMONSTRATION")
    print("=" * 70)
    
    # Initialize engine
    try:
        Config.validate()
        engine = QueryEngine()
    except Exception as e:
        print(f"Error initializing: {e}")
        print("\nPlease ensure:")
        print("1. You have run 'python setup.py' to create the database")
        print("2. Your .env file has correct API keys")
        return
    
    # Example queries
    examples = [
        {
            "category": "Simple Count",
            "query": "How many products are in the database?",
            "description": "Get total product count"
        },
        {
            "category": "Product Search",
            "query": "Find products for glaucoma",
            "description": "Search by medical condition"
        },
        {
            "category": "Specific Product",
            "query": "What are the side effects of Dolo 650?",
            "description": "Get details about a specific product"
        },
        {
            "category": "Ingredient Search",
            "query": "List products containing aspirin",
            "description": "Search by ingredient"
        },
        {
            "category": "Safety Query",
            "query": "Which products are unsafe during pregnancy?",
            "description": "Safety-related information"
        },
        {
            "category": "Therapeutic Search",
            "query": "Show me products for heart conditions",
            "description": "Search by therapeutic area"
        },
        {
            "category": "Side Effect Query",
            "query": "What products may cause drowsiness?",
            "description": "Search by side effects"
        }
    ]
    
    results_summary = []
    
    for idx, example in enumerate(examples, 1):
        print(f"\n{'='*70}")
        print(f"EXAMPLE {idx}: {example['category']}")
        print(f"{'='*70}")
        print(f"Description: {example['description']}")
        print(f"Query: \"{example['query']}\"")
        print(f"{'-'*70}")
        
        # Execute query
        result = engine.query(
            example['query'],
            return_sql=True,
            natural_response=True
        )
        
        if result['success']:
            print(f"\n✓ Success!")
            print(f"SQL Generated: {result['sql']}")
            print(f"Results Found: {result['result_count']}")
            print(f"\nNatural Language Response:")
            print(f"{'-'*70}")
            print(result['response'])
            
            results_summary.append({
                "query": example['query'],
                "success": True,
                "count": result['result_count']
            })
        else:
            print(f"\n✗ Failed")
            print(f"Error: {result['error']}")
            print(f"Response: {result['response']}")
            
            results_summary.append({
                "query": example['query'],
                "success": False,
                "error": result['error']
            })
    
    # Summary
    print(f"\n{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}")
    
    successful = sum(1 for r in results_summary if r['success'])
    total = len(results_summary)
    
    print(f"\nTotal Queries: {total}")
    print(f"Successful: {successful}")
    print(f"Failed: {total - successful}")
    
    if successful == total:
        print("\n🎉 All example queries executed successfully!")
    else:
        print(f"\n⚠️  {total - successful} queries failed. Check errors above.")
    
    print(f"\n{'='*70}\n")


def export_example_results():
    """Export example query results to JSON."""
    engine = QueryEngine()
    
    queries = [
        "How many products are there?",
        "Find products for diabetes",
        "What are the uses of Dolo 650?"
    ]
    
    all_results = []
    
    for query in queries:
        result = engine.query(query, return_sql=True, natural_response=True)
        all_results.append(result)
    
    # Export to JSON
    output_file = "example_results.json"
    with open(output_file, 'w') as f:
        json.dump(all_results, f, indent=2)
    
    print(f"✓ Exported results to {output_file}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Run example queries")
    parser.add_argument(
        "--export",
        action="store_true",
        help="Export results to JSON file"
    )
    
    args = parser.parse_args()
    
    if args.export:
        export_example_results()
    else:
        run_example_queries()

