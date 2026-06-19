"""
OpenAI protocol interface - works with LM Studio, Ollama, DeepSeek, OpenAI, grok, etc
"""
from openai import OpenAI
#
# from core.config import LM_STUDIO_URL, LM_STUDIO_API_KEY
#
# from core.config import DEEPSEEK_URL, DEEPSEEK_FIRST_API_KEY
# from core.config import DEEPSEEK_CHAT, DEEPSEEK_REASONER  # deepseek models
#
# from core.config import OPEN_ROUTER_BASE_URL, OPEN_ROUTER_DEEPSEEK_R1_API_KEY, OPEN_ROUTER_DEEPSEEK_R1_MODEL_NAME
# from core.config import GEMINI_FLASH_URL, GEMINI_FLASH_API_KEY, GEMINI_FLASH_MODEL
#
# from core.config import OPENAI_API_URL, OPENAI_API_KEY, OPENAI_MODEL
#

# --------------------- Define base_url and api_key ----------------------
# base_url = GEMINI_FLASH_URL  # DEEPSEEK_URL  # LM_STUDIO_URL
# api_key = GEMINI_FLASH_API_KEY  # DEEPSEEK_FIRST_API_KEY # LM_STUDIO_API_KEY
# model = GEMINI_FLASH_MODEL  # DEEPSEEK_CHAT  # r"gemma-2-9b-it"

# base_url = OPENAI_API_URL
# api_key = OPENAI_API_KEY
# model = OPENAI_MODEL  # r"gemma-2-9b-it"


# base_url = "http://192.168.68.107:1234/v1"  # LM_STUDIO_URL
base_url = "http://localhost:1234/v1"

api_key = "LM_STUDIO_API_KEY"
# model = r"gemma-2-9b-it"
model = r"google/gemma-3-12b"

# base_url = OPEN_ROUTER_BASE_URL
# api_key = OPEN_ROUTER_DEEPSEEK_R1_API_KEY
# model = OPEN_ROUTER_DEEPSEEK_R1_MODEL_NAME


# ------------------------------------------------------------------------
# create a client
client1 = OpenAI(base_url=base_url, api_key=api_key)  # html to json


def get_completion(prompt, client=client1, model=model):
    """
    given the prompt, obtain the response from LLM hosted by LM Studio as a server
    :param prompt: prompt to be sent to LLM server
    :return: response from the LLM
    """
    prompt = [
        {"role": "user", "content": prompt}
    ]
    completion = client.chat.completions.create(
        model=model,
        messages=prompt,
        temperature=0.0,
        stream=True,
    )
    new_message = {"role": "assistant", "content": ""}
    for chunk in completion:
        if chunk.choices[0].delta.content:
            # print(chunk.choices[0].delta.content, end="", flush=True)
            val = chunk.choices[0].delta.content
            new_message["content"] += val
    val = new_message["content"]  # .split("<end_of_turn>")[0]
    return val


def get_completion_messages(messages, client=client1, model=model):
    """
    given the prompt, obtain the response from LLM hosted by LM Studio as a server
    :param messages: messages for the LLM that contain the prompts
    :return: response from the LLM
    """
    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.0,
        # stream=False,
        # stream_options={"include_usage": True},
    )
    return completion.choices[0].message.content


def get_chat_completion_stream(messages):
    """
    Streams back tokens for the given messages.
    Yields chunks of text.
    """
    stream = client1.chat.completions.create(
        model=model,
        messages=messages,
        stream=True,
    )

    for chunk in stream:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content


if __name__ == '__main__':
    prompt = """
    What is machine learning in one line?
    """
    messages = [
        {
            "role": "system",
            "content": "You are a Professor in CS from Stanford."
        },

        {
            "role": "user",
            "content": prompt,
        }
    ]

    # results = get_completion_messages(messages)
    # print(results)

    response_text = ""
    for token in get_chat_completion_stream(messages):
        # For Streamlit, you can accumulate and display incrementally:
        response_text += token
        # print(token)
        print(response_text)
    #     # placeholder.write(response_text)
