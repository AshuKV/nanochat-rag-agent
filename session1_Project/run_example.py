#!/usr/bin/env python3
"""
Quick example runner for Training Program Advisor Chatbot
Shows how to use the chatbot programmatically
"""
import sys
from pathlib import Path

# Add src to Python path
sys.path.append(str(Path(__file__).parent / 'src'))

def run_example_queries():
    """
    Example showing how to use the chatbot with actual LLM calls
    NOTE: Requires LM Studio/Ollama running with a model loaded
    """
    from src.chatbot import TrainingAdvisorChatbot
    from src.utils.llm_client import LLMClient
    
    print("🎓 Training Program Advisor - Example Usage")
    print("=" * 50)
    
    # Initialize the chatbot
    try:
        # Configure for your LLM setup
        llm_client = LLMClient(
            base_url="http://localhost:1234/v1",  # LM Studio default
            api_key="LM_STUDIO_API_KEY",
            model="google/gemma-3-12b"  # Adjust to your model
        )
        
        chatbot = TrainingAdvisorChatbot("data/sample_participants.json", llm_client)
        print("✅ Chatbot initialized successfully!")
        
    except Exception as e:
        print(f"❌ Error initializing chatbot: {e}")
        print("\n💡 Make sure:")
        print("   1. LM Studio or Ollama is running")
        print("   2. Model is loaded")
        print("   3. Server URL is correct")
        return
    
    # Example queries to test
    test_queries = [
        "Who has GenAI experience and uses a Mac M2?",
        "How many participants are interested in prompt engineering?",
        "What are the backgrounds of participants with less than 1 year experience?"
    ]
    
    print(f"\n📊 Dataset info: {chatbot.get_dataset_info()['total_participants']} participants loaded")
    
    # Run example queries
    for i, query in enumerate(test_queries, 1):
        print(f"\n🔍 Query {i}: {query}")
        print("-" * 40)
        
        try:
            response = chatbot.process_query(query)
            print(f"🤖 Response: {response}")
            
        except Exception as e:
            print(f"❌ Error processing query: {e}")
        
        print("-" * 40)
    
    print(f"\n🎯 Generate test questions:")
    try:
        questions = chatbot.generate_test_questions(3)
        for i, q in enumerate(questions, 1):
            print(f"   {i}. {q}")
    except Exception as e:
        print(f"❌ Error generating questions: {e}")

if __name__ == "__main__":
    print("This example requires an LLM server to be running.")
    print("For a demo without LLM requirements, run: python3 demo.py")
    print()
    
    user_input = input("Do you want to proceed with LLM queries? (y/N): ")
    if user_input.lower().startswith('y'):
        run_example_queries()
    else:
        print("👍 Run 'python3 demo.py' for offline demonstration")
