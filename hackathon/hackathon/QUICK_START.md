# Quick Start Guide - Enhanced RAG for Code Intelligence

## Prerequisites
1. LM Studio running on `http://localhost:1234` with a model loaded
2. Python environment with required packages installed

## Installation
```bash
# Install required packages
pip install langchain langchain-community chromadb sentence-transformers
```

## Step 1: Configure Your Code Repository
Edit `ingest_code.py` and set your code path:
```python
DATA_PATH = r"/path/to/your/python/code"
```

## Step 2: Ingest Your Codebase (One-Time Setup)
```bash
cd /Users/ashutoshkumv/Documents/gAi/hackathon/hackathon
python ingest_code.py
```

**What happens:**
- ✅ Loads all `.py` files from your repository
- ✅ Generates file-level summaries using LLM (**Task 2**)
- ✅ Splits code into chunks with metadata
- ✅ Adds source file information to each chunk (**Task 1**)
- ✅ Creates embeddings and stores in ChromaDB

**Expected Output:**
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

## Step 3: Ask Questions About Your Code
```bash
python model_code.py
```

**Example Session:**
```
LLM Loaded:  OpenAI
======================================================================
Enhanced RAG for Code Intelligence
✓ Task 1: Traceability - Source files are cited in answers
✓ Task 2: Conceptual Reasoning - File summaries used for context
======================================================================

Your Query (or 'quit' to exit): Outline the pretraining → midtraining → SFT → inference pipeline

----------------------------------------------------------------------
Retrieved 6 relevant code chunks

📂 Source Files Referenced (3):
   • model.py
   • training.py
   • inference.py

💭 Generating answer...

======================================================================
ANSWER:
======================================================================
The training pipeline consists of several stages [Source: training.py]:

1. **Pretraining:** The model is pretrained on a large corpus using the 
   pretrain() function, which optimizes the base language model weights.

2. **Midtraining:** Domain-specific training occurs in the midtrain() 
   function, adapting the model to specific tasks or domains.

3. **SFT (Supervised Fine-Tuning):** The supervised_finetune() function 
   performs task-specific fine-tuning using labeled data [Source: training.py].

4. **Inference:** The trained model is loaded and used for generation in 
   the InferenceEngine class [Source: inference.py], which handles prompt 
   processing and response generation.

The Model class [Source: model.py] provides the core architecture that 
persists through all stages.
======================================================================

Your Query (or 'quit' to exit): quit
```

## Key Features Demonstrated

### 🎯 Task 1: Traceability
- Notice the `📂 Source Files Referenced` section
- Each answer includes `[Source: filename.py]` citations
- Easy to verify information by checking cited files

### 🧠 Task 2: Conceptual Reasoning
- The system uses file-level summaries to understand architecture
- Can answer "how" and "why" questions, not just "what"
- Provides context about how files relate to each other

## Example Queries to Try

### Conceptual Questions (Task 2)
```
- "How is the tokenizer implemented?"
- "What is the overall architecture?"
- "Explain the training pipeline"
- "How do the different modules interact?"
```

### Specific Code Questions (Task 1)
```
- "Show me the encode function"
- "Where is the main function?"
- "What does the train() function do?"
- "List all the classes in the codebase"
```

### Mixed Questions (Both Tasks)
```
- "How does the system handle errors and where is this implemented?"
- "What design patterns are used and in which files?"
- "Describe the data flow through the system"
```

## Troubleshooting

### "Connection refused" Error
**Problem:** LM Studio is not running
**Solution:** Start LM Studio and load a model, then try again

### No file summaries in output
**Problem:** LLM unavailable during ingestion
**Solution:** Re-run `python ingest_code.py` with LM Studio running

### Poor answer quality
**Problem:** Model or context issues
**Solution:** 
- Try a better model in LM Studio
- Increase `k` value in `model_code.py` (line 120) to retrieve more chunks
- Adjust chunk size in `ingest_code.py`

## Re-ingesting After Code Changes
If your code repository changes:
```bash
# Delete old vector store
rm -rf vector_stores/db_chroma_code

# Re-ingest with updated code
python ingest_code.py
```

## Tips for Best Results
1. **Use descriptive file and function names** - helps retrieval
2. **Add docstrings** - improves summaries and chunk quality
3. **Organize code logically** - better file-level summaries
4. **Ask specific questions** - gets better targeted answers
5. **Verify citations** - check source files when in doubt

## Next Steps
- Read `IMPLEMENTATION_NOTES.md` for detailed technical information
- Customize prompts in `model_code.py` for your use case
- Adjust chunk sizes and overlap in `ingest_code.py`
- Experiment with different retrieval strategies

## Support
For issues or questions, refer to:
- `IMPLEMENTATION_NOTES.md` - Detailed implementation guide
- `ingest_code.py` - Ingestion configuration
- `model_code.py` - Query and prompt configuration

