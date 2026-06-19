"""LLM-based Schema Creator for SQLite database."""

import json
import sqlite3
import os
import sys
from pathlib import Path
from typing import Dict, List, Any

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import Config
from src.llm_client import get_llm_client


class SchemaCreator:
    """Creates SQLite database schema using LLM analysis of JSON data."""
    
    def __init__(self):
        """Initialize Schema Creator."""
        self.llm_client = get_llm_client()
        self.db_path = Config.DB_PATH
        self.table_name = Config.TABLE_NAME
    
    def analyze_json_samples(self, json_dir: str, sample_count: int = 5) -> List[Dict[str, Any]]:
        """Load sample JSON files for analysis.
        
        Args:
            json_dir: Directory containing JSON files
            sample_count: Number of samples to analyze
            
        Returns:
            List of sample JSON data
        """
        json_files = list(Path(json_dir).glob("*.json"))[:sample_count]
        samples = []
        
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    samples.append(data)
            except Exception as e:
                print(f"Warning: Could not read {json_file}: {e}")
        
        return samples
    
    def generate_schema_with_llm(self, samples: List[Dict[str, Any]]) -> str:
        """Use LLM to generate optimal database schema based on JSON samples.
        
        Args:
            samples: List of sample JSON data
            
        Returns:
            SQL CREATE TABLE statement
        """
        system_prompt = """You are a database architect. Analyze the provided JSON samples and create an optimal SQLite database schema.

Guidelines:
1. Create a single table with appropriate columns
2. Use appropriate data types (TEXT, INTEGER, REAL, BLOB)
3. Add a primary key (id INTEGER PRIMARY KEY AUTOINCREMENT)
4. Add a column for product_name (extracted from filename or data)
5. For complex nested data (like dictionaries), store as JSON TEXT
6. Keep the schema simple and queryable
7. Return ONLY the CREATE TABLE SQL statement, nothing else"""

        user_prompt = f"""Analyze these pharma product JSON samples and create a SQLite schema:

Table Name: {self.table_name}

Sample Data (first 3 samples):
{json.dumps(samples[:3], indent=2)}

Return ONLY the CREATE TABLE statement."""

        try:
            response = self.llm_client.get_completion(
                prompt=user_prompt,
                system_prompt=system_prompt,
                temperature=0.3,
                max_tokens=1000
            )
            
            # Extract SQL statement from response
            sql = self._extract_sql(response)
            return sql
        
        except Exception as e:
            print(f"Error generating schema with LLM: {e}")
            return self._get_fallback_schema()
    
    def _extract_sql(self, response: str) -> str:
        """Extract SQL statement from LLM response.
        
        Args:
            response: LLM response text
            
        Returns:
            Clean SQL statement
        """
        # Remove markdown code blocks if present
        response = response.strip()
        if "```sql" in response:
            response = response.split("```sql")[1].split("```")[0]
        elif "```" in response:
            response = response.split("```")[1].split("```")[0]
        
        return response.strip()
    
    def _get_fallback_schema(self) -> str:
        """Return a fallback schema if LLM generation fails.
        
        Returns:
            Default SQL CREATE TABLE statement
        """
        return f"""CREATE TABLE IF NOT EXISTS {self.table_name} (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    product_introduction TEXT,
    uses TEXT,
    side_effects TEXT,
    how_to_use TEXT,
    how_it_works TEXT,
    missed_dose_info TEXT,
    fact_box TEXT,
    safety_advice TEXT,
    full_data TEXT
)"""
    
    def create_database(self, schema_sql: str) -> bool:
        """Create SQLite database with the given schema.
        
        Args:
            schema_sql: SQL CREATE TABLE statement
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Ensure data directory exists
            Config.DATA_DIR.mkdir(parents=True, exist_ok=True)
            
            # Connect to database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Drop existing table if exists
            cursor.execute(f"DROP TABLE IF EXISTS {self.table_name}")
            
            # Create new table
            cursor.execute(schema_sql)
            
            conn.commit()
            conn.close()
            
            print(f"✓ Database created successfully at: {self.db_path}")
            print(f"✓ Table '{self.table_name}' created")
            return True
        
        except Exception as e:
            print(f"Error creating database: {e}")
            return False
    
    def get_schema_info(self) -> Dict[str, Any]:
        """Get information about the database schema.
        
        Returns:
            Dictionary with schema information
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get table info
            cursor.execute(f"PRAGMA table_info({self.table_name})")
            columns = cursor.fetchall()
            
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
                ]
            }
        
        except Exception as e:
            print(f"Error getting schema info: {e}")
            return {}
    
    def run(self, json_dir: str, use_llm: bool = True) -> bool:
        """Run the complete schema creation process.
        
        Args:
            json_dir: Directory containing JSON files
            use_llm: Whether to use LLM for schema generation (True) or fallback (False)
            
        Returns:
            True if successful, False otherwise
        """
        print("=" * 60)
        print("PHARMA DATABASE SCHEMA CREATOR")
        print("=" * 60)
        
        # Analyze samples
        print("\n1. Analyzing JSON samples...")
        samples = self.analyze_json_samples(json_dir, sample_count=5)
        print(f"   ✓ Analyzed {len(samples)} sample files")
        
        # Generate schema
        print("\n2. Generating database schema...")
        if use_llm:
            print("   Using LLM to design optimal schema...")
            schema_sql = self.generate_schema_with_llm(samples)
        else:
            print("   Using fallback schema...")
            schema_sql = self._get_fallback_schema()
        
        print("\n   Generated Schema:")
        print("   " + "-" * 56)
        for line in schema_sql.split('\n'):
            print(f"   {line}")
        print("   " + "-" * 56)
        
        # Create database
        print("\n3. Creating database...")
        success = self.create_database(schema_sql)
        
        if success:
            print("\n✓ Schema creation completed successfully!")
            schema_info = self.get_schema_info()
            print(f"\n   Table: {schema_info['table_name']}")
            print(f"   Columns: {len(schema_info['columns'])}")
            for col in schema_info['columns']:
                pk = " [PRIMARY KEY]" if col['primary_key'] else ""
                print(f"     - {col['name']} ({col['type']}){pk}")
        
        print("\n" + "=" * 60)
        return success


def main():
    """Main function for standalone execution."""
    try:
        # Validate configuration
        Config.validate()
        
        # Create schema
        creator = SchemaCreator()
        json_dir = Config.JSON_DATA_PATH
        
        if not os.path.exists(json_dir):
            print(f"Error: JSON data directory not found: {json_dir}")
            return
        
        success = creator.run(json_dir, use_llm=True)
        
        if not success:
            print("\nFailed to create schema. Please check the errors above.")
    
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()

