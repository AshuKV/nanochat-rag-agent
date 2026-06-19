#!/usr/bin/env python3
"""Streamlit GUI for Pharma Database System."""

import sys
import os
from pathlib import Path
import json
from datetime import datetime

# Add to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from config.config import Config
from src.query_engine import QueryEngine


# Page configuration
st.set_page_config(
    page_title="Pharma Database - NLP Query System",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .query-box {
        padding: 1rem;
        background-color: #f0f2f6;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .result-box {
        padding: 1rem;
        background-color: #e8f5e9;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #4CAF50;
    }
    .error-box {
        padding: 1rem;
        background-color: #ffebee;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #f44336;
    }
    .stat-card {
        padding: 1rem;
        background-color: #e3f2fd;
        border-radius: 10px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_resource
def initialize_engine():
    """Initialize query engine (cached)."""
    try:
        Config.validate()
        
        if not Config.DB_PATH.exists():
            st.error(f"Database not found at {Config.DB_PATH}")
            st.info("Please run setup first: `python setup.py`")
            return None
        
        return QueryEngine()
    except Exception as e:
        st.error(f"Error initializing: {e}")
        return None


def display_header():
    """Display application header."""
    st.markdown('<div class="main-header">💊 Pharma Database NLP Query System</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Ask questions about pharmaceutical products in natural language</div>', unsafe_allow_html=True)


def display_sidebar(engine):
    """Display sidebar with info and examples."""
    with st.sidebar:
        st.header("ℹ️ Information")
        
        # Database stats
        st.subheader("Database Statistics")
        try:
            result = engine.query("How many products are in the database?", natural_response=False)
            if result["success"] and result["raw_results"]:
                count = list(result["raw_results"][0].values())[0]
                st.metric("Total Products", count)
            
            st.info(f"**Database:** {Config.DB_NAME}\n\n**Table:** {Config.TABLE_NAME}")
        except:
            st.warning("Could not load statistics")
        
        st.divider()
        
        # Example queries
        st.subheader("📝 Example Queries")
        examples = engine.get_suggestions()
        
        for idx, example in enumerate(examples[:8], 1):
            if st.button(example, key=f"example_{idx}", use_container_width=True):
                st.session_state.example_query = example
        
        st.divider()
        
        # Settings
        st.subheader("⚙️ Settings")
        st.session_state.show_sql = st.checkbox("Show SQL Query", value=True)
        st.session_state.show_raw_results = st.checkbox("Show Raw Results", value=False)
        st.session_state.natural_response = st.checkbox("Natural Language Response", value=True)
        
        st.divider()
        
        # About
        with st.expander("ℹ️ About"):
            st.markdown("""
            **Pharma Database NLP Query System**
            
            This system allows you to query pharmaceutical product 
            information using natural language. Simply type your 
            question and get instant answers.
            
            **Features:**
            - Natural language understanding
            - Automatic SQL generation
            - Human-readable responses
            - Fast search across 775+ products
            
            **Technology:**
            - LLM-powered query conversion
            - SQLite database
            - Streamlit interface
            """)
        
        # Credits
        st.caption("Made with ❤️ using Python, Streamlit & AI")


def display_query_interface(engine):
    """Display main query interface."""
    # Check for example query from sidebar
    default_query = ""
    if 'example_query' in st.session_state:
        default_query = st.session_state.example_query
        del st.session_state.example_query
    
    # Query input
    col1, col2 = st.columns([5, 1])
    
    with col1:
        query = st.text_input(
            "Your Question:",
            value=default_query,
            placeholder="e.g., Find products for diabetes, What are side effects of Dolo 650?",
            label_visibility="collapsed"
        )
    
    with col2:
        search_button = st.button("🔍 Search", type="primary", use_container_width=True)
    
    # Process query
    if search_button and query:
        with st.spinner("Processing your query..."):
            result = engine.query(
                query,
                return_sql=True,
                natural_response=st.session_state.get('natural_response', True)
            )
        
        # Store in session state
        if 'query_history' not in st.session_state:
            st.session_state.query_history = []
        st.session_state.query_history.append(result)
        
        # Display results
        display_results(result)
    
    elif query and not search_button:
        st.info("👆 Click Search or press Enter to submit your query")


def display_results(result):
    """Display query results."""
    st.divider()
    
    if result["success"]:
        # Success indicator
        st.success(f"✅ Found {result['result_count']} result(s)")
        
        # Show SQL query if enabled
        if st.session_state.get('show_sql', True) and result.get('sql'):
            with st.expander("🔍 View Generated SQL Query"):
                st.code(result['sql'], language='sql')
        
        # Show natural language response
        if result['response']:
            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            st.markdown("### 📋 Response")
            st.markdown(result['response'])
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Show raw results if enabled
        if st.session_state.get('show_raw_results', False) and result['raw_results']:
            with st.expander("📊 View Raw Data"):
                st.json(result['raw_results'])
        
        # Download results
        if result['raw_results']:
            col1, col2, col3 = st.columns([1, 1, 4])
            with col1:
                st.download_button(
                    label="📥 Download JSON",
                    data=json.dumps(result['raw_results'], indent=2),
                    file_name=f"query_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
            with col2:
                # Convert to CSV-like text
                if result['raw_results']:
                    headers = list(result['raw_results'][0].keys())
                    csv_text = ",".join(headers) + "\n"
                    for row in result['raw_results']:
                        values = [str(row.get(h, '')).replace(',', ';') for h in headers]
                        csv_text += ",".join(values) + "\n"
                    
                    st.download_button(
                        label="📥 Download CSV",
                        data=csv_text,
                        file_name=f"query_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
    
    else:
        # Error display
        st.markdown('<div class="error-box">', unsafe_allow_html=True)
        st.error("❌ Query Failed")
        st.markdown(f"**Error:** {result.get('error', 'Unknown error')}")
        if result.get('response'):
            st.markdown(result['response'])
        st.markdown('</div>', unsafe_allow_html=True)


def display_history():
    """Display query history."""
    if 'query_history' not in st.session_state or not st.session_state.query_history:
        st.info("No query history yet. Start by asking a question!")
        return
    
    st.subheader("📜 Query History")
    
    for idx, hist in enumerate(reversed(st.session_state.query_history[-10:]), 1):
        with st.expander(f"{idx}. {hist['query'][:80]}... ({hist.get('result_count', 0)} results)"):
            st.write(f"**Query:** {hist['query']}")
            st.write(f"**Time:** {hist.get('timestamp', 'N/A')}")
            st.write(f"**Results:** {hist.get('result_count', 0)}")
            
            if hist.get('sql'):
                st.code(hist['sql'], language='sql')
            
            if hist.get('response'):
                st.markdown("**Response:**")
                st.write(hist['response'])
    
    if st.button("🗑️ Clear History"):
        st.session_state.query_history = []
        st.rerun()


def main():
    """Main application."""
    # Initialize engine
    engine = initialize_engine()
    
    if not engine:
        st.stop()
    
    # Display header
    display_header()
    
    # Display sidebar
    display_sidebar(engine)
    
    # Main content
    tab1, tab2 = st.tabs(["🔍 Query", "📜 History"])
    
    with tab1:
        st.write("")  # Spacing
        display_query_interface(engine)
        
        # Tips
        with st.expander("💡 Tips for Better Queries"):
            st.markdown("""
            **Good Query Examples:**
            - "Find products for treating diabetes"
            - "What are the side effects of Dolo 650?"
            - "List all antibiotics in the database"
            - "Show me products that are unsafe during pregnancy"
            - "How many products contain aspirin?"
            
            **Tips:**
            - Be specific about what you're looking for
            - Use medical terms when appropriate
            - You can ask about uses, side effects, ingredients, etc.
            - You can ask for counts, lists, or specific product information
            """)
    
    with tab2:
        display_history()


if __name__ == "__main__":
    main()

