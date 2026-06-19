"""
Naive RAG - Implementation Example

"""
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from traceback import print_exc
import json
import os
import frontmatter

# Disable tokenizers parallelism warning
os.environ["TOKENIZERS_PARALLELISM"] = "false"


DATA_PATH = "/Users/ashutoshkumv/Documents/gAi/session5_rag/code/dataset/"
# DATA_PATH = r"C:\home\ananth\research\datasets\budget_datasets"
DB_CHROMA_PATH = "vector_stores/db_chroma_model_card"
EMBEDDINGS_MODEL = "thenlper/gte-large"


class ModelCardLoader:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load(self):
        # Parse YAML frontmatter
        post = frontmatter.load(self.file_path)
        content = post.content.strip()

        # Remove noise (license/legal text)
        noise_headers = [
            "### LLAMA 2 COMMUNITY LICENSE AGREEMENT",
            "### Acceptable Use Policy",
            "Disclaimer:"
        ]
        for header in noise_headers:
            content = content.replace(header, "").strip()

        # Extract essential metadata
        metadata = {
            "license": post.metadata.get("license", "unknown"),
            # "tags": post.metadata.get("tags", []),
            "model_name": post.metadata.get("name", "unknown"),
            "source": self.file_path
        }

        # data1 = json.dumps(metadata)

        return [Document(page_content=content, metadata=metadata)]


def get_docs():
    """
    loads the documents from the given source where each doc has page_content and metadata.
    It is possible to add metadata by updating the doc.metadata which is a dict()
    :return:
    """
    # loader = DirectoryLoader(DATA_PATH, glob="*.pdf", loader_cls=PyPDFLoader, recursive=True)
    loader = ModelCardLoader(DATA_PATH)
    docs = loader.load()
    return docs


def get_chunks(docs, chunk_size=512, chunk_overlap=50):
    """
    Given docs obtained by using LangChain loader, split these to chunks and return them
    :param docs: documents returned by loader, that could be ArxivLoader or local directory loader
    :param chunk_size: size of chunk to be set according to the application
    :param chunk_overlap: overlap window size between consecutive chunks
    :return: chunks
    """
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    texts = text_splitter.split_documents(docs)
    return texts


def get_embeddings_model(model_name=None, device="cuda"):
    if model_name is None:
        model_name = EMBEDDINGS_MODEL
    embeddings_model = HuggingFaceEmbeddings(model_name=model_name,
                                             model_kwargs={"device": device},
                                            )
    # embeddings_model = AutoModel.from_pretrained(model_name, trust_remote_code=True)
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
    :param source: Can be "arxiv" to load from arxiv web site, "local" for DirectoryLoader
    :return:
    """

    # 1. Load the data from the data source
    docs = get_docs()
    print(docs[0])
    # docs = get_docs(source="arxiv")
    # return
    # 2. Chunk the documents
    texts = get_chunks(docs)
    print(len(docs), len(texts))

    # 3. get the embedding model
    embs_model = get_embeddings_model(device="cpu")

    # 4. Use the embedding model to vectorize and save it in db
    flag = create_vector_store(texts, embs_model, DB_CHROMA_PATH, use_db="chroma")
    if flag:
        print("Vector Store Created!")


def get_retriever():
    """
    after texts are ingested in vectordb, get it as a retriever
    :return:
    """
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDINGS_MODEL,
                                       model_kwargs={'device': 'cpu'})
    vectordb = Chroma(persist_directory=DB_CHROMA_PATH, embedding_function=embeddings)
    return vectordb.as_retriever(search_kwargs={"k": 8})


if __name__ == '__main__':
    ingest()


