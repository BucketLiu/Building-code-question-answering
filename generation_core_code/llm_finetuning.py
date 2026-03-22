import torch
from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)
from peft import LoraConfig, get_peft_model

# ========= 1. 模型 =========
model_name = "Qwen/Qwen-7B"

tokenizer = AutoTokenizer.from_pretrained(
    model_name,
    trust_remote_code=True
)
tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    trust_remote_code=True,
    torch_dtype=torch.float16,
    device_map="auto"
)

# ========= 2. LoRA =========
lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["c_attn"],  # Qwen-7B必须用这个
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

model = get_peft_model(model, lora_config)

# ========= 3. 数据 =========
dataset = load_dataset("json", data_files="data.json")

def format_example(example):
    # 推荐Qwen格式（比alpaca更稳定）
    text = f"问：{example['instruction']}\n答：{example['output']}"
    return {"text": text}

dataset = dataset["train"].map(format_example)

def tokenize(example):
    return tokenizer(
        example["text"],
        truncation=True,
        padding="max_length",
        max_length=512
    )

dataset = dataset.map(tokenize, batched=True)

# ========= 4. 训练参数（你的原始参数） =========
training_args = TrainingArguments(
    output_dir="./models/buildingqa-7b",  # ⭐ 模型名
    per_device_train_batch_size=1,
    gradient_accumulation_steps=4,
    max_steps=6440,
    learning_rate=1e-5,
    logging_steps=50,
    save_steps=500,
    fp16=True,
    report_to="none"
)

# ========= 5. Trainer =========
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False),
)

# ========= 6. 开始训练 =========
trainer.train()

# ========= 7. 保存模型 =========
output_dir = "./models/buildingqa-7b"

model.save_pretrained(output_dir)
tokenizer.save_pretrained(output_dir)

print(f"模型已保存到 {output_dir}")