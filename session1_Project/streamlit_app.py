"""
Streamlit Web Interface for Training Program Advisor Chatbot
"""
import streamlit as st
import pandas as pd
import json
import sys
from pathlib import Path

# Add src to Python path
sys.path.append(str(Path(__file__).parent / 'src'))

from src.chatbot import TrainingAdvisorChatbot
from src.utils.llm_client import LLMClient

# Page configuration
st.set_page_config(
    page_title="Training Program Advisor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

def initialize_session_state():
    """Initialize session state variables"""
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'dataset_loaded' not in st.session_state:
        st.session_state.dataset_loaded = False

def load_chatbot(data_file, model_name, server_url, api_key, max_participants=15, compact_mode=True):
    """Load and initialize the chatbot"""
    try:
        llm_client = LLMClient(base_url=server_url, api_key=api_key, model=model_name)
        chatbot = TrainingAdvisorChatbot(data_file, llm_client)
        
        # Set configuration options
        chatbot.max_participants = max_participants
        chatbot.compact_mode = compact_mode
        
        return chatbot, None
    except Exception as e:
        return None, str(e)

def display_dataset_info(chatbot):
    """Display dataset information in sidebar"""
    info = chatbot.get_dataset_info()
    stats = info['statistics']
    
    st.sidebar.subheader("📊 Dataset Overview")
    st.sidebar.metric("Total Participants", info['total_participants'])
    
    # Experience distribution
    if stats.get('experience_distribution'):
        st.sidebar.subheader("👥 Experience Levels")
        exp_data = stats['experience_distribution']
        for level, count in exp_data.items():
            st.sidebar.metric(level, count)
    
    # GenAI experience
    if stats.get('genai_experience_count'):
        st.sidebar.subheader("🤖 GenAI Experience")
        genai_data = stats['genai_experience_count']
        for level, count in genai_data.items():
            st.sidebar.metric(level, count)
    
    # System distribution  
    if stats.get('system_distribution'):
        st.sidebar.subheader("💻 Systems")
        system_data = stats['system_distribution']
        for system, count in system_data.items():
            st.sidebar.metric(system, count)

def main():
    """Main Streamlit application"""
    initialize_session_state()
    
    # Header
    st.title("🎓 Training Program Advisor")
    st.markdown("*AI-powered chatbot to analyze GenAI training program participants*")
    st.divider()
    
    # Sidebar Configuration
    st.sidebar.title("⚙️ Configuration")
    
    # LLM Settings
    st.sidebar.subheader("🤖 LLM Settings")
    model_name = st.sidebar.text_input("Model Name", value="google/gemma-3-12b")
    server_url = st.sidebar.text_input("Server URL", value="http://localhost:1234/v1")
    api_key = st.sidebar.text_input("API Key", value="LM_STUDIO_API_KEY", type="password")
    
    # Advanced settings
    with st.sidebar.expander("⚙️ Advanced Settings"):
        st.info("💡 **Tip:** If you get context length errors, try models with larger context windows like `mistral-7b-instruct` or reduce your dataset size.")
        max_participants = st.slider("Max participants to include", 5, 50, 15, 
                                    help="Reduce this if you get context length errors")
        compact_mode = st.checkbox("Use compact mode", value=True, 
                                 help="Use abbreviated participant data to save context space")
    
    # Data File Selection
    st.sidebar.subheader("📁 Data File")
    data_source = st.sidebar.radio(
        "Choose data source:",
        ["Use Sample Data", "Upload File"]
    )
    
    if data_source == "Use Sample Data":
        data_file = "data/sample_participants.json"
    else:
        uploaded_file = st.sidebar.file_uploader(
            "Upload participant data", 
            type=['json', 'csv', 'xlsx'],
            help="Upload JSON, CSV, or Excel file with participant data"
        )
        if uploaded_file:
            # Save uploaded file temporarily
            data_file = f"temp_{uploaded_file.name}"
            with open(data_file, "wb") as f:
                f.write(uploaded_file.getbuffer())
        else:
            data_file = None
    
    # Initialize/Reload Chatbot
    if st.sidebar.button("🔄 Initialize/Reload Chatbot"):
        if data_file:
            with st.spinner("Loading chatbot..."):
                chatbot, error = load_chatbot(data_file, model_name, server_url, api_key, max_participants, compact_mode)
                
                if chatbot:
                    st.session_state.chatbot = chatbot
                    st.session_state.dataset_loaded = True
                    st.sidebar.success("✅ Chatbot loaded successfully!")
                else:
                    st.sidebar.error(f"❌ Error loading chatbot: {error}")
                    st.session_state.dataset_loaded = False
        else:
            st.sidebar.warning("⚠️ Please select a data file first")
    
    # Display dataset info if loaded
    if st.session_state.dataset_loaded and st.session_state.chatbot:
        display_dataset_info(st.session_state.chatbot)
    
    # Main Content Area
    if not st.session_state.dataset_loaded:
        st.info("👆 Please configure and initialize the chatbot using the sidebar.")
        
        # Show sample questions
        st.subheader("💡 Sample Questions")
        sample_questions = [
            "Who in the group has GenAI experience and a Mac M2?",
            "How many participants are interested in prompt engineering?", 
            "Show me all participants with less than 1 year of experience who want to learn fine-tuning.",
            "What are the most common backgrounds among participants?",
            "Which participants would be good candidates for an advanced course?"
        ]
        
        for i, question in enumerate(sample_questions, 1):
            st.markdown(f"{i}. {question}")
        
        return
    
    # Chat Interface
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("💬 Chat with Training Advisor")
        
        # Display chat history
        chat_container = st.container()
        with chat_container:
            for message in st.session_state.chat_history:
                if message["role"] == "user":
                    st.chat_message("user").write(message["content"])
                else:
                    st.chat_message("assistant").write(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask about the training participants..."):
            # Add user message to history
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)
            
            # Generate response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        response = st.session_state.chatbot.process_query(prompt)
                        st.write(response)
                        
                        # Add assistant response to history
                        st.session_state.chat_history.append({"role": "assistant", "content": response})
                    except Exception as e:
                        error_msg = f"❌ Error: {str(e)}"
                        st.error(error_msg)
                        st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
    
    with col2:
        st.subheader("🛠️ Tools")
        
        # Clear Chat Button
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()
        
        # Generate Test Questions
        if st.button("🎯 Generate Test Questions"):
            with st.spinner("Generating questions..."):
                try:
                    questions = st.session_state.chatbot.generate_test_questions(5)
                    st.success("Generated test questions:")
                    for i, question in enumerate(questions, 1):
                        st.write(f"{i}. {question}")
                        if st.button(f"Ask Q{i}", key=f"ask_{i}"):
                            # Add question to chat
                            st.session_state.chat_history.append({"role": "user", "content": question})
                            response = st.session_state.chatbot.process_query(question) 
                            st.session_state.chat_history.append({"role": "assistant", "content": response})
                            st.rerun()
                except Exception as e:
                    st.error(f"Error generating questions: {e}")
        
        # Export Chat
        if st.button("💾 Export Chat"):
            if st.session_state.chat_history:
                chat_export = {
                    "chat_history": st.session_state.chat_history,
                    "dataset_info": st.session_state.chatbot.get_dataset_info()
                }
                st.download_button(
                    label="Download Chat History", 
                    data=json.dumps(chat_export, indent=2),
                    file_name="chat_history.json",
                    mime="application/json"
                )
            else:
                st.warning("No chat history to export")
    
    # Dataset Viewer (expandable)
    with st.expander("🔍 View Dataset", expanded=False):
        if st.session_state.chatbot:
            participants = st.session_state.chatbot.data_loader.participants
            df = pd.DataFrame(participants)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Load chatbot first to view dataset")

if __name__ == "__main__":
    main()
