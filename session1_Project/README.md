# 🎓 Training Program Advisor Chatbot

An LLM-powered chatbot that analyzes participant data for GenAI training programs and provides intelligent insights through natural language queries.

## 📋 Features

- **Natural Language Queries**: Ask questions about participants in plain English
- **Multiple Interfaces**: Both CLI and Web (Streamlit) interfaces available  
- **Flexible Data Input**: Supports JSON, CSV, and Excel formats
- **LLM Integration**: Works with LM Studio, Ollama, and OpenAI-compatible APIs
- **Smart Analytics**: Automatic statistics generation and data insights
- **Test Generation**: Auto-generates test questions for evaluation
- **Real-time Responses**: Streaming responses for better user experience

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+** installed on your system
2. **LM Studio** or **Ollama** running locally with a model loaded (e.g., `gemma-3-12b`)
3. Participant dataset in JSON, CSV, or Excel format

### Installation

```bash
# Clone or download the project
cd session1_Project

# Install dependencies
pip install -r requirements.txt
```

### LLM Setup

#### Option 1: LM Studio
1. Download and install [LM Studio](https://lmstudio.ai/)
2. Load a model like `google/gemma-3-12b-it` or similar
3. Start the local server (default: `http://localhost:1234`)

#### Option 2: Ollama  
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull a model
ollama pull gemma2

# Start server (runs on http://localhost:11434 by default)
ollama serve
```

## 💻 Usage

### Web Interface (Recommended)

```bash
# Launch Streamlit app
streamlit run streamlit_app.py
```

Open your browser to `http://localhost:8501`

### Command Line Interface

```bash
# Basic usage with sample data
python cli_interface.py

# Custom data file
python cli_interface.py --data your_data.csv

# Custom LLM settings  
python cli_interface.py --model gemma2 --url http://localhost:11434/v1
```

## 📊 Sample Queries

The chatbot can handle various types of questions:

### Filtering Queries
- "Who in the group has GenAI experience and a Mac M2?"
- "Show me all participants with less than 1 year of experience who want to learn fine-tuning"
- "Which participants use Linux and are interested in model deployment?"

### Counting Queries  
- "How many participants are interested in prompt engineering?"
- "How many people have more than 2 years of experience?"
- "Count participants by system type"

### Analysis Queries
- "What are the most common backgrounds among participants?"
- "What patterns do you see in participant expectations?"
- "Which participants would be good candidates for an advanced course?"

### Recommendation Queries
- "Who should be paired together for team projects?"  
- "Which participants need more foundational training?"
- "Suggest learning paths based on participant backgrounds"

## 📁 Data Format

### Required Fields
Your dataset should include these fields (column names flexible):

```json
{
  "name": "Participant Name",
  "title": "Job Title/Role", 
  "experience_years": 2.5,
  "genai_experience": "Yes/No/Limited",
  "system": "Mac M2/Windows PC/Linux Ubuntu",
  "interests": ["prompt engineering", "fine-tuning"],
  "expectations": "Learning goals and expectations",
  "background": "Technical background and skills"
}
```

### Supported Formats
- **JSON**: Array of participant objects
- **CSV**: Columns matching the field names
- **Excel**: First sheet with appropriate columns

## 🏗️ Project Structure

```
session1_Project/
├── src/
│   ├── chatbot.py              # Core chatbot logic
│   └── utils/
│       ├── llm_client.py       # LLM client wrapper
│       └── data_loader.py      # Data loading utilities
├── data/
│   └── sample_participants.json # Sample dataset
├── cli_interface.py            # Command line interface
├── streamlit_app.py           # Web interface
├── requirements.txt           # Python dependencies  
└── README.md                  # This file
```

## ⚙️ Configuration

### LLM Settings
- **Model**: Any OpenAI-compatible model (tested with Gemma-3-12B)  
- **Server URL**: Default `http://localhost:1234/v1` (LM Studio)
- **API Key**: Can be any string for local models

### Customization
- Modify system prompts in `src/chatbot.py`
- Add new data processing logic in `src/utils/data_loader.py`
- Extend interfaces with additional features

## 🧪 Testing

### Auto-Generated Test Questions
The chatbot can generate its own test questions:

```python
# In Python or through CLI/Web interface
questions = chatbot.generate_test_questions(10)
```

### Manual Testing
Use the provided sample questions or create your own based on your dataset.

### Evaluation Criteria
- **Accuracy**: Correct information retrieval
- **Relevance**: Responses match query intent  
- **Completeness**: All relevant participants/data included
- **Format**: Clear, structured outputs

## 🔧 Troubleshooting

### Common Issues

**LLM Connection Error**
- Ensure LM Studio/Ollama is running
- Check the server URL and port
- Verify model is loaded

**Data Loading Error**  
- Check file path and format
- Ensure required columns exist
- Verify file permissions

**Poor Response Quality**
- Try different models (larger models often perform better)
- Adjust system prompt for your specific use case
- Ensure data quality and completeness

### Performance Tips
- Use smaller models for faster responses
- Larger models (7B+ parameters) for better accuracy
- Consider temperature settings for creativity vs consistency

## 🎯 Assignment Requirements Checklist

- ✅ **Dataset Loading**: JSON/CSV/Excel support with structured data
- ✅ **Natural Language Queries**: Full query processing pipeline
- ✅ **LLM Integration**: OpenAI API format with local models
- ✅ **Prompt Engineering**: Carefully crafted system and user prompts  
- ✅ **Multiple Interfaces**: Both CLI and Streamlit GUI
- ✅ **Test Generation**: LLM-generated test questions
- ✅ **Query Types**: Filtering, counting, analysis, and recommendation queries
- ✅ **Clean Code**: Well-structured, documented, and testable

## 📈 Future Enhancements

- Historical conversation memory
- Advanced filtering with multiple conditions
- Export capabilities (PDF reports, Excel)  
- Dashboard with visualizations
- Multi-model comparison
- Batch query processing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes  
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is created for educational purposes as part of a GenAI training program.
