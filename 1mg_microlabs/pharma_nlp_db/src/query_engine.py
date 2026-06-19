"""Query Execution Engine and Response Generator."""

import json
import sqlite3
import os
import sys
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import Config
from src.llm_client import get_llm_client
from src.nl_to_sql import NLToSQLConverter


class QueryEngine:
    """Executes SQL queries and generates human-readable responses."""
    
    def __init__(self):
        """Initialize Query Engine."""
        self.db_path = Config.DB_PATH
        self.table_name = Config.TABLE_NAME
        self.llm_client = get_llm_client()
        self.nl_to_sql = NLToSQLConverter()
    
    def execute_sql(self, sql_query: str) -> Tuple[List[Dict[str, Any]], Optional[str]]:
        """Execute SQL query and return results.
        
        Args:
            sql_query: SQL query to execute
            
        Returns:
            Tuple of (results as list of dicts, error message if any)
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # Enable column access by name
            cursor = conn.cursor()
            
            cursor.execute(sql_query)
            rows = cursor.fetchall()
            
            # Convert to list of dictionaries
            results = [dict(row) for row in rows]
            
            conn.close()
            
            return results, None
        
        except Exception as e:
            return [], f"SQL Error: {str(e)}"
    
    def format_results_as_text(self, results: List[Dict[str, Any]]) -> str:
        """Format query results as readable text.
        
        Args:
            results: Query results as list of dictionaries
            
        Returns:
            Formatted text string
        """
        if not results:
            return "No results found."
        
        # If single value (like COUNT), return it directly
        if len(results) == 1 and len(results[0]) == 1:
            key = list(results[0].keys())[0]
            value = results[0][key]
            return f"{key}: {value}"
        
        # Format multiple results
        output = []
        for idx, row in enumerate(results, 1):
            output.append(f"\nResult {idx}:")
            for key, value in row.items():
                # Handle JSON fields
                if key in ['fact_box', 'safety_advice', 'full_data'] and value:
                    try:
                        json_obj = json.loads(value) if isinstance(value, str) else value
                        value = json.dumps(json_obj, indent=2)
                    except:
                        pass
                
                # Truncate very long values
                value_str = str(value)
                if len(value_str) > 500:
                    value_str = value_str[:500] + "..."
                
                output.append(f"  {key}: {value_str}")
        
        return "\n".join(output)
    
    def generate_natural_response(
        self, 
        user_query: str, 
        sql_query: str, 
        results: List[Dict[str, Any]]
    ) -> str:
        """Generate a natural language response from query results.
        
        Args:
            user_query: Original user question
            sql_query: SQL query that was executed
            results: Query results
            
        Returns:
            Natural language response
        """
        system_prompt = """You are a helpful pharmaceutical information assistant.
Generate a clear, natural language response based on the query results.

Guidelines:
- Be concise but informative
- Use bullet points for lists
- Highlight important information like warnings and side effects
- If no results, say so politely
- Don't mention SQL or technical details
- Focus on answering the user's question directly"""

        # Prepare results summary for LLM (limit size)
        results_summary = results[:10] if len(results) > 10 else results
        
        # Remove very large fields
        cleaned_results = []
        for result in results_summary:
            cleaned = {k: v for k, v in result.items() if k not in ['full_data']}
            cleaned_results.append(cleaned)
        
        user_prompt = f"""User Question: {user_query}

Query Results ({len(results)} total):
{json.dumps(cleaned_results, indent=2)}

Generate a natural, helpful response:"""

        try:
            response = self.llm_client.get_completion(
                prompt=user_prompt,
                system_prompt=system_prompt,
                temperature=0.5,
                max_tokens=800
            )
            return response.strip()
        
        except Exception as e:
            # Fallback to simple formatting if LLM fails
            return f"Found {len(results)} result(s):\n" + self.format_results_as_text(results)
    
    def query(
        self, 
        natural_query: str, 
        return_sql: bool = False,
        natural_response: bool = True
    ) -> Dict[str, Any]:
        """Process a natural language query end-to-end.
        
        Args:
            natural_query: User's natural language question
            return_sql: Whether to include SQL in response
            natural_response: Whether to generate natural language response
            
        Returns:
            Dictionary with query results and metadata
        """
        result = {
            "query": natural_query,
            "timestamp": datetime.now().isoformat(),
            "success": False,
            "sql": None,
            "raw_results": [],
            "result_count": 0,
            "response": None,
            "error": None
        }
        
        try:
            # Convert to SQL
            sql = self.nl_to_sql.convert_to_sql(natural_query)
            
            if not sql:
                result["error"] = "Could not generate SQL query from your question."
                result["response"] = "I'm sorry, I couldn't understand your question. Please try rephrasing it."
                return result
            
            result["sql"] = sql
            
            # Execute SQL
            raw_results, error = self.execute_sql(sql)
            
            if error:
                result["error"] = error
                result["response"] = f"An error occurred while executing the query: {error}"
                return result
            
            result["raw_results"] = raw_results
            result["result_count"] = len(raw_results)
            result["success"] = True
            
            # Generate response
            if natural_response:
                result["response"] = self.generate_natural_response(
                    natural_query, sql, raw_results
                )
            else:
                result["response"] = self.format_results_as_text(raw_results)
        
        except Exception as e:
            result["error"] = str(e)
            result["response"] = f"An unexpected error occurred: {str(e)}"
        
        return result
    
    def get_suggestions(self) -> List[str]:
        """Get example queries users can try.
        
        Returns:
            List of example query strings
        """
        return [
            "How many products are in the database?",
            "Find products for glaucoma",
            "What are the side effects of Dolo 650?",
            "List all products containing paracetamol",
            "Show me products that are unsafe during pregnancy",
            "What products are used for heart conditions?",
            "Find all antibiotic products",
            "Which products cause drowsiness?",
            "List products for pain relief",
            "What are the uses of Azithromycin?"
        ]


def main():
    """Main function for testing."""
    try:
        Config.validate()
        
        engine = QueryEngine()
        
        print("=" * 60)
        print("PHARMA DATABASE QUERY ENGINE - TEST")
        print("=" * 60)
        
        # Show suggestions
        print("\nExample queries:")
        for idx, suggestion in enumerate(engine.get_suggestions()[:5], 1):
            print(f"{idx}. {suggestion}")
        
        # Test queries
        test_queries = [
            "How many products are there?",
            "Find products for glaucoma"
        ]
        
        for query in test_queries:
            print("\n" + "=" * 60)
            print(f"Query: {query}")
            print("-" * 60)
            
            result = engine.query(query, return_sql=True, natural_response=True)
            
            if result["success"]:
                print(f"\n✓ SQL: {result['sql']}")
                print(f"✓ Found: {result['result_count']} result(s)")
                print(f"\nResponse:\n{result['response']}")
            else:
                print(f"\n✗ Error: {result['error']}")
                print(f"Response: {result['response']}")
        
        print("\n" + "=" * 60)
    
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()

