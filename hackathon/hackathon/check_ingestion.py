"""
Quick script to check if data has been ingested and show statistics.
Run this before your demo to verify everything is ready!
"""

import os

# Configuration - use absolute path to vector store
DB_CHROMA_PATH = "/Users/ashutoshkumv/Documents/gAi/vector_stores/db_chroma_code"
EMBEDDINGS_MODEL = "thenlper/gte-large"


def check_ingestion_status():
    """
    Quick check if ingestion has been completed.
    Shows statistics about the ingested data.
    """
    print("="*70)
    print("INGESTION STATUS CHECK")
    print("="*70)
    
    # Debug: show the path being checked
    abs_path = os.path.abspath(DB_CHROMA_PATH)
    print(f"\n🔍 Looking for data at: {DB_CHROMA_PATH}")
    print(f"   Absolute path: {abs_path}")
    
    # Check if vector store directory exists
    if not os.path.exists(DB_CHROMA_PATH):
        print(f"\n❌ NO INGESTED DATA FOUND")
        print(f"\n📍 Expected location: {DB_CHROMA_PATH}")
        print("\n🔧 To ingest data, run:")
        print("   python ingest_code.py")
        return False
    
    print(f"\n✅ Vector store found at: {DB_CHROMA_PATH}")
    
    try:
        from langchain_community.vectorstores import Chroma
        from langchain_community.embeddings import HuggingFaceEmbeddings
        
        # Load vector store
        print("\n⏳ Loading vector store...")
        embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDINGS_MODEL,
            model_kwargs={'device': 'cpu'}
        )
        
        vectordb = Chroma(
            persist_directory=DB_CHROMA_PATH, 
            embedding_function=embeddings
        )
        
        # Get statistics
        collection = vectordb._collection
        total_chunks = collection.count()
        
        print(f"\n📊 INGESTION STATISTICS:")
        print(f"   • Total chunks: {total_chunks}")
        
        if total_chunks == 0:
            print("\n⚠️  Vector store is empty!")
            print("   Run: python ingest_code.py")
            return False
        
        # Sample some documents to check metadata
        print(f"\n🔍 Checking metadata quality...")
        sample_docs = vectordb.similarity_search("import", k=10)
        
        # Analyze metadata
        source_files = set()
        chunks_with_source = 0
        chunks_with_summary = 0
        
        for doc in sample_docs:
            if 'source' in doc.metadata:
                chunks_with_source += 1
                source = doc.metadata['source']
                source_files.add(source)
            
            if 'file_summary' in doc.metadata:
                chunks_with_summary += 1
        
        print(f"\n📁 Source Files (sample of {len(source_files)}):")
        for src in list(source_files)[:5]:
            print(f"   • {os.path.basename(src)}")
        if len(source_files) > 5:
            print(f"   ... and {len(source_files) - 5} more")
        
        print(f"\n✅ METADATA QUALITY:")
        print(f"   • Chunks with 'source' field: {chunks_with_source}/{len(sample_docs)} (Task 1)")
        print(f"   • Chunks with 'file_summary': {chunks_with_summary}/{len(sample_docs)} (Task 2)")
        
        # Show sample chunk
        if sample_docs:
            print(f"\n📄 SAMPLE CHUNK:")
            doc = sample_docs[0]
            source = doc.metadata.get('source', 'unknown')
            print(f"   Source: {os.path.basename(source)}")
            print(f"   Content: {doc.page_content[:150]}...")
            
            if 'file_summary' in doc.metadata:
                print(f"   Summary: {doc.metadata['file_summary'][:150]}...")
        
        # Final verdict
        print(f"\n" + "="*70)
        
        if chunks_with_source == len(sample_docs) and chunks_with_summary > 0:
            print("✅ SYSTEM READY FOR DEMO!")
            print(f"   ✓ Task 1 (Traceability): Source metadata present")
            print(f"   ✓ Task 2 (Conceptual Reasoning): File summaries present")
            print("\n🚀 You can now run:")
            print("   python demo_notebook.py")
            print("   OR")
            print("   jupyter notebook demo.ipynb")
        elif chunks_with_source == len(sample_docs):
            print("⚠️  PARTIAL INGESTION")
            print(f"   ✓ Task 1 metadata present")
            print(f"   ✗ Task 2 metadata missing")
            print("\n💡 Re-run ingestion with LLM to add file summaries:")
            print("   python ingest_code.py")
        else:
            print("⚠️  METADATA INCOMPLETE")
            print("\n💡 Re-run ingestion:")
            print("   python ingest_code.py")
        
        print("="*70)
        return True
        
    except Exception as e:
        print(f"\n❌ Error checking vector store: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    check_ingestion_status()

