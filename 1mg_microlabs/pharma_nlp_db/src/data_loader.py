"""Database Loader - Populates SQLite database from JSON files."""

import json
import sqlite3
import os
import sys
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import Config


class DataLoader:
    """Loads pharma data from JSON files into SQLite database."""
    
    def __init__(self):
        """Initialize Data Loader."""
        self.db_path = Config.DB_PATH
        self.table_name = Config.TABLE_NAME
    
    def parse_json_data(self, json_data: Dict[str, Any], filename: str) -> Dict[str, Any]:
        """Parse JSON data and extract fields for database insertion.
        
        Args:
            json_data: Raw JSON data from file
            filename: Name of the JSON file (used for product name)
            
        Returns:
            Dictionary with extracted and formatted fields
        """
        # Extract product name from filename (remove .json extension)
        product_name = filename.replace('.json', '')
        
        # Extract fields (handling various possible key names)
        parsed_data = {
            'product_name': product_name,
            'product_introduction': json_data.get('Product introduction', ''),
            'uses': json_data.get('Uses of Acetamide Tablet', 
                                 json_data.get('Uses', '')),
            'side_effects': json_data.get('Side effects of Acetamide Tablet', 
                                         json_data.get('Side effects', '')),
            'how_to_use': json_data.get('How to use Acetamide Tablet', 
                                       json_data.get('How to use', '')),
            'how_it_works': json_data.get('How Acetamide Tablet works', 
                                         json_data.get('How it works', '')),
            'missed_dose_info': json_data.get('What if you forget to take Acetamide Tablet?', 
                                             json_data.get('Missed dose', '')),
            'fact_box': json.dumps(json_data.get('fact box', {})),
            'safety_advice': json.dumps(json_data.get('safety_advice', {})),
            'full_data': json.dumps(json_data)
        }
        
        return parsed_data
    
    def load_json_files(self, json_dir: str) -> List[Dict[str, Any]]:
        """Load all JSON files from directory.
        
        Args:
            json_dir: Directory containing JSON files
            
        Returns:
            List of parsed data dictionaries
        """
        json_files = list(Path(json_dir).glob("*.json"))
        parsed_records = []
        errors = []
        
        print(f"Found {len(json_files)} JSON files to load...")
        
        for idx, json_file in enumerate(json_files, 1):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    parsed = self.parse_json_data(data, json_file.name)
                    parsed_records.append(parsed)
                
                if idx % 100 == 0:
                    print(f"  Processed {idx}/{len(json_files)} files...")
            
            except Exception as e:
                errors.append((json_file.name, str(e)))
        
        if errors:
            print(f"\nWarning: {len(errors)} files had errors:")
            for filename, error in errors[:5]:  # Show first 5 errors
                print(f"  - {filename}: {error}")
            if len(errors) > 5:
                print(f"  ... and {len(errors) - 5} more")
        
        return parsed_records
    
    def insert_records(self, records: List[Dict[str, Any]]) -> int:
        """Insert records into database.
        
        Args:
            records: List of parsed data dictionaries
            
        Returns:
            Number of records successfully inserted
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get column names from first record
            if not records:
                print("No records to insert")
                return 0
            
            # Get actual table columns
            cursor.execute(f"PRAGMA table_info({self.table_name})")
            table_columns = [col[1] for col in cursor.fetchall() if col[1] != 'id']
            
            # Prepare insert statement
            placeholders = ', '.join(['?' for _ in table_columns])
            columns_str = ', '.join(table_columns)
            insert_sql = f"INSERT INTO {self.table_name} ({columns_str}) VALUES ({placeholders})"
            
            # Insert records
            inserted_count = 0
            for record in records:
                try:
                    # Extract values in the same order as table columns
                    values = [record.get(col, '') for col in table_columns]
                    cursor.execute(insert_sql, values)
                    inserted_count += 1
                except Exception as e:
                    print(f"Error inserting record {record.get('product_name', 'unknown')}: {e}")
            
            conn.commit()
            conn.close()
            
            return inserted_count
        
        except Exception as e:
            print(f"Error inserting records: {e}")
            return 0
    
    def get_record_count(self) -> int:
        """Get total number of records in database.
        
        Returns:
            Number of records
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM {self.table_name}")
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except Exception as e:
            print(f"Error getting record count: {e}")
            return 0
    
    def clear_table(self):
        """Clear all data from the table."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM {self.table_name}")
            conn.commit()
            conn.close()
            print(f"✓ Cleared all data from {self.table_name}")
        except Exception as e:
            print(f"Error clearing table: {e}")
    
    def run(self, json_dir: str, clear_existing: bool = True) -> bool:
        """Run the complete data loading process.
        
        Args:
            json_dir: Directory containing JSON files
            clear_existing: Whether to clear existing data before loading
            
        Returns:
            True if successful, False otherwise
        """
        print("=" * 60)
        print("PHARMA DATABASE DATA LOADER")
        print("=" * 60)
        
        # Check if database exists
        if not self.db_path.exists():
            print(f"\nError: Database not found at {self.db_path}")
            print("Please run schema creator first!")
            return False
        
        # Clear existing data if requested
        if clear_existing:
            print("\n1. Clearing existing data...")
            self.clear_table()
        
        # Load JSON files
        print(f"\n2. Loading JSON files from: {json_dir}")
        records = self.load_json_files(json_dir)
        print(f"   ✓ Loaded and parsed {len(records)} files")
        
        # Insert records
        print(f"\n3. Inserting records into database...")
        inserted = self.insert_records(records)
        print(f"   ✓ Inserted {inserted}/{len(records)} records")
        
        # Verify
        print(f"\n4. Verifying database...")
        total_count = self.get_record_count()
        print(f"   ✓ Total records in database: {total_count}")
        
        print("\n✓ Data loading completed successfully!")
        print("=" * 60)
        
        return True


def main():
    """Main function for standalone execution."""
    try:
        # Validate configuration
        Config.validate()
        
        # Load data
        loader = DataLoader()
        json_dir = Config.JSON_DATA_PATH
        
        if not os.path.exists(json_dir):
            print(f"Error: JSON data directory not found: {json_dir}")
            return
        
        success = loader.run(json_dir, clear_existing=True)
        
        if not success:
            print("\nFailed to load data. Please check the errors above.")
    
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()

