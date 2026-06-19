# 📖 Implementation Guide - Pharma NLP Database System

This document explains how the system was implemented and how each component works together.

## 🎯 System Overview

The Pharma NLP Database System is a complete solution for querying pharmaceutical data using natural language. It consists of 5 main components working together:

```
User Query (Natural Language)
        ↓
[1. NL to SQL Converter] ← Uses LLM
        ↓
[2. SQL Query Validator]
        ↓
[3. Query Execution Engine] → SQLite Database
        ↓
[4. Response Generator] ← Uses LLM
        ↓
Natural Language Response
```

## 📁 Project Structure

```
pharma_nlp_db/
│
├── config/
│   ├── __init__.py
│   └── config.py              # Central configuration
│
├── src/
│   ├── __init__.py
│   ├── llm_client.py         # Universal LLM client
│   ├── schema_creator.py     # AI-powered schema design
│   ├── data_loader.py        # JSON to SQLite loader
│   ├── nl_to_sql.py          # Natural Language → SQL
│   └── query_engine.py       # Query execution & formatting
│
├── data/
│   └── pharmadb.db           # SQLite database (created)
│
├── setup.py                   # Setup wizard
├── cli.py                     # CLI interface
├── app.py                     # Streamlit GUI
├── test_system.py            # System tests
├── requirements.txt          # Dependencies
├── .env                      # Configuration (user fills)
├── README.md                 # User documentation
├── QUICKSTART.md             # Quick start guide
└── IMPLEMENTATION_GUIDE.md   # This file
```

## 🔧 Component Details

### 1. Configuration Module (`config/config.py`)

**Purpose**: Centralized configuration management

**Key Features**:
- Environment variable loading via `python-dotenv`
- Support for multiple LLM providers (OpenAI, Anthropic, Ollama)
- Path management for database and data files
- Configuration validation

**Usage**:
```python
from config.config import Config

Config.validate()  # Validates all settings
db_path = Config.DB_PATH
api_key = Config.OPENAI_API_KEY
```

### 2. LLM Client Module (`src/llm_client.py`)

**Purpose**: Universal interface for different LLM providers

**Supported Providers**:
- **OpenAI**: GPT-4, GPT-3.5, etc.
- **Anthropic**: Claude 3.5 Sonnet, Claude 3 Opus
- **Ollama**: Llama 3.2, Llama 2, Mistral (local)

**Key Features**:
- Provider abstraction - same interface for all LLMs
- Automatic client initialization
- Separate methods for regular and JSON completions
- Error handling and fallbacks

**Implementation Highlights**:
```python
class LLMClient:
    def get_completion(self, prompt, system_prompt=None, temperature=0.7):
        # Unified interface for all providers
        if self.provider == "anthropic":
            return self._get_anthropic_completion(...)
        else:
            return self._get_openai_completion(...)
```

### 3. Schema Creator Module (`src/schema_creator.py`)

**Purpose**: Automatically design and create database schema using LLM

**How It Works**:

1. **Sample Analysis**
   - Loads 5 sample JSON files
   - Extracts structure and data types
   - Identifies nested fields (fact_box, safety_advice)

2. **LLM Schema Generation**
   - Sends samples to LLM with instructions
   - LLM analyzes structure and suggests optimal schema
   - Handles various field types (TEXT, JSON, etc.)

3. **Schema Creation**
   - Generates SQL CREATE TABLE statement
   - Creates SQLite database
   - Validates schema

4. **Fallback Schema**
   - If LLM fails, uses predefined schema
   - Ensures system always works

**Key Method**:
```python
def generate_schema_with_llm(self, samples):
    system_prompt = """You are a database architect...
    Guidelines:
    1. Create a single table
    2. Use appropriate data types
    3. Add primary key
    4. Store complex data as JSON TEXT
    ..."""
    
    response = llm_client.get_completion(prompt, system_prompt)
    sql = self._extract_sql(response)
    return sql
```

### 4. Data Loader Module (`src/data_loader.py`)

**Purpose**: Load JSON pharmaceutical data into SQLite database

**How It Works**:

1. **JSON Parsing**
   - Reads all JSON files from directory
   - Extracts product name from filename
   - Parses nested structures (fact_box, safety_advice)
   - Converts complex fields to JSON strings

2. **Data Transformation**
   - Normalizes field names
   - Handles missing fields gracefully
   - Preserves full JSON in `full_data` column

3. **Batch Insertion**
   - Inserts records in batch for efficiency
   - Error handling per record
   - Progress reporting

**Key Features**:
- Handles 775+ JSON files efficiently
- Robust error handling
- Preserves data integrity
- Progress feedback

### 5. NL to SQL Converter (`src/nl_to_sql.py`)

**Purpose**: Convert natural language questions to SQL queries using LLM

**How It Works**:

1. **Context Building**
   - Retrieves database schema (columns, types)
   - Gets sample data for context
   - Formats schema description for LLM

2. **LLM Conversion**
   - Sends user query + schema to LLM
   - LLM generates appropriate SQL
   - Extracts SQL from response

3. **SQL Validation**
   - Checks query starts with SELECT
   - Blocks dangerous operations (DROP, DELETE, etc.)
   - Validates syntax with SQLite EXPLAIN
   - Returns only if valid and safe

4. **Query Explanation**
   - Optional: Generate human-readable explanation
   - Helps users understand what's happening

**Security Features**:
```python
def _validate_sql(self, sql):
    # Must start with SELECT
    if not sql_lower.startswith('select'):
        return False
    
    # Block dangerous keywords
    dangerous = ['drop', 'delete', 'insert', 'update', ...]
    for keyword in dangerous:
        if keyword in sql_lower:
            return False
    
    # Validate with SQLite
    cursor.execute(f"EXPLAIN QUERY PLAN {sql}")
    return True
```

### 6. Query Engine Module (`src/query_engine.py`)

**Purpose**: Execute queries and generate natural language responses

**How It Works**:

1. **Query Processing Pipeline**
   ```
   Natural Language Query
           ↓
   [NL to SQL Converter]
           ↓
   [SQL Validation]
           ↓
   [Query Execution]
           ↓
   [Result Formatting]
           ↓
   [Natural Language Response]
   ```

2. **SQL Execution**
   - Connects to SQLite database
   - Executes validated query
   - Converts results to dictionaries
   - Error handling and reporting

3. **Response Generation**
   - Sends results back to LLM
   - LLM formats as natural language
   - Handles different result types (counts, lists, details)
   - Truncates very long responses

4. **Result Formatting**
   - Multiple output formats supported
   - JSON for programmatic access
   - Natural language for users
   - Raw data with optional export

**Main Query Method**:
```python
def query(self, natural_query, return_sql=False, natural_response=True):
    result = {
        "query": natural_query,
        "success": False,
        "sql": None,
        "raw_results": [],
        "result_count": 0,
        "response": None,
        "error": None
    }
    
    # Convert to SQL
    sql = self.nl_to_sql.convert_to_sql(natural_query)
    
    # Execute
    raw_results, error = self.execute_sql(sql)
    
    # Generate response
    result["response"] = self.generate_natural_response(...)
    
    return result
```

### 7. CLI Interface (`cli.py`)

**Purpose**: Rich command-line interface for querying

**Key Features**:
- **Rich formatting** using `rich` library
- Colored output and panels
- Command history
- Example queries
- Database statistics
- Interactive help

**Implementation Highlights**:
- Uses `rich.console` for beautiful terminal UI
- Interactive prompts with `console.input()`
- Status spinners during processing
- Formatted tables and panels
- Keyboard interrupt handling

**Commands**:
- `/help` - Show help
- `/examples` - Show example queries
- `/history` - Query history
- `/stats` - Database stats
- `/clear` - Clear screen
- `/exit` - Quit application

### 8. GUI Interface (`app.py`)

**Purpose**: Modern web-based interface using Streamlit

**Key Features**:
- **Streamlit** framework for rapid development
- Real-time query processing
- Click-to-query examples
- Query history with expandable details
- Download results (JSON/CSV)
- Database statistics dashboard
- Responsive design

**Layout**:
```
┌─────────────────────────────────────┐
│         Header & Title              │
├─────────────┬───────────────────────┤
│  Sidebar    │   Main Content        │
│  - Stats    │   - Query Input       │
│  - Examples │   - Results Display   │
│  - Settings │   - History Tab       │
└─────────────┴───────────────────────┘
```

**Streamlit Features Used**:
- `st.tabs()` - Query/History tabs
- `st.sidebar` - Side panel
- `st.spinner()` - Loading indicators
- `st.expander()` - Collapsible sections
- `st.download_button()` - Export functionality
- `st.cache_resource()` - Engine caching

### 9. Setup Script (`setup.py`)

**Purpose**: Interactive wizard for initial setup

**Steps**:
1. Validate configuration
2. Check for existing database
3. Create schema (with LLM or fallback)
4. Load all JSON data
5. Verify everything works

**User Experience**:
- Progress feedback
- Error messages with solutions
- Confirmations for destructive operations
- Custom path input if needed
- Success summary with next steps

## 🔄 Data Flow

### Complete Query Flow

```
1. User Input
   "Find products for diabetes"
   
2. NL to SQL Conversion (LLM)
   System Prompt: Database schema + guidelines
   User Prompt: "Find products for diabetes"
   LLM Output: "SELECT product_name, uses FROM pharmadata 
                WHERE uses LIKE '%diabetes%' LIMIT 10"
   
3. SQL Validation
   ✓ Starts with SELECT
   ✓ No dangerous keywords
   ✓ Valid SQLite syntax
   
4. Query Execution
   SQLite: Execute query
   Result: [{"product_name": "Diapride...", "uses": "..."}, ...]
   
5. Response Generation (LLM)
   System Prompt: Format results naturally
   User Prompt: Original query + results
   LLM Output: "I found 8 products for diabetes:
                1. Diapride - Used for type 2 diabetes
                2. Dianorm - Controls blood sugar levels
                ..."
   
6. Display to User
   CLI: Formatted panel with results
   GUI: Card with response + download options
```

## 🛠️ Technology Stack

### Core Technologies
- **Python 3.8+**: Main programming language
- **SQLite3**: Embedded database
- **OpenAI/Anthropic APIs**: LLM providers
- **Ollama**: Local LLM option

### Python Libraries
- **openai**: OpenAI API client
- **anthropic**: Anthropic API client
- **streamlit**: Web GUI framework
- **rich**: Terminal formatting
- **python-dotenv**: Environment variables
- **pandas**: Data manipulation (optional)

### Development Tools
- **pip**: Package management
- **venv**: Virtual environments
- **.env**: Configuration management

## 🔐 Security Considerations

### 1. SQL Injection Prevention
- **No direct SQL input**: Users only provide natural language
- **LLM generates SQL**: Reduced injection risk
- **Validation layer**: Double-checks all queries
- **Read-only operations**: Only SELECT allowed

### 2. Query Validation
```python
# Block dangerous operations
dangerous_keywords = ['drop', 'delete', 'insert', 'update', 
                     'alter', 'create', 'truncate', 'replace',
                     'grant', 'revoke']

# Regex word boundary check
for keyword in dangerous_keywords:
    if re.search(r'\b' + keyword + r'\b', sql_lower):
        return False
```

### 3. API Key Security
- **Environment variables**: Never hardcoded
- **.env file**: Git-ignored by default
- **Validation**: Checked before use
- **Error handling**: Safe error messages

### 4. Data Sanitization
- **JSON encoding**: Complex data safely stored
- **Type validation**: Schema enforces types
- **Error handling**: Graceful failures

## 🎓 LLM Prompt Engineering

### Schema Generation Prompt
```
You are a database architect. Analyze JSON samples and 
create an optimal SQLite schema.

Guidelines:
1. Create a single table with appropriate columns
2. Use appropriate data types (TEXT, INTEGER, REAL, BLOB)
3. Add primary key (id INTEGER PRIMARY KEY AUTOINCREMENT)
4. For complex nested data, store as JSON TEXT
5. Keep schema simple and queryable
6. Return ONLY the CREATE TABLE statement
```

### NL to SQL Prompt
```
You are an expert SQL query generator.

Guidelines:
- Use SELECT statements only (no INSERT, UPDATE, DELETE, DROP)
- Use LIKE '%keyword%' for text searches
- Use JSON functions for querying JSON fields
- Limit results to reasonable numbers
- Use appropriate WHERE, ORDER BY, GROUP BY
- Return ONLY the SQL query, no explanations

Database Schema:
[Schema details here]

User Question: [User's question]
Generate the SQL query:
```

### Response Generation Prompt
```
You are a helpful pharmaceutical information assistant.
Generate a clear, natural language response.

Guidelines:
- Be concise but informative
- Use bullet points for lists
- Highlight important information (warnings, side effects)
- If no results, say so politely
- Don't mention SQL or technical details
- Focus on answering the question directly

User Question: [Original question]
Query Results: [Results from database]
Generate a natural, helpful response:
```

## 📊 Performance Considerations

### Database Performance
- **Indexes**: Can be added for frequently queried columns
- **Query limits**: Automatic LIMIT clauses prevent large result sets
- **Connection pooling**: Single connection per query (sufficient for small scale)

### LLM Performance
- **Temperature tuning**: Lower (0.1-0.3) for SQL, higher (0.5-0.7) for responses
- **Token limits**: Reasonable max_tokens to prevent long responses
- **Caching**: Streamlit caches QueryEngine initialization
- **Prompt optimization**: Concise prompts reduce latency and cost

### Scaling Considerations
For larger deployments:
- **Connection pooling**: Use `sqlite3.connect(uri=True, check_same_thread=False)`
- **Query caching**: Cache common queries
- **Response caching**: Cache LLM responses for identical queries
- **Rate limiting**: Implement API rate limits
- **Async operations**: Use async LLM calls for better concurrency

## 🐛 Error Handling

### Error Hierarchy
```
1. Configuration Errors
   → Missing API keys
   → Invalid paths
   → Missing dependencies

2. Database Errors
   → Database not found
   → Schema errors
   → Query execution errors

3. LLM Errors
   → API failures
   → Rate limits
   → Invalid responses

4. Query Errors
   → Invalid SQL generated
   → No results found
   → Timeout errors
```

### Graceful Degradation
- **Fallback schema**: If LLM fails during setup
- **Manual SQL**: Future feature for advanced users
- **Simple formatting**: If LLM response generation fails
- **Error messages**: Always user-friendly, never technical

## 📈 Future Enhancements

### Potential Improvements
1. **Query Caching**: Cache frequently asked questions
2. **Query Suggestions**: Autocomplete based on history
3. **Advanced Filters**: Date ranges, complex conditions
4. **Multi-table Support**: Join multiple tables
5. **Export Formats**: PDF, Excel, etc.
6. **User Accounts**: Save preferences and history
7. **Analytics**: Track popular queries
8. **Voice Input**: Speech-to-text integration
9. **Multilingual**: Support multiple languages
10. **Mobile App**: React Native or Flutter

### Optimization Ideas
- Pre-compute common queries
- Add full-text search indexes
- Implement query result caching
- Use connection pooling
- Batch LLM requests
- Compress large responses

## 🎯 Design Decisions

### Why SQLite?
- ✅ No server setup required
- ✅ Single file database
- ✅ Fast for read operations
- ✅ Perfect for 1000s of records
- ✅ ACID compliance

### Why Multiple LLM Support?
- ✅ User choice and flexibility
- ✅ Cost optimization (Ollama is free)
- ✅ Redundancy (if one API fails)
- ✅ Feature comparison

### Why Both CLI and GUI?
- ✅ CLI: Fast, scriptable, SSH-friendly
- ✅ GUI: User-friendly, visual, shareable
- ✅ Different use cases
- ✅ Demonstrates versatility

### Why Natural Language Response?
- ✅ Better user experience
- ✅ Context-aware formatting
- ✅ Highlights important information
- ✅ Non-technical users can understand

## 📝 Testing

### Manual Testing
```bash
# Test system health
python test_system.py

# Test specific components
python src/schema_creator.py
python src/data_loader.py
python src/nl_to_sql.py
python src/query_engine.py
```

### Test Queries
- Simple counts: "How many products?"
- Specific searches: "Find Dolo 650"
- Complex filters: "Products unsafe during pregnancy"
- Aggregations: "Most common side effects"
- Existence checks: "Are there any antibiotics?"

## 🤝 Contributing

This is an educational project. To extend:

1. **Fork** the project
2. **Create** a feature branch
3. **Implement** your changes
4. **Test** thoroughly
5. **Document** your changes
6. **Submit** for review

---

## 📚 Additional Resources

- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [OpenAI API Docs](https://platform.openai.com/docs)
- [Anthropic Claude Docs](https://docs.anthropic.com)
- [Streamlit Documentation](https://docs.streamlit.io)
- [Rich Library Docs](https://rich.readthedocs.io)

---

**Built with ❤️ for GenAI Bootcamp 2025**

For questions or issues, refer to the main README.md file.

