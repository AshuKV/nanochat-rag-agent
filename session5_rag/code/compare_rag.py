"""
compare_rag.py
Solution code for classroom exercise: improving multi-company retrieval.
"""
import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from ingest import EMBEDDINGS_MODEL, DB_CHROMA_PATH

# Disable tokenizers parallelism warning
os.environ["TOKENIZERS_PARALLELISM"] = "false"


# ---- Custom Prompt ----
custom_prompt_template = """You are an assistant for question-answering tasks.
Use the following pieces of retrieved context to answer the question.
If you don't know the answer, say that you don't know.

Question: {question}

Context:
{context}

Answer:"""


def set_custom_prompt():
    return PromptTemplate(
        template=custom_prompt_template,
        input_variables=["context", "question"]
    )


def load_llm_client():
    return OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")


def get_retriever():
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDINGS_MODEL,
        model_kwargs={"device": "cpu"}
    )
    vectordb = Chroma(
        persist_directory=DB_CHROMA_PATH,
        embedding_function=embeddings
    )
    return vectordb.as_retriever(search_kwargs={"k": 4})


def format_docs(docs):
    return "\n\n".join([d.page_content for d in docs])


def company_aware_rag(query, company_names=["Adobe", "Microsoft"]):
    retriever = get_retriever()
    llm = load_llm_client()
    prompt_template = set_custom_prompt()
    
    all_contexts = []
    for company in company_names:
        sub_query = f"{query} related to {company}"
        docs = retriever.invoke(sub_query)
        context = format_docs(docs)
        all_contexts.append(f"Context for {company}:\n{context}")
    
    full_context = "\n\n".join(all_contexts)
    full_prompt = prompt_template.format(context=full_context, question=query)
    output = llm.invoke(full_prompt)
    return output


if __name__ == "__main__":
    print("---- Multi-company RAG ----")
    query = input("Enter your query: ")
    print("Generating answer...\n")
    response = company_aware_rag(query, ["Adobe", "Microsoft"])
    print("-" * 100)
    print(response)
