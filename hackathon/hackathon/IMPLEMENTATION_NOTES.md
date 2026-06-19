# Enhanced RAG for Code Intelligence - Implementation Notes

## Overview
This document describes the implementation of the two key tasks for the hackathon: **Traceability** and **Conceptual Reasoning** in a RAG-based code intelligence system.

## Tasks Completed

### ✅ Task 1: Traceability
**Goal:** Modify the answer-generation step so that each response explicitly references the file(s) from which it draws information using metadata fields like `source`.

**Implementation:**
1. **Enhanced Document Formatting** (`model_code.py`):
   - Created `format_docs_with_metadata()` function that extracts source file information from document metadata
   - Each code chunk is now prefixed with `[From: filename.py]` to show its origin
   - Source files are collected and displayed before generating the answer

2. **Updated Prompt Template**:
   - Modified the prompt to explicitly instruct the LLM to cite sources using format: `[Source: filename.py]`
   - The prompt now emphasizes the importance of attribution

3. **User Interface Improvements**:
   - Displays list of source files referenced before showing the answer
   - Format: `📂 Source Files Referenced (N): • filename.py`

**Result:** Every answer now includes citations to source files, making it easy to trace where information came from.

---

### ✅ Task 2: Conceptual Reasoning
**Goal:** Improve performance on higher-level conceptual questions (e.g., "How is the tokenizer implemented?") by leveraging file-level summaries present in metadata.

**Implementation:**
1. **File Summary Generation** (`ingest_code.py`):
   - Added `generate_file_summary()` function that uses an LLM to create high-level summaries
   - Each summary captures:
     - Main purpose and functionality of the file
     - Key classes, functions, or components
     - How the file fits into overall system architecture
   
2. **Enhanced Metadata Storage**:
   - Modified `get_chunks()` to generate file-level summaries during ingestion
   - Summaries are stored in the `file_summary` metadata field of each chunk
   - Each chunk now has both detailed code content AND high-level file context

3. **Two-Level Context in Prompts**:
   - Updated prompt template to include both:
     - **File-Level Context:** High-level summaries for conceptual understanding
     - **Detailed Code Context:** Specific code chunks for implementation details
   - This allows the LLM to understand the "big picture" before diving into specifics

4. **Improved Retrieval Strategy**:
   - The system now provides conceptual context alongside code details
   - Better handles questions about architecture, design patterns, and overall system structure

**Result:** The system can now answer conceptual questions by leveraging file summaries, while still providing detailed code when needed.

---

## Key Code Changes

### ingest_code.py
```python
# New function to generate file summaries
def generate_file_summary(file_content, file_path, llm):
    """Generate a high-level summary of the file for conceptual reasoning."""
    # Uses LLM to create 3-5 sentence summary covering:
    # 1. Main purpose and functionality
    # 2. Key classes, functions, or components
    # 3. How this file fits into the overall system architecture
    
# Enhanced chunk creation
def get_chunks(docs, chunk_size=2048, chunk_overlap=512, llm=None):
    """Split documents and add file-level summaries to metadata."""
    # 1. Split documents into chunks
    # 2. Generate file-level summaries using LLM
    # 3. Add summaries to each chunk's metadata
    # 4. Ensure source field is present for traceability
```

### model_code.py
```python
# Enhanced prompt with two-level context
custom_prompt_template = """
You are an assistant for question-answering tasks pertaining to Python source code.

You have access to:
1. Code snippets from specific files
2. High-level file summaries describing overall purpose and architecture

IMPORTANT: Always cite the source file(s) you're referencing in your answer using the format:
[Source: filename.py]

Question: {question}

File-Level Context (for conceptual understanding):
{file_summaries}

Detailed Code Context:
{context}

Answer (remember to cite sources):
"""

# New function for enhanced formatting
def format_docs_with_metadata(docs):
    """Format documents with source file information and extract file summaries."""
    # Returns: (formatted_context, file_summaries_text, source_files)
    
# Enhanced QA bot with better UI
def qa_bot():
    """Enhanced QA bot with traceability and conceptual reasoning."""
    # 1. Retrieve relevant documents
    # 2. Extract metadata (sources and summaries)
    # 3. Display source files
    # 4. Generate answer with both chunk and file-level context
    # 5. Present formatted answer with citations
```

---

## How to Use

### Step 1: Ingest Code (with summary generation)
```bash
# Make sure LM Studio is running on localhost:1234
python ingest_code.py
```

This will:
- Load all Python files from the configured directory
- Generate file-level summaries for each file
- Split code into chunks
- Store chunks with enhanced metadata (source + file_summary)
- Create vector embeddings and save to ChromaDB

**Note:** File summary generation requires an LLM running locally. If unavailable, it will proceed without summaries.

### Step 2: Run Q&A System
```bash
python model_code.py
```

This will:
- Load the enhanced vector store
- Start an interactive query session
- For each query:
  - Retrieve relevant code chunks
  - Display source files being referenced
  - Generate answer using both file summaries and code details
  - Present answer with proper citations

---

## Example Usage

### Example 1: Conceptual Question
```
Your Query: How is the tokenizer implemented?

📂 Source Files Referenced (2):
   • tokenizer.py
   • utils.py

ANSWER:
The tokenizer is implemented in the Tokenizer class [Source: tokenizer.py]. 
It provides methods for encoding and decoding text into token sequences. 
The implementation uses a vocabulary-based approach with support for special 
tokens. Helper functions for token validation are found in utils.py 
[Source: utils.py].
```

### Example 2: Specific Function Query
```
Your Query: Show me the encode function

📂 Source Files Referenced (1):
   • tokenizer.py

ANSWER:
Here is the encode function [Source: tokenizer.py]:

def encode(self, text: str) -> List[int]:
    """Encodes text into a list of token IDs."""
    tokens = self._split_into_tokens(text)
    return [self.vocab.get(token, self.unk_id) for token in tokens]
```

---

## Benefits

### Task 1: Traceability Benefits
- **Transparency:** Users can see exactly which files were used to generate answers
- **Verification:** Easy to verify answers by checking the cited source files
- **Debugging:** Helps identify if the system is retrieving the right files
- **Trust:** Builds confidence by showing where information comes from

### Task 2: Conceptual Reasoning Benefits
- **Better Context:** File summaries provide high-level understanding
- **Improved Answers:** LLM can reason about architecture and design
- **Efficient Retrieval:** Summaries help answer broad questions without needing all details
- **Multi-Level Understanding:** System can handle both "what" (code details) and "why" (design decisions)

---

## Configuration

### Key Parameters
- `DATA_PATH`: Directory containing Python source code
- `DB_CHROMA_PATH`: Path to store vector database
- `EMBEDDINGS_MODEL`: Model for generating embeddings (`thenlper/gte-large`)
- `chunk_size`: Size of code chunks (default: 2048)
- `chunk_overlap`: Overlap between chunks (default: 512)
- `k`: Number of chunks to retrieve per query (default: 6)

### LLM Configuration
- Base URL: `http://localhost:1234/v1` (LM Studio)
- Temperature: 0.0 (deterministic)
- Max tokens: 10000 (answers), 500 (summaries)

---

## Performance Considerations

### Ingestion Time
- File summary generation adds time during ingestion
- Trade-off: Longer ingestion for better query performance
- Can be disabled by passing `llm=None` to `get_chunks()`

### Query Time
- Slightly longer prompts due to file summaries
- Marginal increase in inference time
- Significant improvement in answer quality

---

## Future Enhancements

1. **Caching:** Cache file summaries to speed up re-ingestion
2. **Incremental Updates:** Update only changed files
3. **Multi-Language Support:** Extend beyond Python to other languages
4. **Hierarchical Retrieval:** First search summaries, then retrieve detailed chunks
5. **Cross-File Reasoning:** Explicitly model relationships between files

---

## Testing Recommendations

### Test Queries for Traceability
- "Where is the encode function defined?"
- "Which files handle tokenization?"
- "Show me the main entry point"

### Test Queries for Conceptual Reasoning
- "How is the tokenizer implemented?"
- "What is the overall architecture of the system?"
- "How do different modules interact?"
- "What design patterns are used?"

---

## Troubleshooting

### Issue: No file summaries generated
**Solution:** Ensure LM Studio is running and accessible at `http://localhost:1234/v1`

### Issue: Citations not appearing in answers
**Solution:** The LLM might not be following instructions. Try:
- Using a more instruction-following model
- Adjusting the prompt template
- Increasing temperature slightly

### Issue: Poor performance on conceptual questions
**Solution:** 
- Verify file summaries are present in metadata
- Increase the quality of file summaries by improving the summary prompt
- Ensure enough chunks are retrieved (increase `k` value)

---

## Summary

This implementation successfully addresses both hackathon tasks:

✅ **Task 1 (Traceability):** Every answer now includes explicit references to source files, both in the UI and within the generated text.

✅ **Task 2 (Conceptual Reasoning):** The system now generates and leverages file-level summaries to provide better context for answering high-level architectural and design questions.

The enhancements maintain backward compatibility while significantly improving the system's transparency and reasoning capabilities.

