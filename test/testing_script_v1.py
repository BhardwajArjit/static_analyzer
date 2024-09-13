import torch
from transformers import RobertaTokenizer, RobertaForSequenceClassification
from concurrent.futures import ThreadPoolExecutor
from time import time

# Load the fine-tuned models and tokenizers
severity_model = RobertaForSequenceClassification.from_pretrained('../models/severity_scoring_codebert')
severity_tokenizer = RobertaTokenizer.from_pretrained('../models/severity_scoring_codebert')

fix_suggestions_model = RobertaForSequenceClassification.from_pretrained('../models/fix_suggestions_codebert')
fix_suggestions_tokenizer = RobertaTokenizer.from_pretrained('../models/fix_suggestions_codebert')

vulnerability_model = RobertaForSequenceClassification.from_pretrained('../models/vulnerability_detection_codebert')
vulnerability_tokenizer = RobertaTokenizer.from_pretrained('../models/vulnerability_detection_codebert')

# Define label sets
severity_set = ['Safe', 'Low', 'Medium', 'High']
vulnerability_set = [
    'hardcoded_credentials',
    'insecure_data_storage',
    'sql_injection',
    'insecure_random',
    'insecure_file_permissions',
    'memory_leaks',
    'lack_of_data_obfuscation',
    'lack_of_hashing',
    'rooted_device_access',
    'no_vulnerability'
]
# fix_suggestions = [
#     "Use parameterized queries to prevent SQL injection.",
#     "Sanitize and validate user input.",
#     "Use prepared statements for secure database queries.",
#     "Ensure proper exception handling and logging.",
#     "No fix needed."
# ]

fix_suggestions = [
    "Use parameterized queries to prevent SQL injection.",
    "Ensure encryption for sensitive data before storing it.",
    "Externalize sensitive information such as credentials to secure storage or environment variables.",
    "Use SecureRandom to generate random numbers for security-sensitive operations.",
    "Ensure that file permissions are restricted to the owner only.",
    "Use a secure random number generator.",
    "Externalize sensitive information such as API keys to environment variables or secure storage.",
    "Ensure file permissions are restricted to authorized users only."
    "No fix needed."
]


# Function to classify the severity of a Java code snippet
def classify_severity(code):
    inputs = severity_tokenizer(code, padding='max_length', truncation=True, return_tensors="pt")
    with torch.no_grad():
        outputs = severity_model(**inputs)
    predicted_class_id = torch.argmax(outputs.logits, dim=-1).item()
    return severity_set[predicted_class_id]

# Function to suggest fixes for a Java code snippet
def suggest_fix(code):
    inputs = fix_suggestions_tokenizer(code, padding='max_length', truncation=True, return_tensors="pt")
    with torch.no_grad():
        outputs = fix_suggestions_model(**inputs)
    predicted_class_id = torch.argmax(outputs.logits, dim=-1).item()
    return fix_suggestions[predicted_class_id]

# Function to detect vulnerabilities in a Java code snippet
def detect_vulnerability(code):
    inputs = vulnerability_tokenizer(code, padding='max_length', truncation=True, return_tensors="pt")
    with torch.no_grad():
        outputs = vulnerability_model(**inputs)
    predicted_class_id = torch.argmax(outputs.logits, dim=-1).item()
    return vulnerability_set[predicted_class_id]

# Get start time
start_time = time()

# Java file input
java_file_path = 'testing_code.java'
with open(java_file_path, 'r') as file:
    java_code = file.read()

# Execute the models in parallel
with ThreadPoolExecutor() as executor:
    future_vulnerability = executor.submit(detect_vulnerability, java_code)
    future_severity = executor.submit(classify_severity, java_code)
    future_fix = executor.submit(suggest_fix, java_code)

    predicted_vulnerability = future_vulnerability.result()
    predicted_severity = future_severity.result()
    predicted_fix = future_fix.result()

# Get end time
end_time = time()

# Output results
print(f"Detected vulnerability: {predicted_vulnerability}")
print(f"Predicted severity level: {predicted_severity}")
print(f"Suggested fix: {predicted_fix}")
print(f"Time taken: {(end_time - start_time)} seconds.")
