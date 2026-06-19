from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
# from langchain.llms import CTransformers
# from ctransformers import AutoModelForCausalLM
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema import StrOutputParser

from ingest_model_card import EMBEDDINGS_MODEL, DB_CHROMA_PATH

from langchain import PromptTemplate
from langchain.llms import OpenAI
# from get_llm import load_llm_client

custom_prompt_template = """
You are an assistant for question-answering tasks.
Use the following pieces of retrieved context to answer the question. 
If you don't know the answer, just say that you don't know. 
Keep the answer precise but provide as much details as needed.
Question: {question} 
Context: {context} 
Answer: 
"""


def load_llm_client():
    """
    Load the llm client that is compatible with Langchain.
    Note that the client that is returned here is a langchain object and not a general openai client
    :return: langchain client supporting openai protocol
    """
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")  # html to json
    return client


def load_llm_remote():
    return OpenAI(base_url="http://192.168.68.108:1234/v1", api_key="lm-studio", temperature=0.0, max_tokens=10000)


def set_custom_prompt():
    prompt = PromptTemplate(template=custom_prompt_template, input_variables=['context', 'question'])
    return prompt


def format_docs(docs):
    """
    This is a function that is executed after retriever is invoked. The docs returned by the retriever are
    processed to extract the page_content strings and concatenated to construct the context variable.
    The output of this function is typically placed in a prompt, along with input query
    and sent to an LLM for final answer.
    :param docs: list of Langchain's document objects, each has metadata and page_content attributes.
    :return: string that is obtained by concatening page_content.
    """
    # you can process page_content as well as metadata
    # for doc in docs:  # for debugging and illustration we print the retrieved docs
    #     print(doc)
    print(docs[0])
    context_string = "\n\n".join([d.page_content for d in docs])
    # print(context_string)
    return context_string


# def load_llm_client():
#     """
#     Load the llm client that is compatible with Langchain.
#     Note that the client that is returned here is a langchain object and not a general openai client
#     :return: langchain client supporting openai protocol
#     """
#     client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")  # html to json
#     return client


def get_retriever():
    """
    after texts are ingested in vectordb, get it as a retriever
    :return:
    """
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDINGS_MODEL,
                                       model_kwargs={'device': 'cuda'})
    vectordb = Chroma(persist_directory=DB_CHROMA_PATH, embedding_function=embeddings)
    return vectordb


def naive_rag(query):
    """
    Given the query perform RAG and return the response
    :param query: user query text
    :return: results of naive RAG
    """
    vectordb = get_retriever()
    retriever = vectordb.as_retriever(search_kwargs={"k": 8})
    # llm = load_llm_client()
    llm = load_llm_remote()
    chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | set_custom_prompt()
            | llm
            | StrOutputParser()
    )

    print("Invoking query in naive RAG...")

    output = chain.invoke(query)

    print("output from naive RAG = ", output)

    return output


def qa_bot():
    vectordb = get_retriever()
    retriever = vectordb.as_retriever(search_kwargs={"k": 8})

    # llm = load_llm_client()
    llm = load_llm_remote()

    chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | set_custom_prompt()
            | llm
            | StrOutputParser()
    )

    while True:
        query = input("Your Query: ")
        if query != "quit":
            output = chain.invoke(query)
            print("-" * 100)
            print(output)
        else:
            break


if __name__ == '__main__':
    qa_bot()
    # inp = input("your Query: ")
    # results = naive_rag(inp)
    # print(results)


