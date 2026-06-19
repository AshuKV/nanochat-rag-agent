# pip install accelerate
import os

from transformers import AutoProcessor, Gemma3ForConditionalGeneration
from PIL import Image
import requests
import torch


TESTCASES_PATH = r"/Users/ashutoshkumv/Documents/gAi/session1Images"

name = "benz1.jpg"

filename = os.path.join(TESTCASES_PATH, name)

model_id = "google/gemma-3-4b-pt"

image = Image.open(filename).convert("RGB")

model = Gemma3ForConditionalGeneration.from_pretrained(model_id).eval()
processor = AutoProcessor.from_pretrained(model_id)

prompt = "<start_of_image> in this image, there is"
model_inputs = processor(text=prompt, images=image, return_tensors="pt")

input_len = model_inputs["input_ids"].shape[-1]

with torch.inference_mode():
    generation = model.generate(**model_inputs, max_new_tokens=100, do_sample=False)
    generation = generation[0][input_len:]

decoded = processor.decode(generation, skip_special_tokens=True)
print(decoded)
