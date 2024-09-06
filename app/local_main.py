from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import torch
from transformers import RobertaTokenizer, RobertaForSequenceClassification
from concurrent.futures import ThreadPoolExecutor
import os

app = FastAPI()

class CodeRequest(BaseModel):
    code: str

# Local paths to models and tokenizers
severity_model_path = os.path.abspath('./models/severity_scoring_codebert')
fix_suggestions_model_path = os.path.abspath('./models/fix_suggestions_codebert')
vulnerability_model_path = os.path.abspath('./models/vulnerability_detection_codebert')

# Load models and tokenizers
severity_model = RobertaForSequenceClassification.from_pretrained(severity_model_path)
severity_tokenizer = RobertaTokenizer.from_pretrained(severity_model_path)

fix_suggestions_model = RobertaForSequenceClassification.from_pretrained(fix_suggestions_model_path)
fix_suggestions_tokenizer = RobertaTokenizer.from_pretrained(fix_suggestions_model_path)

vulnerability_model = RobertaForSequenceClassification.from_pretrained(vulnerability_model_path)
vulnerability_tokenizer = RobertaTokenizer.from_pretrained(vulnerability_model_path)

# Define label sets
severity_set = ['Safe', 'Low', 'Medium', 'High']
vulnerability_set = ['hardcoded_credentials', 'insecure_data_storage', 'sql_injection', 'insecure_random', 'insecure_file_permissions']
fix_suggestions = [
    "Use parameterized queries to prevent SQL injection.",
    "Sanitize and validate user input.",
    "Use prepared statements for secure database queries.",
    "Ensure proper exception handling and logging.",
    "No fix needed."
]

def classify_severity(code):
    inputs = severity_tokenizer(code, padding='max_length', truncation=True, return_tensors="pt")
    with torch.no_grad():
        outputs = severity_model(**inputs)
    predicted_class_id = torch.argmax(outputs.logits, dim=-1).item()
    if predicted_class_id >= len(severity_set):
        raise IndexError("Predicted class ID is out of range for severity set.")
    return severity_set[predicted_class_id]

def suggest_fix(code):
    inputs = fix_suggestions_tokenizer(code, padding='max_length', truncation=True, return_tensors="pt")
    with torch.no_grad():
        outputs = fix_suggestions_model(**inputs)
    predicted_class_id = torch.argmax(outputs.logits, dim=-1).item()
    print(f"Fix Suggestions - Predicted class ID: {predicted_class_id}")
    if predicted_class_id >= len(fix_suggestions):
        raise IndexError("Predicted class ID is out of range for fix suggestions.")
    return fix_suggestions[predicted_class_id]

def detect_vulnerability(code):
    inputs = vulnerability_tokenizer(code, padding='max_length', truncation=True, return_tensors="pt")
    with torch.no_grad():
        outputs = vulnerability_model(**inputs)
    predicted_class_id = torch.argmax(outputs.logits, dim=-1).item()
    if predicted_class_id >= len(vulnerability_set):
        raise IndexError("Predicted class ID is out of range for vulnerability set.")
    return vulnerability_set[predicted_class_id]

def analyze_code(java_code):
    with ThreadPoolExecutor() as executor:
        future_vulnerability = executor.submit(detect_vulnerability, java_code)
        future_severity = executor.submit(classify_severity, java_code)
        future_fix = executor.submit(suggest_fix, java_code)

        predicted_vulnerability = future_vulnerability.result()
        predicted_severity = future_severity.result()
        predicted_fix = future_fix.result()

    results = {
        "vulnerability": predicted_vulnerability,
        "severity": predicted_severity,
        "fix": predicted_fix
    }

    return results

@app.post("/analyze")
async def analyze(request: CodeRequest):
    try:
        results = analyze_code(request.code)
        return results
    except IndexError as e:
        print(f"IndexError: {e}")
        raise HTTPException(status_code=500, detail="Index error in model output.")
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)