"""
DEMO SCRIPT: Enhanced RAG System with Traceability & Conceptual Reasoning
==========================================================================

This demo shows:
1. OPTION A: Run ingestion (if time permits)
2. OPTION B: Show pre-ingested data (faster for demo)
3. Query the system with example questions
4. Demonstrate Task 1 (Traceability) and Task 2 (Conceptual Reasoning)
"""

import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import OpenAI

# Configuration - use absolute path to vector store
DB_CHROMA_PATH = "/Users/ashutoshkumv/Documents/gAi/vector_stores/db_chroma_code"
EMBEDDINGS_MODEL = "thenlper/gte-large"


def check_ingested_data():
    """
    Check if we have pre-ingested data in the vector store.
    This is useful for quick demos without re-running ingestion.
    """
    print("="*70)
    print("CHECKING PRE-INGESTED DATA")
    print("="*70)
    
    # Debug: show the path being checked
    print(f"\n🔍 Looking for data at:")
    print(f"   {DB_CHROMA_PATH}")
    
    if not os.path.exists(DB_CHROMA_PATH):
        print(f"\n❌ No pre-ingested data found at: {DB_CHROMA_PATH}")
        print("   You need to run ingestion first!")
        return False
    
    try:
        # Load the vector store
        embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDINGS_MODEL,
            model_kwargs={'device': 'cpu'}
        )
        vectordb = Chroma(
            persist_directory=DB_CHROMA_PATH, 
            embedding_function=embeddings
        )
        
        # Get collection stats
        collection = vectordb._collection
        count = collection.count()
        
        print(f"✅ Pre-ingested data found!")
        print(f"\n📊 Vector Store Statistics:")
        print(f"   • Location: {DB_CHROMA_PATH}")
        print(f"   • Total chunks: {count}")
        
        # Sample a few documents to show metadata
        if count > 0:
            sample_docs = vectordb.similarity_search("import", k=3)
            
            # Extract unique source files
            source_files = set()
            has_summaries = 0
            
            for doc in sample_docs:
                source = doc.metadata.get('source', 'unknown')
                source_files.add(source)
                if 'file_summary' in doc.metadata:
                    has_summaries += 1
            
            print(f"   • Unique source files (sample): {len(source_files)}")
            print(f"   • Chunks with summaries: {has_summaries}/{len(sample_docs)}")
            
            print(f"\n📁 Sample Source Files:")
            for src in list(source_files)[:3]:
                print(f"   • {os.path.basename(src)}")
            
            print(f"\n🔍 Sample Chunk Preview:")
            doc = sample_docs[0]
            print(f"   • Source: {os.path.basename(doc.metadata.get('source', 'unknown'))}")
            print(f"   • Content (first 150 chars): {doc.page_content[:150]}...")
            if 'file_summary' in doc.metadata:
                print(f"   • Has file summary: Yes ✓")
            else:
                print(f"   • Has file summary: No ⚠️")
        
        return True
        
    except Exception as e:
        print(f"❌ Error loading vector store: {e}")
        return False


def show_ingestion_process():
    """
    Show what the ingestion process does (without actually running it).
    Use this for quick demos when time is limited.
    """
    print("\n" + "="*70)
    print("INGESTION PROCESS OVERVIEW")
    print("="*70)
    
    print("""
The ingestion process (ingest_code.py) does the following:

STEP 1: Load Python Files
   → Scans directory: /Users/ashutoshkumv/nanochat/
   → Finds all .py files recursively
   → Uses LangChain's LanguageParser for Python

STEP 2: Generate File Summaries (⭐ TASK 2)
   → For each file, LLM generates a high-level summary
   → Summary includes: purpose, key components, architecture
   → This enables conceptual reasoning!

STEP 3: Split into Chunks
   → Uses RecursiveCharacterTextSplitter
   → Chunk size: 2048 chars
   → Chunk overlap: 512 chars (for context continuity)

STEP 4: Add Metadata (⭐ TASK 1 & 2)
   → Each chunk gets 'source' field (for traceability)
   → Each chunk gets 'file_summary' field (for conceptual reasoning)

STEP 5: Generate Embeddings
   → Uses HuggingFace model: thenlper/gte-large
   → Creates vector representations

STEP 6: Store in ChromaDB
   → Persists to: vector_stores/db_chroma_code
   → Ready for semantic search!
    """)


def run_ingestion():
    """
    Actually run the ingestion process.
    Use this when you have time and want to show live ingestion.
    """
    print("\n" + "="*70)
    print("RUNNING LIVE INGESTION")
    print("="*70)
    print("\n⚠️  This will take a few minutes depending on codebase size...")
    
    response = input("\nProceed with ingestion? (yes/no): ")
    if response.lower() != 'yes':
        print("Skipping live ingestion.")
        return False
    
    try:
        from ingest_code import ingest
        print("\n🚀 Starting ingestion...\n")
        ingest()
        print("\n✅ Ingestion completed successfully!")
        return True
    except Exception as e:
        print(f"\n❌ Ingestion failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def demo_query_system():
    """
    Demonstrate the query system with example questions.
    Shows both Task 1 (Traceability) and Task 2 (Conceptual Reasoning).
    """
    print("\n" + "="*70)
    print("DEMO: QUERYING THE ENHANCED RAG SYSTEM")
    print("="*70)
    
    try:
        # Load components
        embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDINGS_MODEL,
            model_kwargs={'device': 'cpu'}
        )
        vectordb = Chroma(
            persist_directory=DB_CHROMA_PATH, 
            embedding_function=embeddings
        )
        
        llm = OpenAI(
            base_url="http://localhost:1234/v1", 
            api_key="lm-studio", 
            temperature=0.0, 
            max_tokens=2000
        )
        
        print("\n✅ System loaded successfully!")
        print("\n" + "="*70)
        
        # Example queries demonstrating different capabilities
        example_queries = [
            {
                "query": "What is the main purpose of the tokenizer?",
                "type": "Conceptual (Task 2)",
                "description": "Tests file-level understanding"
            },
            {
                "query": "Show me the encode function",
                "type": "Specific Code (Task 1)",
                "description": "Tests source retrieval and citation"
            },
            {
                "query": "How do the different modules interact?",
                "type": "Architectural (Task 2)",
                "description": "Tests high-level reasoning"
            }
        ]
        
        print("\n📋 Example Queries Available:\n")
        for i, ex in enumerate(example_queries, 1):
            print(f"{i}. [{ex['type']}] {ex['query']}")
            print(f"   → {ex['description']}")
        
        print("\n" + "="*70)
        choice = input("\nSelect query (1-3) or enter custom query: ")
        
        if choice.isdigit() and 1 <= int(choice) <= len(example_queries):
            query = example_queries[int(choice)-1]['query']
        else:
            query = choice
        
        print(f"\n🔍 Query: {query}")
        print("-"*70)
        
        # Retrieve and display results
        retriever = vectordb.as_retriever(search_kwargs={"k": 6})
        docs = retriever.invoke(query)
        
        print(f"\n✅ Retrieved {len(docs)} relevant chunks")
        
        # Extract source files (Task 1: Traceability)
        source_files = set()
        file_summaries = {}
        
        for doc in docs:
            source = doc.metadata.get('source', 'unknown')
            source_files.add(source)
            
            if 'file_summary' in doc.metadata and source not in file_summaries:
                file_summaries[source] = doc.metadata['file_summary']
        
        # Display Task 1: Traceability
        print(f"\n📂 SOURCE FILES REFERENCED (Task 1 - Traceability):")
        print(f"   Total files: {len(source_files)}")
        for src in sorted(source_files):
            print(f"   • {os.path.basename(src)}")
        
        # Display Task 2: Conceptual Context
        if file_summaries:
            print(f"\n🧠 FILE-LEVEL SUMMARIES (Task 2 - Conceptual Reasoning):")
            for src, summary in list(file_summaries.items())[:2]:  # Show first 2
                print(f"\n   📄 {os.path.basename(src)}:")
                print(f"      {summary[:200]}...")
        
        # Format context
        formatted_chunks = []
        for doc in docs:
            filename = os.path.basename(doc.metadata.get('source', 'unknown'))
            chunk_text = f"[From: {filename}]\n{doc.page_content}"
            formatted_chunks.append(chunk_text)
        
        context = "\n\n---\n\n".join(formatted_chunks)
        
        summaries_text = "\n".join([
            f"• {os.path.basename(src)}: {summary}" 
            for src, summary in file_summaries.items()
        ])
        
        # Generate answer
        prompt = f"""
You are an assistant for question-answering tasks pertaining to Python source code.

IMPORTANT: Always cite the source file(s) you're referencing using [Source: filename.py]

Question: {query}

File-Level Context:
{summaries_text}

Detailed Code Context:
{context}

Answer (with source citations):
"""
        
        print(f"\n💭 Generating answer with LLM...\n")
        result = llm.invoke(prompt)
        
        print("="*70)
        print("ANSWER:")
        print("="*70)
        print(result)
        print("="*70)
        
        # Highlight what was demonstrated
        print("\n✨ DEMONSTRATION SUMMARY:")
        print(f"   ✅ Task 1 (Traceability): Showed {len(source_files)} source files")
        print(f"   ✅ Task 2 (Conceptual Reasoning): Used {len(file_summaries)} file summaries")
        print(f"   ✅ Answer includes [Source: ...] citations")
        
    except Exception as e:
        print(f"\n❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()


def main():
    """
    Main demo flow - choose your path based on available time and data.
    """
    print("\n" + "="*70)
    print("ENHANCED RAG SYSTEM DEMO")
    print("Tasks: (1) Traceability + (2) Conceptual Reasoning")
    print("="*70)
    
    print("""
Select Demo Mode:

1. QUICK DEMO - Show pre-ingested data (5 minutes)
   → Check existing vector store
   → Explain ingestion process
   → Run example queries

2. FULL DEMO - Run live ingestion (15-20 minutes)
   → Actually ingest codebase
   → Show real-time processing
   → Run example queries

3. QUERY ONLY - Skip to querying (2 minutes)
   → Assumes data is already ingested
   → Jump straight to examples
    """)
    
    choice = input("Your choice (1/2/3): ")
    
    if choice == "1":
        # Quick demo with pre-ingested data
        has_data = check_ingested_data()
        if has_data:
            show_ingestion_process()
            demo_query_system()
        else:
            print("\n⚠️  No pre-ingested data found!")
            print("Run option 2 first to ingest data.")
    
    elif choice == "2":
        # Full demo with live ingestion
        show_ingestion_process()
        success = run_ingestion()
        if success:
            check_ingested_data()
            demo_query_system()
    
    elif choice == "3":
        # Query only
        demo_query_system()
    
    else:
        print("Invalid choice!")
    
    print("\n" + "="*70)
    print("DEMO COMPLETE")
    print("="*70)


if __name__ == '__main__':
    main()

