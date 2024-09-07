import torch
from transformers import RobertaTokenizer, RobertaForSequenceClassification, Trainer, TrainingArguments
from datasets import DatasetDict, Dataset
import pandas as pd
from evaluate import load

# Load dataset from CSV files
def load_fix_suggestion_data():
    train_df = pd.read_csv('../../data/fix_suggestions_train_data.csv')
    validation_df = pd.read_csv('../../data/fix_suggestions_validation_data.csv')
    return DatasetDict({
        'train': Dataset.from_pandas(train_df),
        'validation': Dataset.from_pandas(validation_df)
    })

# Encode labels
def encode_labels(df):
    unique_labels = df['fixed_code'].unique()
    label_to_id = {label: i for i, label in enumerate(unique_labels)}
    df['labels'] = df['fixed_code'].map(label_to_id)
    return df, label_to_id

# Convert DataFrame to Dataset
def convert_to_dataset(df):
    return Dataset.from_pandas(df)

# Preprocess the data
def preprocess_function(examples):
    inputs = tokenizer(examples['code'], padding='max_length', truncation=True, return_tensors="pt")
    inputs['labels'] = torch.tensor(examples['labels'], dtype=torch.long)
    return inputs

# Load tokenizer and model
tokenizer = RobertaTokenizer.from_pretrained('microsoft/codebert-base')
train_df, label_to_id = encode_labels(pd.read_csv('../../data/fix_suggestions_train_data.csv'))
validation_df, _ = encode_labels(pd.read_csv('../../data/fix_suggestions_validation_data.csv'))

num_labels = len(label_to_id)
model = RobertaForSequenceClassification.from_pretrained('microsoft/codebert-base', num_labels=num_labels)

# Load and preprocess dataset
dataset = DatasetDict({
    'train': convert_to_dataset(train_df),
    'validation': convert_to_dataset(validation_df)
})

tokenized_datasets = dataset.map(preprocess_function, batched=True)

# Define training arguments
training_args = TrainingArguments(
    output_dir='./results',
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=3,
    per_device_eval_batch_size=3,
    num_train_epochs=5,
    weight_decay=0.01
)

# Define metric for evaluation
metric = load("accuracy")

def compute_metrics(p):
    predictions = torch.argmax(torch.tensor(p.predictions), dim=1)
    return metric.compute(predictions=predictions, references=p.label_ids)

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
model.save_pretrained('../../models/fix_suggestions_codebert')
tokenizer.save_pretrained('../../models/fix_suggestions_codebert')
