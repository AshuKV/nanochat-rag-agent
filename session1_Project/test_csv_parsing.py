#!/usr/bin/env python3
"""
Test script to verify CSV parsing works correctly
"""
import sys
from pathlib import Path

# Add src to Python path
sys.path.append(str(Path(__file__).parent / 'src'))

from src.utils.data_loader import DataLoader

def test_csv_parsing():
    """Test CSV parsing with the real dataset"""
    print("🧪 Testing CSV Data Parsing")
    print("=" * 50)
    
    try:
        # Load the real CSV file
        csv_file = "/Users/ashutoshkumv/Documents/gAi/session1_overview/prerequisites_check_redacted_dataset.csv"
        
        print(f"📁 Loading CSV file: {csv_file}")
        data_loader = DataLoader(csv_file)
        
        participants = data_loader.participants
        print(f"✅ Successfully loaded {len(participants)} participants")
        
        # Show first few participants with interests
        print(f"\n📊 Sample Participants with Interests:")
        print("=" * 80)
        
        participants_with_interests = []
        for i, p in enumerate(participants[:10]):
            interests = p.get('interests', [])
            if interests and interests != ['general ai learning']:
                participants_with_interests.append(p)
                print(f"{i+1}. {p['name']} ({p['title']})")
                print(f"   Experience: {p['experience_years']} years | GenAI: {p['genai_experience']}")
                print(f"   System: {p['system']}")
                print(f"   Interests: {', '.join(interests)}")
                print(f"   Expectations: {p['expectations'][:100]}...")
                print()
        
        # Test specific queries
        print(f"\n🔍 Testing Interest Queries:")
        print("=" * 50)
        
        # Check for prompt engineering
        prompt_engineering_participants = [p for p in participants if 'prompt engineering' in p.get('interests', [])]
        print(f"📈 Participants interested in prompt engineering: {len(prompt_engineering_participants)}")
        for p in prompt_engineering_participants:
            print(f"   - {p['name']} ({p['title']})")
        
        # Check for GenAI + Mac M2
        genai_mac_m2 = [p for p in participants 
                       if p.get('genai_experience') in ['Yes', 'Limited'] and 'mac m2' in p.get('system', '').lower()]
        print(f"\n🖥️ Participants with GenAI experience and Mac M2: {len(genai_mac_m2)}")
        for p in genai_mac_m2:
            print(f"   - {p['name']} ({p['title']}) | GenAI: {p['genai_experience']}")
        
        # Statistics
        print(f"\n📊 Dataset Statistics:")
        print("=" * 30)
        stats = data_loader.get_statistics()
        print(f"Total participants: {stats.get('total_participants', 0)}")
        print(f"GenAI experience distribution: {stats.get('genai_experience_count', {})}")
        print(f"System distribution: {stats.get('system_distribution', {})}")
        print(f"Top interests: {dict(list(stats.get('top_interests', {}).items())[:5])}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Starting CSV Parsing Test")
    print("=" * 60)
    
    success = test_csv_parsing()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 CSV parsing test passed! The interests should now be properly extracted.")
        print("\n📋 Next Steps:")
        print("1. Restart your Streamlit app")
        print("2. Upload the CSV file or use the uploaded file")
        print("3. Ask: 'How many participants are interested in prompt engineering?'")
        print("4. The chatbot should now correctly identify participants with interests!")
    else:
        print("❌ CSV parsing test failed. Please check the error messages above.")

