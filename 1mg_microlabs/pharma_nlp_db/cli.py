#!/usr/bin/env python3
"""Command Line Interface for Pharma Database System."""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.config import Config
from src.query_engine import QueryEngine
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table
from rich import box


class PharmaDBCLI:
    """Command-line interface for the Pharma Database System."""
    
    def __init__(self):
        """Initialize CLI."""
        self.console = Console()
        self.query_engine = None
        self.history = []
    
    def initialize(self):
        """Initialize the query engine."""
        try:
            Config.validate()
            
            # Check if database exists
            if not Config.DB_PATH.exists():
                self.console.print("[red]Error: Database not found![/red]")
                self.console.print(f"Expected location: {Config.DB_PATH}")
                self.console.print("\nPlease run setup first:")
                self.console.print("  python setup.py")
                return False
            
            self.query_engine = QueryEngine()
            return True
        
        except Exception as e:
            self.console.print(f"[red]Error initializing: {e}[/red]")
            return False
    
    def print_header(self):
        """Print application header."""
        header = """
╔══════════════════════════════════════════════════════════════╗
║          PHARMA DATABASE - NATURAL LANGUAGE QUERY            ║
║              Powered by AI - Ask in Plain English            ║
╚══════════════════════════════════════════════════════════════╝
"""
        self.console.print(header, style="bold cyan")
    
    def print_help(self):
        """Print help information."""
        help_text = """
**Available Commands:**
- Type your question in natural language
- `/help` - Show this help message
- `/examples` - Show example queries
- `/history` - Show query history
- `/stats` - Show database statistics
- `/clear` - Clear screen
- `/exit` or `/quit` - Exit the application

**Example Questions:**
- "How many products are there?"
- "Find products for diabetes"
- "What are the side effects of Dolo 650?"
- "List all products containing aspirin"
"""
        self.console.print(Panel(Markdown(help_text), title="Help", border_style="green"))
    
    def print_examples(self):
        """Print example queries."""
        examples = self.query_engine.get_suggestions()
        
        table = Table(title="Example Queries", box=box.ROUNDED, show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Example Query", style="white")
        
        for idx, example in enumerate(examples, 1):
            table.add_row(str(idx), example)
        
        self.console.print(table)
    
    def print_history(self):
        """Print query history."""
        if not self.history:
            self.console.print("[yellow]No queries in history yet.[/yellow]")
            return
        
        table = Table(title="Query History", box=box.ROUNDED, show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Query", style="white", width=50)
        table.add_column("Results", style="green", width=10)
        
        for idx, hist in enumerate(self.history[-10:], 1):  # Show last 10
            table.add_row(
                str(idx),
                hist["query"][:50] + "..." if len(hist["query"]) > 50 else hist["query"],
                str(hist.get("result_count", 0))
            )
        
        self.console.print(table)
    
    def print_stats(self):
        """Print database statistics."""
        try:
            result = self.query_engine.query("How many products are in the database?", natural_response=False)
            
            if result["success"]:
                count = result["raw_results"][0] if result["raw_results"] else {"COUNT(*)": 0}
                total = list(count.values())[0]
                
                stats_text = f"""
**Database Statistics:**
- Database: {Config.DB_NAME}
- Table: {Config.TABLE_NAME}
- Total Products: {total}
- Location: {Config.DB_PATH}
"""
                self.console.print(Panel(Markdown(stats_text), title="Statistics", border_style="blue"))
            else:
                self.console.print("[red]Could not retrieve statistics[/red]")
        
        except Exception as e:
            self.console.print(f"[red]Error getting stats: {e}[/red]")
    
    def process_query(self, query: str):
        """Process a user query.
        
        Args:
            query: User's natural language query
        """
        with self.console.status("[bold green]Processing query...", spinner="dots"):
            result = self.query_engine.query(query, return_sql=True, natural_response=True)
        
        # Store in history
        self.history.append(result)
        
        # Display results
        if result["success"]:
            # Show SQL (collapsible)
            self.console.print(f"\n[dim]SQL: {result['sql']}[/dim]")
            self.console.print(f"[dim]Results found: {result['result_count']}[/dim]\n")
            
            # Show natural language response
            response_panel = Panel(
                result["response"],
                title="Response",
                border_style="green",
                box=box.ROUNDED
            )
            self.console.print(response_panel)
        else:
            error_panel = Panel(
                f"[red]{result['error']}[/red]\n\n{result['response']}",
                title="Error",
                border_style="red",
                box=box.ROUNDED
            )
            self.console.print(error_panel)
    
    def run(self):
        """Run the CLI application."""
        # Initialize
        if not self.initialize():
            return
        
        # Print header
        self.print_header()
        
        # Print welcome message
        self.console.print("Welcome! Ask questions about pharmaceutical products in natural language.\n")
        self.console.print("Type [cyan]/help[/cyan] for commands or [cyan]/examples[/cyan] for sample queries.\n")
        
        # Main loop
        while True:
            try:
                # Get user input
                query = self.console.input("\n[bold cyan]Your question:[/bold cyan] ").strip()
                
                if not query:
                    continue
                
                # Handle commands
                if query.startswith('/'):
                    command = query.lower()
                    
                    if command in ['/exit', '/quit', '/q']:
                        self.console.print("\n[cyan]Thank you for using Pharma Database! Goodbye![/cyan]\n")
                        break
                    
                    elif command == '/help':
                        self.print_help()
                    
                    elif command == '/examples':
                        self.print_examples()
                    
                    elif command == '/history':
                        self.print_history()
                    
                    elif command == '/stats':
                        self.print_stats()
                    
                    elif command == '/clear':
                        os.system('clear' if os.name != 'nt' else 'cls')
                        self.print_header()
                    
                    else:
                        self.console.print(f"[red]Unknown command: {query}[/red]")
                        self.console.print("Type [cyan]/help[/cyan] for available commands.")
                
                else:
                    # Process as query
                    self.process_query(query)
            
            except KeyboardInterrupt:
                self.console.print("\n\n[yellow]Interrupted by user[/yellow]")
                confirm = self.console.input("[cyan]Exit? (y/n):[/cyan] ").strip().lower()
                if confirm == 'y':
                    break
            
            except Exception as e:
                self.console.print(f"[red]Unexpected error: {e}[/red]")


def main():
    """Main entry point."""
    cli = PharmaDBCLI()
    cli.run()


if __name__ == "__main__":
    main()

