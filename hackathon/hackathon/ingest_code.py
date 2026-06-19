"""
Naive RAG - Implementation Example
Ingest source code - python source code
Enhanced with file-level summaries for conceptual reasoning
"""
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from traceback import print_exc
import os
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser
from langchain_text_splitters import Language, RecursiveCharacterTextSplitter
from langchain_community.llms import OpenAI

# DATA_PATH = r"C:\home\ananth\research\packages\nanochat"
DATA_PATH = r"/Users/ashutoshkumv/nanochat/"

CONTENT_ID = "code"
DB_CHROMA_PATH = "vector_stores/db_chroma" + "_" + CONTENT_ID
EMBEDDINGS_MODEL = "thenlper/gte-large"


def generate_file_summary(file_content, file_path, llm):
    """
    Generate a high-level summary of the file for conceptual reasoning.
    This summary captures the purpose, key components, and main functionality.
    """
    summary_prompt = f"""
Analyze the following Python source code file and provide a concise summary (3-5 sentences) covering:
1. Main purpose and functionality
2. Key classes, functions, or components
3. How this file fits into the overall system architecture

File: {file_path}
Code:
{file_content[:2000]}  # Use first 2000 chars for context

Summary:"""
    
    try:
        summary = llm.invoke(summary_prompt)
        return summary.strip()
    except Exception as e:
        print(f"Error generating summary for {file_path}: {e}")
        return f"File containing Python code from {os.path.basename(file_path)}"


def get_docs():
    loader = GenericLoader.from_filesystem(
        DATA_PATH,
        # glob="*",  # not recursive
        glob="**/*",  # Recursive glob
        suffixes=[".py"],
        parser=LanguageParser(language="python"),
    )
    docs = loader.load()
    return docs


def get_chunks(docs, chunk_size=2048, chunk_overlap=512, llm=None):
    """
    Given docs obtained by using LangChain loader, split these to chunks and return them.
    Enhanced to add file-level summaries to metadata for conceptual reasoning.
    :param docs: documents returned by loader, that could be ArxivLoader or local directory loader
    :param llm: Language model for generating file summaries
    :return: chunks with enhanced metadata
    """
    py_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.PYTHON, chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    texts = py_splitter.split_documents(docs)
    
    # Group chunks by source file and add file-level summaries
    file_summaries = {}
    if llm:
        print("Generating file-level summaries for conceptual reasoning...")
        for doc in docs:
            source_path = doc.metadata.get('source', 'unknown')
            if source_path not in file_summaries:
                summary = generate_file_summary(doc.page_content, source_path, llm)
                file_summaries[source_path] = summary
                print(f"Generated summary for: {os.path.basename(source_path)}")
    
    # Add file summary to each chunk's metadata
    for text_chunk in texts:
        source_path = text_chunk.metadata.get('source', 'unknown')
        if source_path in file_summaries:
            text_chunk.metadata['file_summary'] = file_summaries[source_path]
        # Ensure source is always present for traceability
        if 'source' not in text_chunk.metadata:
            text_chunk.metadata['source'] = 'unknown'
    
    print(f"Processed {len(texts)} chunks from {len(file_summaries)} files")
    return texts


def get_embeddings_model(model_name=None, device="cuda"):
    if model_name is None:
        model_name = EMBEDDINGS_MODEL
    embeddings_model = HuggingFaceEmbeddings(model_name=model_name,
                                       model_kwargs={"device": device})
    return embeddings_model


def create_vector_store(texts, embeddings, db_path, use_db="chroma"):
    """
    Given the chunks, their embeddings and path to save the db, save and persist the data in the data store
    :param texts: chunks for which we are constructing the data store
    :param embeddings: vector embeddings for given chunks
    :param db_path: storage path
    :param use_db: type of data store to use
    :return: None
    """
    flag = True
    try:
        if use_db == "chroma":
            db = Chroma.from_documents(texts, embeddings, persist_directory=db_path)
        else:
            print("Unknown db type, exiting!")
            db = None
            import sys
            sys.exit(-1)
        db.persist()
    except:
        flag = False
        print_exc()
        print("Exception when creating data store: ", db_path, use_db)
    return flag


def ingest():
    """
    Ingest Python source code files from the given data source.
    Enhanced to generate file-level summaries for better conceptual reasoning.
    :return:
    """

    # 1. Load the data from the data source
    docs = get_docs()
    print(f"Loaded {len(docs)} documents")

    # 2. Initialize LLM for generating file summaries
    print("Initializing LLM for file summary generation...")
    try:
        llm = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio", 
                     temperature=0.0, max_tokens=500)
        print("LLM initialized successfully")
    except Exception as e:
        print(f"Warning: Could not initialize LLM: {e}")
        print("Proceeding without file summaries...")
        llm = None

    # 3. Split into chunks with file-level summaries
    texts = get_chunks(docs, llm=llm)
    print(f"Total documents: {len(docs)}, Total chunks: {len(texts)}")

    # 4. Create embeddings and vector store
    embs_model = get_embeddings_model(device="cpu")
    flag = create_vector_store(texts, embs_model, DB_CHROMA_PATH, use_db="chroma")
    if flag:
        print("Vector Store Created with Enhanced Metadata!")
        print("✓ Task 1: Traceability metadata added (source field)")
        print("✓ Task 2: File-level summaries added for conceptual reasoning")


if __name__ == '__main__':
    ingest()


