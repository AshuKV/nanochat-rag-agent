# 💊 Pharma Database NLP Query System

A sophisticated natural language query system for pharmaceutical product data, powered by Large Language Models (LLMs). Ask questions in plain English and get instant, accurate answers from a database of 775+ pharma products.

## 🎯 Features

- **🤖 LLM-Powered Schema Generation**: Automatically designs optimal database schemas from JSON data
- **💬 Natural Language Queries**: Ask questions in plain English, no SQL knowledge required
- **🔄 Multi-LLM Support**: Works with OpenAI, Anthropic Claude, or local Ollama models
- **🎨 Dual Interface**: Both CLI and GUI (Streamlit) interfaces available
- **⚡ Fast & Accurate**: Instant responses with contextual understanding
- **📊 Rich Results**: Get human-readable answers with optional raw data export
- **🔒 Safe Queries**: Automatic validation prevents harmful SQL operations

## 📋 System Components

### 1. **LLM-Based Schema Creator**
Analyzes JSON pharmaceutical data and automatically generates an optimal SQLite database schema using AI.

### 2. **Natural Language to SQL Module**
Converts user questions in natural language to SQL queries using LLM understanding.

### 3. **Query Execution Engine**
Safely executes SQL queries and retrieves results from the database.

### 4. **Response Generator**
Formats query results into clear, human-readable responses using AI.

### 5. **User Interfaces**
- **CLI**: Rich terminal interface with colors and formatting
- **GUI**: Modern web-based Streamlit application

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- API key for OpenAI, Anthropic, or Ollama running locally

### Installation

1. **Clone or navigate to the project directory:**
```bash
cd /Users/ashutoshkumv/Documents/gAi/special_assignment/pharma_nlp_db
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables:**

Create a `.env` file in the project root:

```bash
# For OpenAI
LLM_PROVIDER=openai
OPENAI_API_KEY=your_openai_key_here
OPENAI_MODEL=gpt-4o-mini

# For Anthropic Claude
# LLM_PROVIDER=anthropic
# ANTHROPIC_API_KEY=your_anthropic_key_here
# ANTHROPIC_MODEL=claude-3-5-sonnet-20241022

# For Ollama (local)
# LLM_PROVIDER=ollama
# OLLAMA_BASE_URL=http://localhost:11434
# OLLAMA_MODEL=llama3.2

# Data path (adjust if needed)
DATA_PATH=../1mg_microlabs
```

4. **Run setup to create database:**
```bash
python setup.py
```

This will:
- Analyze your JSON pharmaceutical data
- Use LLM to design optimal database schema
- Create SQLite database (`pharmadb.db`)
- Load all product data into the database

### Usage

#### CLI Interface

```bash
python cli.py
```

**Features:**
- Interactive terminal interface
- Command history
- Example queries
- Rich formatting with colors

**Commands:**
- Type your question naturally
- `/help` - Show help
- `/examples` - Show example queries
- `/history` - Show query history
- `/stats` - Database statistics
- `/exit` - Quit

#### GUI Interface (Streamlit)

```bash
streamlit run app.py
```

**Features:**
- Modern web interface
- Click example queries
- Download results as JSON/CSV
- Query history
- Real-time statistics

Access at: `http://localhost:8501`

## 📝 Example Queries

Try these natural language questions:

```
"How many products are in the database?"
"Find products for treating diabetes"
"What are the side effects of Dolo 650?"
"List all products containing aspirin"
"Show me antibiotics"
"Which products are unsafe during pregnancy?"
"Find painkillers"
"What products treat high blood pressure?"
"Show glaucoma medications"
"List products with drowsiness side effects"
```

## 🏗️ Architecture

```
pharma_nlp_db/
├── config/
│   └── config.py              # Configuration management
├── src/
│   ├── llm_client.py         # LLM client (OpenAI/Anthropic/Ollama)
│   ├── schema_creator.py     # AI-powered schema generation
│   ├── data_loader.py        # JSON to SQLite loader
│   ├── nl_to_sql.py          # Natural language to SQL converter
│   └── query_engine.py       # Query execution & response generation
├── data/
│   └── pharmadb.db           # SQLite database (created by setup)
├── setup.py                   # Database setup wizard
├── cli.py                     # CLI interface
├── app.py                     # Streamlit GUI
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## 🔧 Database Schema

The database is automatically designed by the LLM based on your JSON data structure. Typical schema includes:

```sql
CREATE TABLE pharmadata (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    product_introduction TEXT,
    uses TEXT,
    side_effects TEXT,
    how_to_use TEXT,
    how_it_works TEXT,
    missed_dose_info TEXT,
    fact_box TEXT,          -- JSON field
    safety_advice TEXT,     -- JSON field
    full_data TEXT          -- Complete JSON
)
```

## 🔐 Security

- **Read-Only Queries**: System only allows SELECT statements
- **SQL Validation**: Automatic validation prevents DROP, DELETE, UPDATE, etc.
- **Query Sanitization**: LLM-generated SQL is validated before execution
- **No Direct SQL Input**: Users interact only through natural language

## 🎓 How It Works

1. **User Input**: You ask a question in natural language
2. **Schema Context**: System provides database schema to LLM
3. **SQL Generation**: LLM converts your question to SQL query
4. **Validation**: Query is validated for safety and correctness
5. **Execution**: SQL is executed against SQLite database
6. **Response Generation**: LLM formats results into natural language
7. **Display**: Beautiful, readable response shown to user

## 📊 Supported LLM Providers

### OpenAI (Recommended)
- **Models**: GPT-4, GPT-4 Turbo, GPT-3.5
- **Setup**: Get API key from platform.openai.com
- **Cost**: Pay per token

### Anthropic Claude
- **Models**: Claude 3.5 Sonnet, Claude 3 Opus
- **Setup**: Get API key from console.anthropic.com
- **Cost**: Pay per token

### Ollama (Local, Free)
- **Models**: Llama 3.2, Llama 2, Mistral, etc.
- **Setup**: Install Ollama and run locally
- **Cost**: Free (runs on your machine)

## 🐛 Troubleshooting

### Database not found
```bash
# Run setup first
python setup.py
```

### LLM API errors
- Check your API key in `.env`
- Verify API key has sufficient credits
- Check network connection

### Module not found
```bash
# Install dependencies
pip install -r requirements.txt
```

### JSON data not found
- Update `DATA_PATH` in `.env`
- Ensure JSON files exist at specified path

## 📚 API Usage (Advanced)

You can also use the system programmatically:

```python
from src.query_engine import QueryEngine

# Initialize
engine = QueryEngine()

# Query
result = engine.query("How many products are there?")

# Access results
print(result['response'])        # Natural language answer
print(result['raw_results'])     # Raw data
print(result['sql'])             # Generated SQL
print(result['result_count'])    # Number of results
```

## 🤝 Contributing

This is an educational project. Feel free to extend it with:
- Additional LLM providers
- Enhanced query understanding
- More sophisticated response formatting
- Export to different formats
- Query optimization
- Caching layer

## 📄 License

This project is for educational purposes as part of GenAI Bootcamp 2025.

## 🙏 Acknowledgments

- **GenAI Bootcamp 2025** for the assignment
- **1mg** for pharmaceutical data structure
- **OpenAI/Anthropic** for LLM APIs
- **Streamlit** for amazing GUI framework

## 📞 Support

For issues or questions:
1. Check this README first
2. Review error messages carefully
3. Verify configuration in `.env`
4. Ensure database is set up (`python setup.py`)

---

**Made with ❤️ using Python, SQLite, Streamlit & AI**

🎉 Happy Querying! 💊

