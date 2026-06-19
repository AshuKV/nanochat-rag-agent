# Task 1: RAG Query Agent - Quick Start Guide

This guide will help you get started with the RAG Query Agent in under 5 minutes.

## Prerequisites Check

Before starting, ensure you have:
- ✅ Python 3.8 or higher
- ✅ LM Studio or compatible LLM server running
- ✅ Vector database created (NanoChat codebase ingested)

## Step 1: Verify LLM Server (30 seconds)

Open your browser and check:
```
http://localhost:1234/v1
```

You should see a response indicating the server is running.

**OR** Start LM Studio:
1. Open LM Studio
2. Load a model (e.g., llama3.2:latest)
3. Start the server on port 1234

## Step 2: Quick Test (1 minute)

Open Python and run:

```python
from rag_query_agent import RAGQueryAgent

# Initialize
agent = RAGQueryAgent()

# Ask a question
result = agent.query("What is NanoChat?")

# View answer
print(result["answer"])
```

**Expected Output**: A detailed answer about the NanoChat codebase with source references.

## Step 3: Try Interactive Mode (2 minutes)

Run the interactive CLI:

```bash
python rag_query_agent.py
```

Try these questions:
1. "What is the main purpose of this codebase?"
2. "How is message routing implemented?"
3. "What are the key features?"
4. Type `quit` to exit

## Step 4: Run Demo Notebook (5 minutes)

```bash
jupyter notebook task1_rag_agent_demo.ipynb
```

Run all cells to see various examples and capabilities.

## Step 5: Run Tests (3 minutes)

Validate the installation:

```bash
python test_rag_agent.py
```

For a quick test:
```bash
python test_rag_agent.py --quick
```

## Common Usage Patterns

### Pattern 1: Single Question
```python
from rag_query_agent import RAGQueryAgent

agent = RAGQueryAgent()
answer = agent.query_simple("Your question here")
print(answer)
```

### Pattern 2: Detailed Query
```python
from rag_query_agent import RAGQueryAgent

agent = RAGQueryAgent()
result = agent.query("Your question here")

print(f"Answer: {result['answer']}")
print(f"Sources: {result['sources']}")
```

### Pattern 3: Tool Interface (for LangGraph)
```python
from rag_query_agent import rag_tool

answer = rag_tool("Your question here")
print(answer)
```

### Pattern 4: Command Line
```bash
# Single question
python rag_query_agent.py --question "What is NanoChat?"

# Interactive mode
python rag_query_agent.py

# With custom settings
python rag_query_agent.py --question "Your question" --k 10 --temperature 0.1
```

## Troubleshooting

### Problem: "Connection refused"
**Solution**: Start your LLM server
```bash
# For LM Studio: Start server in UI
# For local model: Check if server is running on localhost:1234
```

### Problem: "Vector database not found"
**Solution**: Create the vector database
```bash
python ingest.py
```

### Problem: "Module not found"
**Solution**: Install dependencies
```bash
pip install langchain langchain-openai langchain-community chromadb sentence-transformers
```

### Problem: Slow responses
**Solutions**:
- Use a smaller model in LM Studio
- Reduce k_retrieval: `agent = RAGQueryAgent(k_retrieval=5)`
- Use GPU if available: `agent = RAGQueryAgent(device="cuda")`

## Next Steps

1. ✅ **Read Full Documentation**: See `TASK1_README.md` for comprehensive guide
2. ✅ **Explore Demo Notebook**: Run `task1_rag_agent_demo.ipynb`
3. ✅ **Integration**: Use `rag_tool` in your LangGraph workflows (Task 4)
4. ✅ **Customization**: Adjust parameters for your use case

## Example Questions to Try

### General Understanding
- "What is the purpose of this codebase?"
- "What are the main components?"
- "What technologies are used?"

### Technical Details
- "How is message routing implemented?"
- "What functions handle authentication?"
- "How is error handling done?"

### Architecture
- "Describe the overall architecture"
- "How are modules organized?"
- "What design patterns are used?"

### Code Specifics
- "Show me the main entry point"
- "What are the key classes?"
- "How is configuration managed?"

## Performance Expectations

Typical response times:
- **Retrieval**: 100-200ms
- **LLM Generation**: 2-5 seconds
- **Total**: 2-7 seconds per query

## Need Help?

1. **Check Logs**: Look for error messages in console output
2. **Test Components**: Run `python test_rag_agent.py` to identify issues
3. **Review Documentation**: See `TASK1_README.md` for detailed information
4. **Verify Setup**: Ensure LLM server and vector DB are working

## Success Indicators

You're ready to proceed if:
- ✅ Agent initializes without errors
- ✅ Queries return relevant answers
- ✅ Source files are referenced
- ✅ Responses are coherent and technical
- ✅ Test suite passes (at least 8/10 tests)

## What's Next: Task 4 Integration

This RAG Query Agent will be integrated into Task 4's multi-agent workflow:

```python
from langgraph.graph import StateGraph
from rag_query_agent import rag_tool

# Add RAG tool to your agent
tools = [rag_tool, other_tools...]

# Use in LangGraph workflow
graph = StateGraph(AgentState)
# ... add nodes and edges ...
```

---

**Congratulations!** 🎉 You're now ready to use the RAG Query Agent for answering technical questions about the NanoChat codebase.






