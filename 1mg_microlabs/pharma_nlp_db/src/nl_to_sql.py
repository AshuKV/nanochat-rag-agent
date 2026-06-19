"""Natural Language to SQL Query Converter."""

import json
import re
import sqlite3
import os
import sys
from typing import Dict, Any, Optional, List

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import Config
from src.llm_client import get_llm_client


class NLToSQLConverter:
    """Converts natural language queries to SQL using LLM."""
    
    def __init__(self):
        """Initialize NL to SQL Converter."""
        self.llm_client = get_llm_client()
        self.db_path = Config.DB_PATH
        self.table_name = Config.TABLE_NAME
        self.schema_info = self._get_schema_info()
    
    def _get_schema_info(self) -> Dict[str, Any]:
        """Get database schema information.
        
        Returns:
            Dictionary with schema details
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get table info
            cursor.execute(f"PRAGMA table_info({self.table_name})")
            columns = cursor.fetchall()
            
            # Get sample data for context
            cursor.execute(f"SELECT * FROM {self.table_name} LIMIT 3")
            sample_rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            
            conn.close()
            
            return {
                "table_name": self.table_name,
                "columns": [
                    {
                        "name": col[1],
                        "type": col[2],
                        "nullable": not col[3],
                        "primary_key": bool(col[5])
                    }
                    for col in columns
                ],
                "column_names": column_names,
                "sample_data": [dict(zip(column_names, row)) for row in sample_rows]
            }
        
        except Exception as e:
            print(f"Warning: Could not get schema info: {e}")
            return {"table_name": self.table_name, "columns": [], "column_names": []}
    
    def _build_schema_description(self) -> str:
        """Build a human-readable schema description for LLM.
        
        Returns:
            Formatted schema description
        """
        description = f"Database: {Config.DB_NAME}\n"
        description += f"Table: {self.schema_info['table_name']}\n\n"
        description += "Columns:\n"
        
        for col in self.schema_info['columns']:
            pk = " [PRIMARY KEY]" if col['primary_key'] else ""
            description += f"  - {col['name']} ({col['type']}){pk}\n"
        
        # Add sample data for context
        if self.schema_info.get('sample_data'):
            description += "\nSample Records (for reference):\n"
            for idx, sample in enumerate(self.schema_info['sample_data'][:2], 1):
                description += f"\nRecord {idx}:\n"
                for key, value in sample.items():
                    if key not in ['full_data', 'fact_box', 'safety_advice']:  # Skip large fields
                        value_preview = str(value)[:100] + "..." if len(str(value)) > 100 else str(value)
                        description += f"  {key}: {value_preview}\n"
        
        return description
    
    def convert_to_sql(self, natural_query: str) -> Optional[str]:
        """Convert natural language query to SQL.
        
        Args:
            natural_query: User's natural language question
            
        Returns:
            SQL query string or None if conversion fails
        """
        system_prompt = """You are an expert SQL query generator for a pharmaceutical products database.

Your task:
1. Analyze the user's natural language question
2. Generate a valid SQLite SQL query that answers the question
3. Return ONLY the SQL query, no explanations or markdown

Guidelines:
- Use SELECT statements (no INSERT, UPDATE, DELETE, DROP)
- Use LIKE '%keyword%' for text searches (case-insensitive with LOWER())
- Use JSON functions for querying JSON fields (fact_box, safety_advice)
- Limit results to reasonable numbers (use LIMIT clause)
- Use appropriate WHERE, ORDER BY, GROUP BY as needed
- For counting queries, use COUNT(*)
- For listing queries, select relevant columns only

Common query patterns:
- "Find products for X" → WHERE uses LIKE '%X%' OR product_introduction LIKE '%X%'
- "How many products..." → SELECT COUNT(*) FROM ...
- "List all products that..." → SELECT product_name, ... FROM ... WHERE ...
- "What are the side effects of X" → SELECT side_effects FROM ... WHERE product_name LIKE '%X%'
"""

        schema_desc = self._build_schema_description()
        
        user_prompt = f"""Database Schema:
{schema_desc}

User Question: {natural_query}

Generate the SQL query:"""

        try:
            response = self.llm_client.get_completion(
                prompt=user_prompt,
                system_prompt=system_prompt,
                temperature=0.1,
                max_tokens=500
            )
            
            # Extract and clean SQL
            sql = self._extract_sql(response)
            
            # Validate SQL
            if self._validate_sql(sql):
                return sql
            else:
                print(f"Warning: Generated SQL failed validation: {sql}")
                return None
        
        except Exception as e:
            print(f"Error converting query: {e}")
            return None
    
    def _extract_sql(self, response: str) -> str:
        """Extract SQL query from LLM response.
        
        Args:
            response: LLM response text
            
        Returns:
            Clean SQL query
        """
        # Remove markdown code blocks if present
        response = response.strip()
        if "```sql" in response:
            response = response.split("```sql")[1].split("```")[0]
        elif "```" in response:
            response = response.split("```")[1].split("```")[0]
        
        # Clean up the SQL
        sql = response.strip()
        
        # Remove any leading/trailing semicolons or quotes
        sql = sql.rstrip(';').strip()
        
        return sql
    
    def _validate_sql(self, sql: str) -> bool:
        """Validate SQL query for safety and correctness.
        
        Args:
            sql: SQL query string
            
        Returns:
            True if valid, False otherwise
        """
        if not sql:
            return False
        
        # Convert to lowercase for checking
        sql_lower = sql.lower().strip()
        
        # Must start with SELECT
        if not sql_lower.startswith('select'):
            return False
        
        # Disallow dangerous operations
        dangerous_keywords = [
            'drop', 'delete', 'insert', 'update', 'alter', 'create',
            'truncate', 'replace', 'grant', 'revoke'
        ]
        
        for keyword in dangerous_keywords:
            if re.search(r'\b' + keyword + r'\b', sql_lower):
                return False
        
        # Try to parse with SQLite
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(f"EXPLAIN QUERY PLAN {sql}")
            conn.close()
            return True
        except Exception as e:
            print(f"SQL validation error: {e}")
            return False
    
    def explain_query(self, natural_query: str, sql_query: str) -> str:
        """Generate a human-readable explanation of the SQL query.
        
        Args:
            natural_query: Original natural language query
            sql_query: Generated SQL query
            
        Returns:
            Explanation text
        """
        system_prompt = """You are a helpful assistant that explains SQL queries in simple terms.
Explain what the SQL query does and how it answers the user's question.
Keep it brief and non-technical."""

        user_prompt = f"""User asked: "{natural_query}"

Generated SQL: {sql_query}

Explain what this SQL query does:"""

        try:
            explanation = self.llm_client.get_completion(
                prompt=user_prompt,
                system_prompt=system_prompt,
                temperature=0.3,
                max_tokens=200
            )
            return explanation.strip()
        except Exception as e:
            return f"SQL Query: {sql_query}"


def main():
    """Main function for testing."""
    try:
        Config.validate()
        
        converter = NLToSQLConverter()
        
        # Test queries
        test_queries = [
            "Find all products for glaucoma",
            "How many products are there?",
            "What are the side effects of Acetamide?",
            "List all products that contain amlodipine",
            "Show me products with pregnancy warnings"
        ]
        
        print("=" * 60)
        print("TESTING NATURAL LANGUAGE TO SQL CONVERSION")
        print("=" * 60)
        
        for query in test_queries:
            print(f"\nQuery: {query}")
            sql = converter.convert_to_sql(query)
            if sql:
                print(f"SQL: {sql}")
                explanation = converter.explain_query(query, sql)
                print(f"Explanation: {explanation}")
            else:
                print("Failed to convert query")
            print("-" * 60)
    
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()

