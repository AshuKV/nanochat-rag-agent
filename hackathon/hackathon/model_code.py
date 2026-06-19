"""
model for generating and reviewing code using RAG
Enhanced with:
- Task 1: Traceability - explicit source file references
- Task 2: Conceptual Reasoning - leveraging file-level summaries
"""
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import OpenAI
import os
from collections import defaultdict

from ingest_code import EMBEDDINGS_MODEL, DB_CHROMA_PATH
from langchain_core.prompts import PromptTemplate

# Enhanced prompt template that uses file summaries for conceptual reasoning
custom_prompt_template = """
You are an assistant for question-answering tasks pertaining to Python source code.

You have access to:
1. Code snippets from specific files
2. High-level file summaries describing overall purpose and architecture

Use the following information to answer the question. 
If you don't know the answer, just say that you don't know. 
When a function definition is asked, provide the full function source code.

IMPORTANT: Always cite the source file(s) you're referencing in your answer using the format:
[Source: filename.py]

Question: {question}

File-Level Context (for conceptual understanding):
{file_summaries}

Detailed Code Context:
{context}

Answer (remember to cite sources):
"""


def set_custom_prompt():
    prompt = PromptTemplate.from_template(template=custom_prompt_template)
    return prompt


def format_docs_with_metadata(docs):
    """
    Format documents with source file information for traceability (Task 1).
    Extract file summaries for conceptual reasoning (Task 2).
    
    Returns: (formatted_context, file_summaries_text, source_files)
    """
    formatted_chunks = []
    file_summaries = {}
    source_files = set()
    
    for i, doc in enumerate(docs):
        source = doc.metadata.get('source', 'unknown')
        source_files.add(source)
        filename = os.path.basename(source)
        
        # Format chunk with source attribution
        chunk_text = f"[From: {filename}]\n{doc.page_content}"
        formatted_chunks.append(chunk_text)
        
        # Collect file summaries for conceptual reasoning
        if 'file_summary' in doc.metadata and source not in file_summaries:
            file_summaries[source] = doc.metadata['file_summary']
    
    # Format the context
    context = "\n\n---\n\n".join(formatted_chunks)
    
    # Format file summaries
    summaries_text = ""
    if file_summaries:
        summaries_text = "\n".join([
            f"• {os.path.basename(src)}: {summary}" 
            for src, summary in file_summaries.items()
        ])
    else:
        summaries_text = "No file-level summaries available."
    
    return context, summaries_text, source_files


def format_docs(docs):
    """Legacy function - kept for compatibility"""
    context, _, _ = format_docs_with_metadata(docs)
    return context


def load_llm():
    return OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio", temperature=0.0, max_tokens=10000)


def load_llm_remote():
    return OpenAI(base_url="http://192.168.68.108:1234/v1", api_key="lm-studio", temperature=0.0, max_tokens=10000)


def get_retriever():
    """
    after texts are ingested in vectordb, get it as a retriever
    :return:
    """
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDINGS_MODEL,
                                       model_kwargs={'device': 'cpu'})
    vectordb = Chroma(persist_directory=DB_CHROMA_PATH, embedding_function=embeddings)
    return vectordb


def qa_bot():
    """
    Enhanced QA bot with:
    - Task 1: Traceability - shows source files referenced
    - Task 2: Conceptual Reasoning - uses file-level summaries
    """
    vectordb = get_retriever()
    retriever = vectordb.as_retriever(search_kwargs={"k": 6})

    llm = load_llm()
    # llm = load_llm_remote()
    print("LLM Loaded: ", llm)
    print("\n" + "="*70)
    print("Enhanced RAG for Code Intelligence")
    print("✓ Task 1: Traceability - Source files are cited in answers")
    print("✓ Task 2: Conceptual Reasoning - File summaries used for context")
    print("="*70 + "\n")

    query = ""
    while query != "quit":
        query = input("\nYour Query (or 'quit' to exit): ")
        if query == "quit":
            break
            
        print("\n" + "-"*70)
        
        # Retrieve relevant documents
        retrieved_docs = retriever.invoke(query)
        print(f"Retrieved {len(retrieved_docs)} relevant code chunks")
        
        # Format with metadata for traceability and conceptual reasoning
        context, file_summaries, source_files = format_docs_with_metadata(retrieved_docs)
        
        # Display source files for transparency (Task 1: Traceability)
        print(f"\n📂 Source Files Referenced ({len(source_files)}):")
        for src in sorted(source_files):
            print(f"   • {os.path.basename(src)}")
        
        # Generate answer using enhanced prompt
        prompt = set_custom_prompt()
        formatted_prompt = prompt.format(
            context=context, 
            question=query,
            file_summaries=file_summaries
        )
        
        print("\n💭 Generating answer...")
        result = llm.invoke(formatted_prompt)

        print("\n" + "="*70)
        print("ANSWER:")
        print("="*70)
        print(result)
        print("="*70)


if __name__ == '__main__':
    qa_bot()



