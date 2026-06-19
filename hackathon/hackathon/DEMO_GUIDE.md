# Demo Guide: How to Show Ingestion

## Quick Answer: Two Options for Demonstrating Ingestion

### Option A: Show Pre-Ingested Data (⚡ FAST - Recommended for Demos)

**Best for**: Quick demos, presentations, time-limited scenarios

**Steps**:
1. Make sure data is already ingested (run `python ingest_code.py` once beforehand)
2. Use the demo files to **show** the pre-ingested data

**Using Python Script**:
```bash
cd /Users/ashutoshkumv/Documents/gAi/hackathon/hackathon
python demo_notebook.py
# Choose option 1: "QUICK DEMO"
```

**Using Jupyter Notebook**:
```bash
jupyter notebook demo.ipynb
# Run Part 1 to check pre-ingested data
# Shows statistics without re-ingesting
```

**What it demonstrates**:
- ✅ Shows vector store exists
- ✅ Displays total chunks count
- ✅ Shows sample source files
- ✅ Verifies Task 1 metadata (source)
- ✅ Verifies Task 2 metadata (file_summary)

---

### Option B: Run Live Ingestion (🐌 SLOW - Complete Demo)

**Best for**: Full demonstrations, when you have 15-20 minutes

**Steps**:
1. Make sure LM Studio is running on `localhost:1234`
2. Run ingestion live during demo

```bash
cd /Users/ashutoshkumv/Documents/gAi/hackathon/hackathon
python ingest_code.py
```

**What it shows**:
```
Loaded 25 documents
Initializing LLM for file summary generation...
LLM initialized successfully
Generating file-level summaries for conceptual reasoning...
Generated summary for: tokenizer.py
Generated summary for: utils.py
...
Processed 150 chunks from 25 files
Vector Store Created with Enhanced Metadata!
✓ Task 1: Traceability metadata added (source field)
✓ Task 2: File-level summaries added for conceptual reasoning
```

---

## Complete Demo Flow (Recommended)

### Pre-Demo Setup (Do this BEFORE your presentation)
```bash
cd /Users/ashutoshkumv/Documents/gAi/hackathon/hackathon

# 1. Make sure you have ingested data
python ingest_code.py

# 2. Verify it worked
python -c "import os; print('Data exists!' if os.path.exists('vector_stores/db_chroma_code') else 'No data')"
```

### During Demo (5-10 minutes)

#### Step 1: Show Pre-Ingested Data (2 min)
```bash
python demo_notebook.py
# Choose option 1
```

**What to say**:
> "We've already ingested the nanochat codebase. Let me show you what's stored..."
> 
> - Points out total chunks
> - Shows source files
> - Highlights metadata fields (Task 1 & 2)

#### Step 2: Explain Ingestion Process (2 min)
Show `ingest_code.py` file and explain:
- Loads Python files
- Generates file summaries with LLM (Task 2)
- Adds source metadata (Task 1)
- Creates embeddings
- Stores in ChromaDB

#### Step 3: Query the System (3-5 min)
```bash
# Use Python script
python demo_notebook.py
# Choose option 3

# OR use Jupyter
jupyter notebook demo.ipynb
# Run Parts 2-3
```

**Example queries**:
1. "How is the tokenizer implemented?" (Task 2 - conceptual)
2. "Show me the encode function" (Task 1 - specific with source)
3. "What is the overall architecture?" (Task 2 - high-level)

**What to highlight**:
- 📂 Source files are listed (Task 1)
- 🧠 File summaries provide context (Task 2)
- ✅ Answers include [Source: ...] citations (Task 1)

---

## Files You Created

### 1. `demo_notebook.py` - Interactive Python Script
**Purpose**: Command-line demo with 3 modes

**Usage**:
```bash
python demo_notebook.py
```

**Modes**:
1. Quick Demo - show pre-ingested data + query
2. Full Demo - run ingestion + query
3. Query Only - skip to querying

### 2. `demo.ipynb` - Jupyter Notebook
**Purpose**: Interactive notebook for step-by-step demo

**Usage**:
```bash
jupyter notebook demo.ipynb
```

**Sections**:
- Part 1: Check pre-ingested data
- Part 2: Query example with both tasks
- Part 3: Interactive query section

---

## How to Check if Data is Already Ingested

### Quick Check:
```bash
ls -la /Users/ashutoshkumv/Documents/gAi/hackathon/hackathon/vector_stores/db_chroma_code
```

If directory exists → Data is ingested ✅

### Detailed Check:
```python
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="thenlper/gte-large",
    model_kwargs={'device': 'cpu'}
)

vectordb = Chroma(
    persist_directory="vector_stores/db_chroma_code",
    embedding_function=embeddings
)

count = vectordb._collection.count()
print(f"Total chunks: {count}")

# Sample documents
docs = vectordb.similarity_search("import", k=3)
print(f"Sample sources: {[doc.metadata.get('source', 'unknown') for doc in docs]}")
```

---

## Troubleshooting

### "No pre-ingested data found"
**Solution**: Run ingestion first
```bash
python ingest_code.py
```

### "Could not connect to LLM"
**Solution**: Start LM Studio
- Open LM Studio
- Load a model
- Make sure it's running on `localhost:1234`

### "ModuleNotFoundError"
**Solution**: Install dependencies
```bash
pip install langchain langchain-community chromadb sentence-transformers
```

---

## Best Practices for Demo

### DO:
✅ Pre-ingest data before demo  
✅ Test the demo flow beforehand  
✅ Have LM Studio running  
✅ Use Jupyter notebook for interactive demos  
✅ Prepare 2-3 example queries  

### DON'T:
❌ Run live ingestion unless you have time  
❌ Skip checking pre-ingested data first  
❌ Use complex queries that take too long  
❌ Forget to highlight Task 1 and Task 2  

---

## Summary: Answer to Your Question

**Q: "How to get Ingest (or show pre-ingested data)?"**

**A: Two approaches:**

1. **Show pre-ingested** (FAST):
   ```bash
   python demo_notebook.py  # Choose option 1
   ```
   
2. **Run ingestion live** (SLOW):
   ```bash
   python ingest_code.py  # Watch it process
   ```

**For demos**: Use option 1 (show pre-ingested) because:
- Takes 2 minutes instead of 20
- Still demonstrates both tasks
- More reliable (no network/LLM failures)
- Better for Q&A time

The demo files will **inspect the vector store** and show:
- Total chunks ingested
- Source files present
- Metadata structure (Task 1 & 2)
- Sample queries with results

This proves ingestion worked WITHOUT re-running it! 🎯

