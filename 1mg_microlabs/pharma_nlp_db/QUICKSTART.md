# 🚀 Quick Start Guide

Get up and running in 5 minutes!

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Configure API Keys

Open `.env` file and add your API key:

**For OpenAI:**
```bash
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-key-here
```

**For Anthropic Claude:**
```bash
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=your-key-here
```

**For Ollama (Free, Local):**
```bash
LLM_PROVIDER=ollama
# Make sure Ollama is running: ollama serve
```

## Step 3: Setup Database

```bash
python setup.py
```

This will:
- ✅ Create database schema using AI
- ✅ Load all 775+ pharmaceutical products
- ✅ Verify everything is working

## Step 4: Start Querying!

### Option A: CLI Interface (Terminal)
```bash
python cli.py
```

### Option B: GUI Interface (Web)
```bash
streamlit run app.py
```
Then open: http://localhost:8501

## Example Queries to Try

```
How many products are there?
Find products for diabetes
What are side effects of Dolo 650?
List all antibiotics
Show products unsafe during pregnancy
```

## Troubleshooting

**"Database not found"**
→ Run `python setup.py` first

**"API key error"**
→ Check your `.env` file has correct API key

**"Module not found"**
→ Run `pip install -r requirements.txt`

## Need Help?

See full `README.md` for detailed documentation.

---

🎉 **You're all set! Start asking questions!** 💊

