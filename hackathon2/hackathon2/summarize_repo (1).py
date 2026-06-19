import os
import json

from core.utils.get_completion_client import get_completion_messages
from core.utils.traverse_code_repository import build_tree, print_directory_tree, count_files_by_extension


def generate_summary(file_path, contents):
    """
    Example function that calls an LLM to summarize code.
    """
    prompt = f"""
    Summarize the *conceptual role* of this Python file ({file_path}) within the larger system.

    Do not list classes, methods, or implementation details. 
    Instead, focus on:
    - Its primary purpose
    - The problem it solves
    - How it integrates into the system
    - Key patterns or data formats it introduces

    Keep it under 5 sentences. Use clear, concise language. 
    Avoid implementation details (classes, functions). 
    Prioritize discoverability: At the end of the summary include a list of keywords someone might search for.

    Keep it crisp without losing critical information. 
    Use plain, high-level language — assume the reader understands the system’s domain but not this specific file.

    Example of good summary:
    This file defines the text tokenizer used by NanoChat to convert raw user input into structured token sequences for the language model. 
    It enforces conversation formatting (e.g., user/assistant boundaries) and code block isolation using special tokens, 
    enabling the model to distinguish between dialogue roles and executable code. 
    The implementation prioritizes inference speed via a Rust-backed BPE encoder.
    
    Keywords: <list of relevant keywords pertaining to this code>

    Code:
    {contents}
    """

    messages = [
        {
            "role": "system",
            "content": "You are an expert software developer, great at understanding code and summarizing."
        },
        {
            "role": "user",
            "content": prompt
        }
    ]

    response = get_completion_messages(messages, temperature=0.3)

    print(f"[Summary for {file_path}]")
    print(response)
    print("=" * 80)

    return response


def read_summaries(file_path=None):
    """
    Given a JSON file path that contains a dict of filename versus summaries, return the dict
    :param file_path: full path to JSON file
    :return: dict of filename versus summaries
    """
    if file_path is None:
        file_path = r"/Users/ananth/PycharmProjects/agentic_ai_nov_2025/core/summarizer/summary.json"

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data


if __name__ == '__main__':
    test_root = "/Users/ananth/research/packages/nanochat"  # Replace with your actual repo path

    def my_callback(path):
        """Example callback function."""
        if path.endswith(".py") or path.endswith(".rs") or path.endswith(".sh"):
            with open(path, "r", encoding="utf-8") as f:
                data = f.read()
            summary = generate_summary(path, data)
            return {"summary": summary}  # Example annotation
        else:
            if os.path.isdir(path):
                pass
            return {"summary": None}

    tree_data, summaries = build_tree(test_root, callback=my_callback)

    # Count files by extension
    extension_counts = count_files_by_extension(tree_data)

    # Print the results
    print("File counts by extension:")
    for extension, count in extension_counts.items():
        print(f"{extension}: {count}")

    # Print the directory tree (you can modify this to display annotations)
    print("\nDirectory Tree:")
    print_directory_tree(tree_data)

    for pth, summ in summaries.items():
        print(pth, " => ", summ)

    with open("./summary.json", "w", encoding="utf-8") as f:
        json.dump(summaries, f, indent=4)

    print(tree_data)

    with open("./tree_data.json", "w", encoding="utf-8") as f:
        json.dump(tree_data, f, indent=4)

