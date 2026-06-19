import openai
import ollama

from core.config import OPENAI_API_KEY, OPENAI_MODEL
from core.config import OLLAMA_LLAMA3_MODEL, OLLAMA_GEMMA2_2B_MODEL, OLLAMA_GEMMA3_12B_MODEL

# Choose whether to use OpenAI API or Ollama
USE_OPENAI = False  # Set to True for OpenAI, False for Ollama


# Function to get AI response
def get_response(user_prompt, system_prompt="You are a helpful assistant."):
    if USE_OPENAI:
        openai.api_key = OPENAI_API_KEY
        response = openai.ChatCompletion.create(
            model=OPENAI_MODEL,  # Change model if needed
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7
        )
        return response["choices"][0]["message"]["content"]

    else:
        response = ollama.chat(
            model="gemma3:12b",  # Change to any available model
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        return response["message"]["content"]


# Function to get AI response
def get_response_for_messages(messages):
    response = ollama.chat(
        model=OLLAMA_GEMMA3_12B_MODEL,  # Change to any available model
        messages=messages,
    )
    return response["message"]["content"]


if __name__ == '__main__':
    import os
    test_dir = r"C:\home\ananth\research\my_projects\mar_apr_2025\core\session_1_overview\testcases"
    # name = "page_1.png"
    name = "benz7.jpg"
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant"
        },
        {
            'role': 'user',
            'content': """
            Describe the given image.
            """,
            'images': [os.path.join(test_dir, name)]
        }
    ]

    results = get_response_for_messages(messages)

    print(results)

