from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

model_name = "meta-llama/Llama-2-7b-chat-hf"  # или другая версия Llama 2

# Загрузка модели и токенизатора
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",  # автоматически использует GPU, если доступен
    torch_dtype=torch.float16,  # для экономии памяти
)

# Входной текст
prompt = "Как работает Llama 2?"

# Токенизация и генерация ответа
inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
outputs = model.generate(**inputs, max_new_tokens=100)

# Декодирование и вывод ответа
answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(answer)