#!/usr/bin/env python3
"""
Demo script for Training Program Advisor Chatbot
Demonstrates core functionality without requiring LLM server
"""
import sys
from pathlib import Path

# Add src to Python path
sys.path.append(str(Path(__file__).parent / 'src'))

from src.utils.data_loader import DataLoader
from src.chatbot import TrainingAdvisorChatbot
from src.utils.llm_client import LLMClient

def demo_data_loading():
    """Demonstrate data loading functionality"""
    print("=" * 60)
    print("🔍 DEMO: Data Loading and Processing")
    print("=" * 60)
    
    # Initialize data loader
    data_file = "data/sample_participants.json"
    loader = DataLoader(data_file)
    
    print(f"📊 Loaded {len(loader.participants)} participants")
    print(f"📁 Data file: {data_file}")
    
    # Show statistics
    print("\n📈 Dataset Statistics:")
    stats = loader.get_statistics()
    for key, value in stats.items():
        if isinstance(value, dict):
            print(f"   {key}: {dict(list(value.items())[:3])}...")
        else:
            print(f"   {key}: {value}")
    
    # Show sample participant
    print("\n👤 Sample Participant:")
    if loader.participants:
        sample = loader.participants[0]
        for key, value in sample.items():
            print(f"   {key}: {value}")
    
    print("\n✅ Data loading demo completed!\n")

def demo_filtering():
    """Demonstrate data filtering"""
    print("=" * 60)  
    print("🎯 DEMO: Data Filtering")
    print("=" * 60)
    
    loader = DataLoader("data/sample_participants.json")
    
    # Filter by GenAI experience
    genai_experienced = loader.filter_participants(genai_experience="Yes")
    print(f"🤖 Participants with GenAI experience: {len(genai_experienced)}")
    for p in genai_experienced:
        print(f"   • {p['name']} ({p['title']})")
    
    # Filter by system and experience  
    mac_users = loader.filter_participants(system="Mac M2")
    print(f"\n💻 Mac M2 users: {len(mac_users)}")
    for p in mac_users:
        print(f"   • {p['name']} - {p.get('experience_years', 'N/A')} years exp")
    
    print("\n✅ Filtering demo completed!\n")

def demo_prompt_creation():
    """Demonstrate prompt creation without LLM call"""
    print("=" * 60)
    print("📝 DEMO: Prompt Engineering")  
    print("=" * 60)
    
    # Mock LLM client for testing (won't make actual calls)
    class MockLLMClient:
        def get_completion_messages(self, messages):
            return "Mock response: This would be processed by the LLM"
        
        def get_streaming_completion(self, messages):
            yield "Mock "
            yield "streaming "
            yield "response"
    
    # Initialize chatbot with mock client
    chatbot = TrainingAdvisorChatbot("data/sample_participants.json", MockLLMClient())
    
    print("🧠 System Prompt Preview:")
    system_prompt = chatbot.system_prompt[:500] + "..."
    print(system_prompt)
    
    print("\n📊 Dataset Context:")
    data_summary = chatbot.data_loader.get_structured_data()[:300] + "..."
    print(data_summary)
    
    print("\n✅ Prompt engineering demo completed!\n")

def demo_test_questions():
    """Show how test questions would be generated"""  
    print("=" * 60)
    print("❓ DEMO: Test Question Generation")
    print("=" * 60)
    
    # Example questions that would be generated
    sample_questions = [
        "Who in the group has GenAI experience and a Mac M2?",
        "How many participants are interested in prompt engineering?", 
        "Show me all participants with less than 1 year of experience who want to learn fine-tuning.",
        "What are the most common backgrounds among participants?",
        "Which participants would be good candidates for an advanced course?",
        "Who uses Linux systems and has research experience?",
        "How many participants have no GenAI experience?",
        "Which participants are interested in both fine-tuning and deployment?",
        "Show me frontend developers who want to learn AI integration.",
        "What systems are most popular among experienced participants?"
    ]
    
    print("🎯 Sample Test Questions:")
    for i, question in enumerate(sample_questions, 1):
        print(f"{i:2d}. {question}")
    
    print(f"\n📊 Generated {len(sample_questions)} diverse test questions")
    print("✅ Test generation demo completed!\n")

def demo_cli_preview():
    """Show CLI interface preview"""
    print("=" * 60)
    print("💻 DEMO: CLI Interface Preview")
    print("=" * 60)
    
    print("🚀 CLI Commands Available:")
    commands = [
        ("help, h", "Show help message"),
        ("info, i", "Show dataset information"), 
        ("stats, s", "Show participant statistics"),
        ("questions, q", "Generate test questions"),
        ("test, t", "Run test with sample questions"),
        ("exit, quit", "Exit the chatbot")
    ]
    
    for cmd, desc in commands:
        print(f"   {cmd:<15} - {desc}")
    
    print("\n🌐 Web Interface Features:")
    features = [
        "Interactive chat interface",
        "Real-time streaming responses", 
        "Dataset visualization",
        "Configuration sidebar",
        "Export functionality",
        "Auto-generated test questions"
    ]
    
    for feature in features:
        print(f"   • {feature}")
    
    print("\n✅ Interface demo completed!\n")

def main():
    """Run all demos"""
    print("🎓 Training Program Advisor Chatbot - DEMO")
    print("This demo shows core functionality without requiring LLM server")
    print()
    
    try:
        demo_data_loading()
        demo_filtering()  
        demo_prompt_creation()
        demo_test_questions()
        demo_cli_preview()
        
        print("=" * 60)
        print("🎉 All demos completed successfully!")
        print("=" * 60)
        print()
        print("📋 Next Steps:")
        print("1. Install requirements: pip install -r requirements.txt")
        print("2. Set up LM Studio or Ollama with a model")
        print("3. Run CLI: python cli_interface.py")
        print("4. Run Web UI: streamlit run streamlit_app.py") 
        print()
        print("💡 See README.md for detailed instructions")
        
    except Exception as e:
        print(f"❌ Demo error: {e}")
        print("Make sure you're in the project directory with sample data")

if __name__ == "__main__":
    main()
