import math
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain.tools import tool

from core.utils.print_dict import print_dict
from core.session1_foundations.model_code import do_rag

# --------------------------
# 1. Define custom tools
# --------------------------
@tool
def compute_square_root(number):
    """Calculate the square root of a number."""
    print("Calculating square root of {}...".format(number))
    return math.sqrt(number)


@tool
def rag_tool(query: str) -> str:
    """
    RAG tool that takes a query pertaining to nanochat code base and returns the results.
    nanochat implements a GPT 2 style LLM from scratch originally developed and release by Andrej Karpathy.
    """
    print("Rag tool: {}".format(query))
    return do_rag(query)

# --------------------------
# 2. Create tool list
# --------------------------
tools = [compute_square_root, rag_tool]  # TavilySearch(max_results=3),

# --------------------------
# 4. Choose LLM
# --------------------------
llm = ChatOpenAI(
    model="google/gemma-3-12b",           # or the model name your LMStudio serves
    openai_api_base="http://localhost:1234/v1",
    openai_api_key="EMPTY",       # LMStudio doesn’t usually need a key
    temperature=0,
)

# --------------------------
# 5. Create agent + executor
# --------------------------
# Create the ReAct agent
agent_executor = create_agent(llm, tools)

# --------------------------
# 6. Run example queries
# --------------------------
messages = [{"role": "user", "content": "Compute square root of 1234.654"}]
result = agent_executor.invoke(
    dict(messages=messages)
)
print("\nFINAL ANSWER#2:", result)
print_dict(result)
print(result["messages"][-1].content)

messages = [{"role": "user", "content": "What are the different levels of training supported by nanochat?"}]
result = agent_executor.invoke(
    dict(messages=messages)
)

print("\nFINAL ANSWER#3:", result)
print_dict(result)
print(result["messages"][-1].content)
