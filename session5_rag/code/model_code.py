"""
model for generating and reviewing code using RAG
"""
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import OpenAI

from ingest_code import EMBEDDINGS_MODEL, DB_CHROMA_PATH
from langchain import PromptTemplate

custom_prompt_template = """
You are an assistant for question-answering tasks pertaining to Python source code.
Use the following pieces of retrieved context to answer the question. 
If you don't know the answer, just say that you don't know. 
When a function definition is asked please provide the full function source code.
Question: {question} 
Context: {context} 
Answer: 
"""


def set_custom_prompt():
    prompt = PromptTemplate.from_template(template=custom_prompt_template)
    return prompt


def format_docs(docs):
    # for doc in docs:
    #     print(doc)
    return "\n\n".join([d.page_content for d in docs])


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
                                       model_kwargs={'device': 'cuda'})
    vectordb = Chroma(persist_directory=DB_CHROMA_PATH, embedding_function=embeddings)
    return vectordb


def qa_bot():
    vectordb = get_retriever()
    retriever = vectordb.as_retriever(search_kwargs={"k": 6})

    # llm = load_llm()
    llm = load_llm_remote()
    print("LLM Loaded: ", llm)

    query = ""
    while query != "quit":
        query = input("Your Query: ")
        retrieved_docs = retriever.invoke(query)
        # print("Num retrieved docs = ", len(retrieved_docs))
        # print(retrieved_docs[0].page_content)
        context = format_docs(retrieved_docs)
        prompt = set_custom_prompt()
        prompt = prompt.format(context=context, question=query)
        result = llm(prompt)

        print(result)


qa_bot()



