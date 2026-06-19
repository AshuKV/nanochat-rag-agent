# 🚀 Command Reference Guide

## Prerequisites
✅ Dependencies installed: `pip install -r requirements.txt`
✅ Configuration file created: `.env`
⚠️  **ACTION REQUIRED**: Add your API key to `.env` file

---

## Step-by-Step Commands

### 1. Configure Your API Key

**Option A: Edit .env file**
```bash
# Open in nano editor
nano .env

# Or open in default text editor (macOS)
open -e .env

# Or use VS Code
code .env
```

**Option B: Use Ollama (FREE, no API key needed)**
```bash
# Install Ollama from https://ollama.ai, then:
ollama pull llama3.2
ollama serve  # Keep this running in another terminal

# Update .env:
# LLM_PROVIDER=ollama
```

---

### 2. Create Database (First Time Setup)

```bash
# Navigate to project directory
cd /Users/ashutoshkumv/Documents/gAi/special_assignment/pharma_nlp_db

# Run setup wizard
python setup.py
```

**What this does:**
- Analyzes your JSON pharmaceutical data
- Uses AI to design optimal database schema
- Creates SQLite database (`pharmadb.db`)
- Loads all 775+ products into the database
- Takes ~2-5 minutes

---

### 3. Test the System

```bash
# Quick system test
python test_system.py
```

**What this checks:**
- Configuration validity
- LLM connection
- Database access
- Query engine functionality

---

### 4. Run the Application

#### Option A: CLI Interface (Terminal)

```bash
python cli.py
```

**Features:**
- Interactive terminal interface
- Rich formatting with colors
- Command history
- Example queries

**Commands in CLI:**
- Type your question naturally
- `/help` - Show help
- `/examples` - Show example queries
- `/history` - View query history
- `/stats` - Database statistics
- `/exit` - Quit

**Example queries to try:**
```
How many products are in the database?
Find products for diabetes
What are the side effects of Dolo 650?
List all products containing aspirin
Show me products unsafe during pregnancy
```

---

#### Option B: GUI Interface (Web Browser)

```bash
streamlit run app.py
```

**Features:**
- Modern web interface
- Click example queries
- Download results (JSON/CSV)
- Query history
- Real-time statistics

**Access:** Opens automatically at `http://localhost:8501`

---

### 5. Run Examples

```bash
# Run example queries
python examples/example_queries.py

# Run programmatic usage examples
python examples/programmatic_usage.py

# Export example results
python examples/example_queries.py --export
```

---

## Common Commands Summary

```bash
# Setup (one-time)
cd /Users/ashutoshkumv/Documents/gAi/special_assignment/pharma_nlp_db
pip install -r requirements.txt
nano .env  # Add your API key
python setup.py

# Daily usage
python cli.py              # CLI interface
streamlit run app.py       # Web GUI

# Testing
python test_system.py      # System health check
python examples/example_queries.py  # Run examples
```

---

## Troubleshooting Commands

### Check Configuration
```bash
python -c "from config.config import Config; Config.validate(); print('✓ Config OK')"
```

### Check Database
```bash
ls -lh data/pharmadb.db
python -c "import sqlite3; conn = sqlite3.connect('data/pharmadb.db'); print('✓ Database accessible')"
```

### Check LLM Connection
```bash
python -c "from src.llm_client import get_llm_client; client = get_llm_client(); print('✓ LLM connected')"
```

### Reinstall Dependencies
```bash
pip install -r requirements.txt --upgrade
```

### Recreate Database
```bash
python setup.py  # Answer 'yes' when asked to recreate
```

---

## Project Structure

```
pharma_nlp_db/
├── .env                      # Configuration (YOU MUST EDIT THIS)
├── setup.py                  # Database setup wizard
├── cli.py                    # CLI interface
├── app.py                    # Streamlit GUI
├── test_system.py           # System tests
├── config/
│   └── config.py            # Configuration manager
├── src/
│   ├── llm_client.py        # LLM interface
│   ├── schema_creator.py   # Schema generator
│   ├── data_loader.py       # Data loader
│   ├── nl_to_sql.py         # NL to SQL converter
│   └── query_engine.py      # Query processor
├── data/
│   └── pharmadb.db          # SQLite database (created)
└── examples/
    ├── example_queries.py
    └── programmatic_usage.py
```

---

## Next Steps

1. **Add API Key**: Edit `.env` and add your OpenAI/Anthropic key (or use Ollama)
2. **Run Setup**: `python setup.py`
3. **Test System**: `python test_system.py`
4. **Start Querying**: `python cli.py` or `streamlit run app.py`

---

## Quick Links

- **README**: Full documentation
- **QUICKSTART.md**: 5-minute guide
- **IMPLEMENTATION_GUIDE.md**: Technical details
- **COMMANDS.md**: This file

---

**Need Help?**
- Check `README.md` for detailed documentation
- Run `python test_system.py` to diagnose issues
- Ensure `.env` has valid API key
- Verify database exists: `ls data/pharmadb.db`

🎉 **Happy Querying!** 💊

