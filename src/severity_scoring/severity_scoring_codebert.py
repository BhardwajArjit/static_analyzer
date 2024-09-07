from transformers import RobertaTokenizer, RobertaForSequenceClassification, Trainer, TrainingArguments
from datasets import load_dataset, load_metric
import numpy as np

# Load the dataset
def load_severity_data():
    return load_dataset('csv', data_files={
        'train': '../../data/severity_scoring_train_data.csv',
        'validation': '../../data/severity_scoring_validation_data.csv'
    })

# Load tokenizer and model
tokenizer = RobertaTokenizer.from_pretrained('microsoft/codebert-base')
model = RobertaForSequenceClassification.from_pretrained('microsoft/codebert-base', num_labels=4)  # 3 labels: High, Medium, Low

# Preprocess the data
def preprocess_function(examples):
    tokenized_inputs = tokenizer(examples["code"], padding="max_length", truncation=True)
    label_map = {
        "High": 3,
        "Medium": 2,
        "Low": 1,
        "Safe": 0
    }
    tokenized_inputs["labels"] = [label_map[severity] for severity in examples["severity"]]
    return tokenized_inputs

# Load and preprocess the dataset
dataset = load_severity_data()
tokenized_datasets = dataset.map(preprocess_function, batched=True)

# Define training arguments
training_args = TrainingArguments(
    output_dir='./results',
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=2,
    per_device_eval_batch_size=2,
    num_train_epochs=3,
    weight_decay=0.01,
    logging_dir='./logs',
    gradient_accumulation_steps=2,
)


# Define metric for evaluation
metric = load_metric("accuracy")

def compute_metrics(p):
    preds = np.argmax(p.predictions, axis=1)
    return metric.compute(predictions=preds, references=p.label_ids)

# Initialize Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets['train'],
    eval_dataset=tokenized_datasets['validation'],
    compute_metrics=compute_metrics
)

# Fine-tune the model
trainer.train()

# Save the fine-tuned model
model.save_pretrained('../../models/severity_scoring_codebert')
tokenizer.save_pretrained('../../models/severity_scoring_codebert')
