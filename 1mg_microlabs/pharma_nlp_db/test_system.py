#!/usr/bin/env python3
"""Quick test script to verify the system is working."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.config import Config
from src.llm_client import get_llm_client
from src.query_engine import QueryEngine


def test_config():
    """Test configuration."""
    print("Testing configuration...")
    try:
        Config.validate()
        print("✓ Configuration valid")
        print(f"  - Provider: {Config.LLM_PROVIDER}")
        print(f"  - Database: {Config.DB_PATH}")
        print(f"  - JSON Data: {Config.JSON_DATA_PATH}")
        return True
    except Exception as e:
        print(f"✗ Configuration error: {e}")
        return False


def test_llm():
    """Test LLM connection."""
    print("\nTesting LLM connection...")
    try:
        client = get_llm_client()
        response = client.get_completion("Say 'Hello'", temperature=0.3, max_tokens=10)
        print(f"✓ LLM connection working")
        print(f"  - Provider: {client.provider}")
        print(f"  - Model: {client.model}")
        print(f"  - Test response: {response[:50]}")
        return True
    except Exception as e:
        print(f"✗ LLM connection error: {e}")
        return False


def test_database():
    """Test database."""
    print("\nTesting database...")
    try:
        if not Config.DB_PATH.exists():
            print("✗ Database not found!")
            print("  Run: python setup.py")
            return False
        
        from src.data_loader import DataLoader
        loader = DataLoader()
        count = loader.get_record_count()
        print(f"✓ Database accessible")
        print(f"  - Records: {count}")
        return True
    except Exception as e:
        print(f"✗ Database error: {e}")
        return False


def test_query():
    """Test query execution."""
    print("\nTesting query engine...")
    try:
        engine = QueryEngine()
        result = engine.query("How many products are there?", natural_response=False)
        
        if result['success']:
            print("✓ Query engine working")
            print(f"  - SQL: {result['sql']}")
            print(f"  - Results: {result['result_count']}")
            return True
        else:
            print(f"✗ Query failed: {result.get('error', 'Unknown error')}")
            return False
    except Exception as e:
        print(f"✗ Query engine error: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("PHARMA DATABASE SYSTEM - QUICK TEST")
    print("=" * 60)
    
    results = []
    
    results.append(("Configuration", test_config()))
    results.append(("LLM Connection", test_llm()))
    results.append(("Database", test_database()))
    results.append(("Query Engine", test_query()))
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    for name, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status:8} - {name}")
    
    all_passed = all(result[1] for result in results)
    
    if all_passed:
        print("\n🎉 All tests passed! System is ready.")
        print("\nNext steps:")
        print("  - Run CLI: python cli.py")
        print("  - Run GUI: streamlit run app.py")
    else:
        print("\n⚠️  Some tests failed. Please check errors above.")
        print("\nCommon fixes:")
        print("  - Run setup: python setup.py")
        print("  - Check .env file has correct API keys")
        print("  - Verify dependencies: pip install -r requirements.txt")
    
    print("=" * 60)


if __name__ == "__main__":
    main()

