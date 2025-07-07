from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
import torch
import os

# Параметры
MODEL_NAME = "mistralai/Mistral-7B-v0.1"
OUTPUT_DIR = "./output/mistral-qlora"
MAX_LENGTH = 512

# Загрузка токенизатора и модели
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=True)
tokenizer.pad_token = tokenizer.pad_token = tokenizer.eos_token
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    load_in_4bit=True,
    torch_dtype=torch.float16,
    device_map="auto"
)

# Подготовка модели к QLoRA
model = prepare_model_for_kbit_training(model)

# Настройка QLoRA
lora_config = LoraConfig(
    r=64,
    lora_alpha=16,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    lora_dropout=0.1,
    bias="none",
    task_type="CAUSAL_LM"
)

model = get_peft_model(model, lora_config)

# Загрузка датасета
data = load_dataset("json", data_files="./dataset/train.json")["train"]

# Токенизация
def tokenize(example):
    prompt = f"<s>[INST] {example['question']} [/INST] {example['answer']}</s>"
    tokens = tokenizer(
        prompt,
        truncation=True,
        max_length=MAX_LENGTH,
        padding="max_length"
    )
    tokens["labels"] = tokens["input_ids"].copy()
    return tokens

tokenized_data = data.map(tokenize, remove_columns=data.column_names)

# Параметры обучения
training_args = TrainingArguments(
    per_device_train_batch_size=1,
    gradient_accumulation_steps=4,
    num_train_epochs=3,
    learning_rate=2e-4,
    fp16=True,
    logging_steps=10,
    output_dir=OUTPUT_DIR,
    save_total_limit=1,
    save_strategy="epoch",
    report_to="none"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_data,
    tokenizer=tokenizer
)

# Обучение
trainer.train()

# Сохранение модели и токенизатора
model.save_pretrained(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)
