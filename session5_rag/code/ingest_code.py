"""
Naive RAG - Implementation Example
Ingest source code - python source code
"""
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from traceback import print_exc

from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser
from langchain_text_splitters import Language, RecursiveCharacterTextSplitter

DATA_PATH = r"C:\home\ananth\research\packages\nanochat"

CONTENT_ID = "code"
DB_CHROMA_PATH = "vector_stores/db_chroma" + "_" + CONTENT_ID
EMBEDDINGS_MODEL = "thenlper/gte-large"


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


def get_chunks(docs, chunk_size=2048, chunk_overlap=512):
    """
    Given docs obtained by using LangChain loader, split these to chunks and return them
    :param docs: documents returned by loader, that could be ArxivLoader or local directory loader
    :return: chunks
    """
    py_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.PYTHON, chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    texts = py_splitter.split_documents(docs)
    print(texts)
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
    Ingest PDF files from the given data source.
    :return:
    """

    # 1. Load the data from the data source
    docs = get_docs()
    # print(docs[0])
    # docs = get_docs(source="arxiv")

    texts = get_chunks(docs)
    # texts = docs

    print(len(docs), len(texts))

    embs_model = get_embeddings_model(device="cuda")
    flag = create_vector_store(texts, embs_model, DB_CHROMA_PATH, use_db="chroma")
    if flag:
        print("Vector Store Created!")


if __name__ == '__main__':
    ingest()


