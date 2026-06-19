#!/usr/bin/env python3
"""Setup script for Pharma Database System - Creates schema and loads data."""

import sys
import os

# Add to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.config import Config
from src.schema_creator import SchemaCreator
from src.data_loader import DataLoader
from rich.console import Console
from rich.prompt import Confirm, Prompt


def main():
    """Main setup function."""
    console = Console()
    
    console.print("""
╔══════════════════════════════════════════════════════════════╗
║         PHARMA DATABASE SETUP - INITIALIZATION WIZARD        ║
╚══════════════════════════════════════════════════════════════╝
""", style="bold cyan")
    
    try:
        # Validate configuration
        console.print("1. Validating configuration...", style="yellow")
        Config.validate()
        console.print("   ✓ Configuration valid\n", style="green")
        
        # Check if database already exists
        if Config.DB_PATH.exists():
            console.print(f"⚠️  Database already exists at: {Config.DB_PATH}", style="yellow")
            
            if not Confirm.ask("Do you want to recreate it? (This will delete all existing data)", default=False):
                console.print("\n[yellow]Setup cancelled. Existing database preserved.[/yellow]")
                return
            
            console.print("\n[yellow]Recreating database...[/yellow]\n")
        
        # Ask about LLM usage for schema
        use_llm = Confirm.ask(
            "\nUse LLM to automatically design database schema?",
            default=True
        )
        
        if not use_llm:
            console.print("[yellow]Will use fallback schema[/yellow]")
        
        # Create schema
        console.print("\n" + "=" * 60)
        console.print("STEP 1: Creating Database Schema", style="bold cyan")
        console.print("=" * 60 + "\n")
        
        creator = SchemaCreator()
        json_dir = Config.JSON_DATA_PATH
        
        if not os.path.exists(json_dir):
            console.print(f"[red]Error: JSON data directory not found: {json_dir}[/red]")
            console.print("\nPlease update DATA_PATH in your .env file or ensure data exists.")
            
            # Offer to input custom path
            custom_path = Prompt.ask("Enter path to JSON data directory (or 'exit' to quit)")
            if custom_path.lower() == 'exit':
                return
            
            if os.path.exists(custom_path):
                json_dir = custom_path
            else:
                console.print("[red]Path not found. Exiting.[/red]")
                return
        
        success = creator.run(json_dir, use_llm=use_llm)
        
        if not success:
            console.print("\n[red]Schema creation failed. Please check errors above.[/red]")
            return
        
        # Load data
        console.print("\n" + "=" * 60)
        console.print("STEP 2: Loading Data into Database", style="bold cyan")
        console.print("=" * 60 + "\n")
        
        loader = DataLoader()
        success = loader.run(json_dir, clear_existing=True)
        
        if not success:
            console.print("\n[red]Data loading failed. Please check errors above.[/red]")
            return
        
        # Success message
        console.print("\n" + "=" * 60, style="bold green")
        console.print("✓ SETUP COMPLETED SUCCESSFULLY!", style="bold green")
        console.print("=" * 60 + "\n", style="bold green")
        
        console.print("Your Pharma Database is ready to use!\n")
        console.print("Next steps:", style="bold cyan")
        console.print("  1. Try the CLI: [bold]python cli.py[/bold]")
        console.print("  2. Or launch the GUI: [bold]streamlit run app.py[/bold]")
        console.print("\nHave fun querying pharmaceutical data! 💊\n")
    
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Setup interrupted by user.[/yellow]")
    
    except Exception as e:
        console.print(f"\n[red]Setup failed with error: {e}[/red]")
        console.print("\nPlease check your configuration and try again.")


if __name__ == "__main__":
    main()

