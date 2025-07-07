from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

MODEL_PATH = "./output/mistral-qlora"

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    device_map="auto",
    torch_dtype=torch.float16
)

prompt = "<s>[INST] Как мне отчиислиться с кода будущего?[/INST]"
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

with torch.no_grad():
    outputs = model.generate(**inputs, max_new_tokens=256)
    print(tokenizer.decode(outputs[0], skip_special_tokens=True))
