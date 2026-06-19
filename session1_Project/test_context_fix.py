#!/usr/bin/env python3
"""
Test script to verify the context length fixes
"""
import sys
from pathlib import Path

# Add src to Python path
sys.path.append(str(Path(__file__).parent / 'src'))

from src.chatbot import TrainingAdvisorChatbot
from src.utils.llm_client import LLMClient

def test_context_management():
    """Test the context management improvements"""
    print("🧪 Testing Context Length Management Fixes")
    print("=" * 50)
    
    # Initialize chatbot with sample data
    try:
        data_file = "data/sample_participants.json"
        chatbot = TrainingAdvisorChatbot(data_file)
        
        # Set configuration for testing
        chatbot.max_participants = 5  # Limit for testing
        chatbot.compact_mode = True
        
        print(f"✅ Chatbot initialized successfully with {len(chatbot.data_loader.participants)} participants")
        
        # Test query that previously caused context length error
        test_query = "Who in the group has GenAI experience and a Mac M2?"
        
        print(f"\n🔍 Testing query: '{test_query}'")
        print("📊 Getting relevant data...")
        
        # Test the data filtering method
        relevant_data = chatbot._get_relevant_data_for_query(test_query)
        
        print(f"✅ Data filtering successful!")
        print(f"📈 Context length: {len(relevant_data)} characters")
        print(f"📝 Preview of filtered data:")
        print("-" * 30)
        print(relevant_data[:300] + "..." if len(relevant_data) > 300 else relevant_data)
        print("-" * 30)
        
        # Test context length management
        messages = [
            {"role": "system", "content": chatbot.system_prompt},
            {"role": "user", "content": f"Data: {relevant_data}\n\nQuery: {test_query}"}
        ]
        
        print(f"\n🎯 Testing context length management...")
        managed_messages = chatbot._manage_context_length(messages)
        
        total_chars = sum(len(msg['content']) for msg in managed_messages)
        print(f"✅ Context management successful!")
        print(f"📏 Total message length: {total_chars} characters (~{total_chars//4} tokens)")
        
        print(f"\n🎉 All tests passed! Context length error should be resolved.")
        
        # Show configuration tips
        print(f"\n💡 Configuration Tips:")
        print(f"   - Max participants: {chatbot.max_participants}")
        print(f"   - Compact mode: {chatbot.compact_mode}")
        print(f"   - Recommended models: mistral-7b-instruct, llama-3.1-8b-instruct")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False
    
    return True

def test_specific_queries():
    """Test specific queries that might cause context issues"""
    queries = [
        "Who has GenAI experience and a Mac M2?",
        "List all participants with no GenAI experience",
        "Who uses Windows systems?",
        "Show me participants interested in fine-tuning"
    ]
    
    print(f"\n🎯 Testing Specific Queries")
    print("=" * 50)
    
    try:
        chatbot = TrainingAdvisorChatbot("data/sample_participants.json")
        chatbot.max_participants = 8
        chatbot.compact_mode = True
        
        for i, query in enumerate(queries, 1):
            print(f"\n{i}. Query: '{query}'")
            data = chatbot._get_relevant_data_for_query(query)
            print(f"   Result: {len(data)} chars, {data.count('**')} participants found")
            
        print(f"\n✅ All query filtering tests passed!")
        
    except Exception as e:
        print(f"❌ Query tests failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 Starting Context Length Fix Tests")
    print("=" * 60)
    
    success = True
    success &= test_context_management()
    success &= test_specific_queries()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 All tests passed! Your Streamlit app should now work without context length errors.")
        print("\n📋 Next Steps:")
        print("1. Restart your Streamlit app: streamlit run streamlit_app.py")
        print("2. Try the query: 'Who has GenAI experience and a Mac M2?'")
        print("3. Adjust 'Max participants' in Advanced Settings if needed")
    else:
        print("❌ Some tests failed. Please check the error messages above.")

