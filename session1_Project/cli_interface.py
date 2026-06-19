#!/usr/bin/env python3
"""
Command Line Interface for Training Program Advisor Chatbot
"""
import os
import sys
import argparse
from pathlib import Path

# Add src to Python path
sys.path.append(str(Path(__file__).parent / 'src'))

from src.chatbot import TrainingAdvisorChatbot
from src.utils.llm_client import LLMClient

def print_banner():
    """Print welcome banner"""
    banner = """
╔═══════════════════════════════════════════════════════════════╗
║                Training Program Advisor Chatbot               ║
║                      CLI Interface                            ║
╚═══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def print_help():
    """Print available commands"""
    help_text = """
Available Commands:
  help, h          - Show this help message
  info, i          - Show dataset information
  stats, s         - Show participant statistics  
  questions, q     - Generate test questions
  test, t          - Run test with sample questions
  exit, quit, bye  - Exit the chatbot
  
Query Examples:
  • "Who in the group has GenAI experience and a Mac M2?"
  • "How many participants are interested in prompt engineering?"
  • "Show me all participants with less than 1 year of experience who want to learn fine-tuning."
  • "What are the most common backgrounds among participants?"
  • "Which participants would be good candidates for an advanced course?"
"""
    print(help_text)

def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(description='Training Program Advisor Chatbot CLI')
    parser.add_argument('--data', '-d', 
                       default='data/sample_participants.json',
                       help='Path to participant data file (JSON/CSV/Excel)')
    parser.add_argument('--model', '-m',
                       default='google/gemma-3-12b', 
                       help='LLM model name')
    parser.add_argument('--url', '-u',
                       default='http://localhost:1234/v1',
                       help='LLM server URL (LM Studio/Ollama)')
    parser.add_argument('--api-key', '-k',
                       default='LM_STUDIO_API_KEY',
                       help='API key for LLM server')
    
    args = parser.parse_args()
    
    print_banner()
    
    # Initialize components
    try:
        print(f"🔧 Initializing LLM client (Model: {args.model})...")
        llm_client = LLMClient(base_url=args.url, api_key=args.api_key, model=args.model)
        
        print(f"📊 Loading participant data from {args.data}...")
        chatbot = TrainingAdvisorChatbot(args.data, llm_client)
        
        dataset_info = chatbot.get_dataset_info()
        print(f"✅ Loaded {dataset_info['total_participants']} participants successfully!")
        
    except Exception as e:
        print(f"❌ Error initializing chatbot: {e}")
        print("\n💡 Make sure:")
        print("   1. LM Studio/Ollama is running on the specified URL")
        print("   2. The specified model is loaded")
        print("   3. The data file exists and is accessible")
        return
    
    print("\n" + "="*60)
    print("🤖 Training Program Advisor is ready!")
    print("Type 'help' for commands or ask questions about the participants.")
    print("="*60 + "\n")
    
    # Main interaction loop
    while True:
        try:
            user_input = input("👤 You: ").strip()
            
            if not user_input:
                continue
                
            # Handle special commands
            if user_input.lower() in ['exit', 'quit', 'bye']:
                print("👋 Goodbye! Have a great day!")
                break
                
            elif user_input.lower() in ['help', 'h']:
                print_help()
                continue
                
            elif user_input.lower() in ['info', 'i']:
                info = chatbot.get_dataset_info()
                print(f"\n📊 Dataset Information:")
                print(f"   • Total Participants: {info['total_participants']}")
                print(f"   • Data File: {info['data_file']}")
                if info['sample_participant']:
                    sample = info['sample_participant']
                    print(f"   • Sample Participant: {sample.get('name', 'N/A')} ({sample.get('title', 'N/A')})")
                print()
                continue
                
            elif user_input.lower() in ['stats', 's']:
                stats = chatbot.data_loader.get_statistics()
                print(f"\n📈 Participant Statistics:")
                print(f"   • Total: {stats['total_participants']}")
                print(f"   • Experience Distribution: {stats['experience_distribution']}")
                print(f"   • GenAI Experience: {stats['genai_experience_count']}")
                print(f"   • System Distribution: {stats['system_distribution']}")
                print(f"   • Top Interests: {dict(list(stats['top_interests'].items())[:5])}")
                print()
                continue
                
            elif user_input.lower() in ['questions', 'q']:
                print("🎯 Generating test questions...")
                try:
                    questions = chatbot.generate_test_questions(5)
                    print("\n📝 Generated Test Questions:")
                    for i, question in enumerate(questions, 1):
                        print(f"   {i}. {question}")
                    print()
                except Exception as e:
                    print(f"❌ Error generating questions: {e}\n")
                continue
                
            elif user_input.lower() in ['test', 't']:
                print("🧪 Running test with sample questions...")
                test_questions = [
                    "Who has GenAI experience and uses a Mac M2?",
                    "How many participants are interested in fine-tuning?",
                    "Show participants with less than 1 year experience."
                ]
                
                for i, question in enumerate(test_questions, 1):
                    print(f"\n🔍 Test {i}: {question}")
                    try:
                        response = chatbot.process_query(question)
                        print(f"🤖 Assistant: {response}")
                    except Exception as e:
                        print(f"❌ Error: {e}")
                    print("-" * 50)
                continue
            
            # Process regular queries
            print("🤖 Assistant: ", end="", flush=True)
            
            try:
                # Use streaming response for better UX
                response_text = ""
                for chunk in chatbot.stream_response(user_input):
                    print(chunk, end="", flush=True)
                    response_text += chunk
                print("\n")
                
            except Exception as e:
                print(f"❌ Error processing query: {e}")
                print("💡 Please check your LLM server connection and try again.\n")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except EOFError:
            print("\n\n👋 Goodbye!")
            break

if __name__ == "__main__":
    main()
