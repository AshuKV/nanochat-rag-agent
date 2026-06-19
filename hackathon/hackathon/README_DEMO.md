# 🎯 Demo Files for Enhanced RAG System

## Quick Start: Show Ingestion in Your Demo

### Option 1: Check Pre-Ingested Data (⚡ FASTEST)

```bash
# Quick status check (30 seconds)
python check_ingestion.py
```

**Output shows**:
- ✅ Total chunks in vector store
- ✅ Sample source files
- ✅ Task 1 & Task 2 metadata verification
- ✅ System readiness status

---

### Option 2: Full Demo with Queries (🎯 RECOMMENDED)

```bash
# Interactive demo (5-10 minutes)
python demo_notebook.py
```

**OR use Jupyter Notebook**:
```bash
jupyter notebook demo.ipynb
```

---

### Option 3: Run Live Ingestion (⏱️ SLOW)

```bash
# Actually ingest the codebase (15-20 minutes)
python ingest_code.py
```

---

## 📁 Demo Files Created

| File | Purpose | Time | Best For |
|------|---------|------|----------|
| `check_ingestion.py` | Quick status check | 30 sec | Pre-demo verification |
| `demo_notebook.py` | Interactive CLI demo | 5-10 min | Presentations |
| `demo.ipynb` | Jupyter notebook | 5-10 min | Interactive demos |
| `DEMO_GUIDE.md` | Complete guide | - | Reference |

---

## 🚀 Recommended Demo Flow

### Before Demo (Setup)
1. **Verify ingestion** (if not already done):
   ```bash
   python check_ingestion.py
   ```

2. **If not ingested**, run once:
   ```bash
   python ingest_code.py
   ```

3. **Start LM Studio** on `localhost:1234`

### During Demo (5 minutes)

#### Part 1: Show Pre-Ingested Data (1 min)
```bash
python check_ingestion.py
```

**Say to audience**:
> "We've already ingested the nanochat codebase. Here you can see:
> - 150 code chunks stored
> - Source metadata for Task 1 (Traceability)
> - File summaries for Task 2 (Conceptual Reasoning)"

#### Part 2: Explain Ingestion (1 min)
Open `ingest_code.py` and highlight:
- Lines 23-45: File summary generation (Task 2)
- Lines 84-92: Metadata enrichment (Task 1 & 2)

**Say**:
> "During ingestion, we:
> 1. Generate file-level summaries using LLM (Task 2)
> 2. Add source path to every chunk (Task 1)
> 3. Store everything in ChromaDB"

#### Part 3: Query Demo (3 min)
```bash
python demo_notebook.py
# Choose option 3: Query Only
```

Run example queries:
1. **"How is the tokenizer implemented?"** (Task 2 - conceptual)
2. **"Show me the encode function"** (Task 1 - specific)

**Point out**:
- 📂 Source files listed (Task 1)
- 🧠 File summaries used for context (Task 2)
- ✅ Answer includes `[Source: ...]` citations (Task 1)

---

## 📊 What Each Demo Shows

### `check_ingestion.py`
```
✅ SYSTEM READY FOR DEMO!
   ✓ Task 1 (Traceability): Source metadata present
   ✓ Task 2 (Conceptual Reasoning): File summaries present

📊 INGESTION STATISTICS:
   • Total chunks: 150
   • Source files: 25

📁 Sample Source Files:
   • tokenizer.py
   • model.py
   • utils.py
```

### `demo_notebook.py` (Option 1: Quick Demo)
```
CHECKING PRE-INGESTED DATA
✅ Pre-ingested data found!

📊 Vector Store Statistics:
   • Total chunks: 150
   • Source files (in sample): 8
   • Chunks with summaries: 5/5

🔍 Sample Chunk Metadata:
   • Source: tokenizer.py
   • Content preview: class Tokenizer:...
   • File summary: This file implements...
   ✅ Task 2 metadata present!
```

### `demo.ipynb` (Jupyter)
Interactive cells showing:
1. Vector store statistics
2. Metadata verification
3. Live query with source citations
4. File summaries usage

---

## 🎓 Explaining to Your Audience

### Task 1: Traceability

**Before** (without traceability):
```
Answer: "The encode function converts text to tokens..."
❌ Which file? Unknown!
```

**After** (with traceability):
```
📂 Source Files: tokenizer.py, utils.py

Answer: "The encode function [Source: tokenizer.py] 
converts text to tokens using utilities [Source: utils.py]..."
✅ Clear source attribution!
```

### Task 2: Conceptual Reasoning

**Before** (only code chunks):
```
Retrieved: def encode(...): tokens = ...
Answer: Just shows code snippets
❌ No architectural understanding
```

**After** (with file summaries):
```
File Summary: "tokenizer.py implements the Tokenizer 
class with encode/decode methods for text processing..."

Code Chunks: def encode(...): tokens = ...

Answer: "The tokenizer uses a vocabulary-based approach
[Source: tokenizer.py]. The Tokenizer class provides..."
✅ Architectural context + implementation details!
```

---

## 🔧 Troubleshooting

### Issue: "No pre-ingested data found"
**Solution**:
```bash
python ingest_code.py
```

### Issue: "Could not connect to LLM"
**Solution**:
1. Open LM Studio
2. Load a model (e.g., Llama 3)
3. Ensure it's running on `localhost:1234`

### Issue: "Chunks missing file_summary"
**Solution**: Re-run ingestion with LLM running:
```bash
# Make sure LM Studio is running first!
rm -rf vector_stores/db_chroma_code
python ingest_code.py
```

---

## 📋 Quick Command Reference

```bash
# Check if data is ingested
python check_ingestion.py

# Run ingestion (first time or re-ingest)
python ingest_code.py

# Demo - interactive CLI
python demo_notebook.py

# Demo - Jupyter notebook
jupyter notebook demo.ipynb

# Query the system directly
python model_code.py

# Delete and re-ingest
rm -rf vector_stores/db_chroma_code
python ingest_code.py
```

---

## ✨ Key Points for Your Demo

1. **Pre-ingest** before demo (saves time)
2. Use `check_ingestion.py` to **verify** system is ready
3. Use `demo_notebook.py` or `demo.ipynb` for **presentation**
4. Emphasize **Task 1** (source citations) and **Task 2** (file summaries)
5. Show **before/after** comparison for impact

---

## 🎯 Answer to Your Question

**Q: "How to get Ingest (or show pre-ingested data)?"**

**A: Use these commands:**

```bash
# To SHOW pre-ingested data (fast demo):
python check_ingestion.py          # Shows statistics
python demo_notebook.py             # Interactive demo

# To RUN ingestion (if needed first):
python ingest_code.py               # Actually ingest

# To QUERY the system:
python model_code.py                # Ask questions
```

**For your demo**: Run `check_ingestion.py` first to verify data exists, then use `demo_notebook.py` to demonstrate querying with both tasks!

---

**Good luck with your demo! 🚀**

