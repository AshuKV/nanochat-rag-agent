from langchain_openai import ChatOpenAI
from core.config import LM_STUDIO_URL
from core.config import LM_STUDIO_API_KEY


def get_llm(base_url=LM_STUDIO_URL, api_key=LM_STUDIO_API_KEY, temperature=0):
    """
    for the llm server running under LM Studio, get a Langchain llm client object.
    Use this if you are creating a langchain workflow that uses LLM as a local server.
    If you are not using langchain, use huggingface transformers to load the llm file or use get_completion() client.

    :param temperature: between 0 to 1, 0 for no creativity and 1 for maximum creativity due to variance
    :return:
    """
    llm = ChatOpenAI(
        base_url=base_url,
        temperature=temperature,
        api_key=api_key
    )
    return llm


if __name__ == '__main__':
    llm = get_llm()
    response = llm.invoke("hi I am Ananth!")
    print(response.content)
    print(response.response_metadata)

