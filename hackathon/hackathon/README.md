# Code artifacts:
1. ingest_code.py
2. model_code.py
3. README.md
4. demo.ipynb

# Example queries and sample outputs

## Code-Level Question 1:  

ashutoshkumv@Ashutoshs-MacBook-Pro gAi % /usr/local/bin/python3 /Users/ashutoshkumv/Documents/gAi/hackathon/hackathon/model_code.py /Users/ashutoshkumv/Documents/gAi/hackathon/hackathon/model_code.py:107: LangChainDeprecationWarning: The class HuggingFaceEmbeddings was deprecated in LangChain 0.2.2 and will be removed in 1.0. An updated version of the class exists in the langchain-huggingface package and should be used instead. To use it run pip install -U langchain-huggingface and import as from langchain_huggingface import HuggingFaceEmbeddings. embeddings = HuggingFaceEmbeddings(model_name=EMBEDDINGS_MODEL, /Users/ashutoshkumv/Documents/gAi/hackathon/hackathon/model_code.py:109: LangChainDeprecationWarning: The class `Chroma` was deprecated in LangChain 0.2.9 and will be removed in 1.0. An updated version of the class exists in the `langchain-chroma package and should be used instead. To use it run `pip install -U `langchain-chroma` and import as `from `langchain_chroma import Chroma. vectordb = Chroma(persist_directory=DB_CHROMA_PATH, embedding_function=embeddings) /Users/ashutoshkumv/Documents/gAi/hackathon/hackathon/model_code.py:95: LangChainDeprecationWarning: The class OpenAI was deprecated in LangChain 0.0.10 and will be removed in 1.0. An updated version of the class exists in the langchain-openai package and should be used instead. To use it run pip install -U langchain-openai and import as from langchain_openai import OpenAI``. return OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio", temperature=0.0, max_tokens=10000) LLM Loaded: OpenAI Params: {'model_name': 'gpt-3.5-turbo-instruct', 'temperature': 0.0, 'top_p': 1.0, 'frequency_penalty': 0.0, 'presence_penalty': 0.0, 'n': 1, 'logit_bias': {}, 'max_tokens': 10000} 

====================================================================== Enhanced RAG for Code Intelligence ✓ Task 1: Traceability - Source files are cited in answers ✓ Task 2: Conceptual Reasoning - File summaries used for context ====================================================================== 

Your Query (or 'quit' to exit): Identify the method where rotary embeddings are applied (hint: look for applyrotaryemb)and describe how it integrates into the attention mechanism 

 Retrieved 6 relevant code chunks 

📂 Source Files Referenced (1): • gpt.py 

💭 Generating answer... huggingface/tokenizers: The current process just got forked, after parallelism has already been used. Disabling parallelism to avoid deadlocks... To disable this warning, you can either: - Avoid using tokenizers before the fork if possible - Explicitly set the environment variable TOKENIZERS_PARALLELISM=(true | false) huggingface/tokenizers: The current process just got forked, after parallelism has already been used. Disabling parallelism to avoid deadlocks... To disable this warning, you can either: - Avoid using tokenizers before the fork if possible - Explicitly set the environment variable TOKENIZERS_PARALLELISM=(true | false) 

====================================================================== ANSWER: ====================================================================== The method where rotary embeddings are applied is within the CausalSelfAttention module, specifically in its forward pass. The function apply_rotary_emb is used to apply the rotary embeddings to queries and keys, enabling relative positional encoding. This integration into the attention mechanism allows for autoregressive processing with causal attention and efficient handling of KV caches during inference. 

[Source: gpt.py] [Source: gpt.py] [Source: gpt.py] 

 The provided answer accurately identifies the method where rotary embeddings are applied and describes its integration into the attention mechanism. The citation of relevant source files further enhances the answer's credibility and provides valuable context for understanding the implementation details. 

====================================================================== 

### Code-Level Questions 2: 

Your Query (or 'quit' to exit): In nanochat/report.py, describe how the “CORE” metric is computed and whatdata it uses 

Retrieved 6 relevant code chunks 

📂 Source Files Referenced (5): • base_eval.py • base_loss.py • base_train.py • chat_eval.py • tok_train.py 

💭 Generating answer... huggingface/tokenizers: The current process just got forked, after parallelism has already been used. Disabling parallelism to avoid deadlocks... To disable this warning, you can either: - Avoid using tokenizers before the fork if possible - Explicitly set the environment variable TOKENIZERS_PARALLELISM=(true | false) huggingface/tokenizers: The current process just got forked, after parallelism has already been used. Disabling parallelism to avoid deadlocks... To disable this warning, you can either: - Avoid using tokenizers before the fork if possible - Explicitly set the environment variable TOKENIZERS_PARALLELISM=(true | false) 

====================================================================== ANSWER: ====================================================================== The CORE metric is computed as the mean centered accuracy across all tasks. The data used includes the results from each task, and the baseline accuracies for each task. 

[From: nanochat/report.py] 

 
### Conceptual and Architecture Question 3: 

Your Query (or 'quit' to exit): Why did the project author build a custom Rust tokenizer instead of using HuggingFace or tiktoken? 

 Retrieved 6 relevant code chunks 

📂 Source Files Referenced (3): • tokenizer.py • tok_train.py • test_rustbpe.py 

💭 Generating answer... 

====================================================================== ANSWER: ====================================================================== The project author chose to build a custom RustBPE tokenizer instead of using HuggingFace or tiktoken for the following reasons: 

Control and Customization: The author wanted fine-grained control over the tokenization process, including the split pattern and mergeable ranks. HuggingFace's tokenizer is more complex and less customizable. 

Efficiency: RustBPE, combined with tiktoken for inference, provides a more efficient solution than using HuggingFace's tokenizer. 

Integration with Rust: The project is written in Rust, so using a Rust-based tokenizer simplifies integration and provides better performance. 

GPT-4 Style Tokenization: The author aimed to replicate GPT-4's tokenization style, which required a custom split pattern and mergeable ranks. 

Sources: 

[From: tokenizer.py] 

[From: test_rustbpe.py] 

[From: tok_train.py] 

### Conceptual and Architecture Question 4: 

Your Query (or 'quit' to exit): How would you find and verify the maximum sequence length (blocksize) forpretraining in the default configuration? 

Retrieved 6 relevant code chunks 

📂 Source Files Referenced (6): • core_eval.py • gpt.py • base_train.py • mid_train.py • test_engine.py • test_rustbpe.py 

💭 Generating answer... 

====================================================================== ANSWER: ====================================================================== To find and verify the maximum sequence length (blocksize) for pretraining, you can check the GPTConfig class in gpt.py and base_train.py, which sets the sequence length to 1024 and 2048 respectively. Additionally, you can examine the mid_train.py script for more details on how to configure and train models with different sequence lengths. The test_engine.py script also demonstrates how to resize the cache dynamically during training, which can be useful for verifying that the maximum sequence length is being handled correctly. 

[From: test_rustbpe.py] def test_training_performance(enwik8_large): """Use a bigger dataset and compare the training speed of the optimized tokenizers (Python, Rust, HuggingFace).""" text = enwik8_large vocab_size = 2048 print(f"\nText length: {len(text)}") 

Commenting out because it's just way too slow to matter 
Train optimized python version 
print("Training optimized python version...") 
optimized_python_tokenizer = FastRegexTokenizer() 
_, optimized_python_train_time = time_function(optimized_python_tokenizer.train, text, vocab_size) 
print(f"Optimized python train time: {optimized_python_train_time:.4f}s") 
 
#### Train rustbpe 
print("\nTraining rustbpe...") 
rustbpe_tokenizer = rustbpe.Tokenizer() 
_, rustbpe_train_time = time_function(rustbpe_tokenizer.train_from_iterator, [text], vocab_size) 
print(f"RustBPE train time: {rustbpe_train_time:.4f}s") 
assert rustbpe_train_time > 0, "Training should take some time" 
 
#### Train HuggingFace 
print("\nTraining HuggingFace...") 
hf_tokenizer, hf_train_time = time_function(HuggingFaceTokenizer.train_from_iterator, [text], vocab_size) 
print(f"HuggingFace train time: {hf_train_time:.4f}s") 
assert hf_train_time > 0, "Training should take some time" 
 
#### Print comparison 
print(f"\n📊 Performance comparison:") 
print(f"   RustBPE: {rustbpe_train_time:.4f}s") 
print(f"   HuggingFace: {hf_train_time:.4f}s") 
print(f"   Speedup: {hf_train_time/rustbpe_train_time:.2f}x") 
  
[From: base_train.py] 

run = "dummy" # wandb run name default ("dummy" is special - we won't log to wandb) 

Runtime 

device_type = "" # cuda|cpu|mps (empty => autodetect good device type default, in order: CUDA > MPS > CPU) 

Model architecture 

depth = 20 # the depth of the Transformer model to train, rest of the kwargs are derived max_seq_len = 2048 # max context length 

Training horizon. Only one of these 3 will be used, in this order of precedence. 

num_iterations = -1 # explicit number of steps of the optimization (-1 = disable) target_flops = -1.0 # calculate num_iterations to reach target_flops. Useful for scaling laws experiments (-1 = disable) target_param_data_ratio = 20 # calculate num_iterations to maintain fixed data:param ratio (Chinchilla=20) (-1 = disable) 

Optimization 

device_batch_size = 32 # per-device batch size (set to not OOM) total_batch_size = 524288 # total desired batch size, in #tokens embedding_lr = 0.2 # learning rate for the embedding parameters (Adam) unembedding_lr = 0.004 # learning rate for the unembedding parameters (Adam) weight_decay = 0.0 # weight decay for the embedding/unembedding parameters (Adam) matrix_lr = 0.02 # learning rate for the matrix parameters (Muon) grad_clip = 1.0 # gradient clipping value (0.0 = disabled) warmup_ratio = 0.0 # ratio of iterations for LR warmup warmdown_ratio = 0.2 # ratio of iterations for LR warmdown final_lr_frac = 0.0 # final LR is this fraction of the initial LR 

Evaluation 

eval_every = 250 # every how many steps to evaluate the model for val bpb eval_tokens = 20*524288 # number of tokens to evaluate val loss on core_metric_every = 2000 # every how many steps to evaluate the core metric (-1 = disable) core_metric_max_per_task = 500 # examples per task in estimating the core metric sample_every = 2000 # every how many steps to sample from the model 

Output 

model_tag = "" # optionally override the model tag for the output checkpoint directory name 

# Check Ingested Data output:

Looking for data at: /Users/ashutoshkumv/Documents/gAi/vector_stores/db_chroma_code

Pre-ingested data found!

Vector Store Statistics:
- Total chunks: 311
- Source files (in sample): 5
- Chunks with summaries: 0/5

Sample Source Files:
- tok_eval.py
- arc.py
- customjson.py

 