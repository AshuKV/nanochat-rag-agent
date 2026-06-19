# pip install accelerate
import os
from transformers import AutoProcessor, Gemma3ForConditionalGeneration
from PIL import Image
import torch

TESTCASES_PATH = r"C:\home\ananth\research\my_projects\unigrads2\testcases"
name = "benz7.jpg"
filename = os.path.join(TESTCASES_PATH, name)

# Load image as PIL
image = Image.open(filename).convert("RGB")

model_id = "google/gemma-3-4b-it"

# Load model
model = Gemma3ForConditionalGeneration.from_pretrained(
    model_id, device_map="auto"
).eval()

processor = AutoProcessor.from_pretrained(model_id)

# Pass the PIL image instead of a URL
messages = [
    {
        "role": "system",
        "content": [{"type": "text", "text": "You are a helpful assistant."}],
    },
    {
        "role": "user",
        "content": [
            {"type": "image", "image": image},  # PIL image here
            {"type": "text", "text": "Who are the people you see in the image? Describe.."},
        ],
    },
]

# Tokenize + prepare inputs
inputs = processor.apply_chat_template(
    messages,
    add_generation_prompt=True,
    tokenize=True,
    return_dict=True,
    return_tensors="pt",
).to(model.device, dtype=torch.bfloat16)

input_len = inputs["input_ids"].shape[-1]

# Generate
with torch.inference_mode():
    generation = model.generate(**inputs, max_new_tokens=100, do_sample=False)
    generation = generation[0][input_len:]

# Decode
decoded = processor.decode(generation, skip_special_tokens=True)
print(decoded)
