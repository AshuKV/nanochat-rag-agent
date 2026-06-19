from openai import OpenAI

base_url = "http://localhost:11434/v1"
# base_url = "http://192.168.68.130:11434/v1"

client = OpenAI(
    base_url=base_url,  #
    api_key='ollama',  # required, but unused
)


def get_completion_ollama(messages, model="gemma3:12b"):
    """
    Given the prompt messages in OpenAI protocol, runs this as a client to Ollama and returns the results
    :param messages: list of messages constituting a prompt
    :param model: model to invoke
    :return: response (results) as a string
    """
    response = client.chat.completions.create(
      model=model,
      messages=messages
    )
    output = response.choices[0].message.content
    return output


if __name__ == '__main__':
    query = """
    Andrej Karpathy said recently: "The best programming language today is English".
    Do you agree?
    """
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": query},
        # {"role": "assistant", "content": "Yes there is a point in what he said."},
        # {"role": "user", "content": "Explain your answer in detail."}
    ]

    results = get_completion_ollama(messages)
    print(results)
    # print("-" * 100)
    # messages = [
    #     {"role": "system", "content": "You are a helpful assistant."},
    #     {"role": "user", "content": query},
    #     {"role": "assistant", "content": results},
    #     {"role": "user", "content": "Does this mean that programming jobs will become obsolete?"}
    # ]
    #
    # results = get_completion_ollama(messages)
    #
    # print(results)

    # import os
    # test_dir = r"C:\home\ananth\research\my_projects\mar_apr_2025\core\session_1_overview\testcases"
    # # name = "page_1.png"
    # name = "benz7.jpg"
    # messages = [
    #     # {
    #     #     "role": "system",
    #     #     "content": "You are a scientist and a Professor in Stanford. Please respond to questions as a prof."
    #     # },
    #     {
    #         'role': 'user',
    #         'content': """
    #         Describe the image.
    #         """,
    #         'images': [os.path.join(test_dir, name)]
    #     }
    # ]
    #
    # results = get_completion_ollama(messages)
    #
    # print(results)
    #
