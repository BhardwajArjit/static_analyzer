from transformers import AutoTokenizer, AutoModelForSequenceClassification
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import torch
from concurrent.futures import ThreadPoolExecutor

app = FastAPI()

class CodeRequest(BaseModel):
    code: str

# Load models and tokenizers from Hugging Face directly
severity_model = AutoModelForSequenceClassification.from_pretrained("BhardwajArjit/static_analyzer_models", subfolder="severity_scoring_codebert")
severity_tokenizer = AutoTokenizer.from_pretrained("BhardwajArjit/static_analyzer_models", subfolder="severity_scoring_codebert")

fix_suggestions_model = AutoModelForSequenceClassification.from_pretrained("BhardwajArjit/static_analyzer_models", subfolder="fix_suggestions_codebert")
fix_suggestions_tokenizer = AutoTokenizer.from_pretrained("BhardwajArjit/static_analyzer_models", subfolder="fix_suggestions_codebert")

vulnerability_model = AutoModelForSequenceClassification.from_pretrained("BhardwajArjit/static_analyzer_models", subfolder="vulnerability_detection_codebert")
vulnerability_tokenizer = AutoTokenizer.from_pretrained("BhardwajArjit/static_analyzer_models", subfolder="vulnerability_detection_codebert")

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
    return severity_set[predicted_class_id]

def suggest_fix(code):
    inputs = fix_suggestions_tokenizer(code, padding='max_length', truncation=True, return_tensors="pt")
    with torch.no_grad():
        outputs = fix_suggestions_model(**inputs)
    predicted_class_id = torch.argmax(outputs.logits, dim=-1).item()
    return fix_suggestions[predicted_class_id]

def detect_vulnerability(code):
    inputs = vulnerability_tokenizer(code, padding='max_length', truncation=True, return_tensors="pt")
    with torch.no_grad():
        outputs = vulnerability_model(**inputs)
    predicted_class_id = torch.argmax(outputs.logits, dim=-1).item()
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

@app.get("/")
async def root():
    return {"message": "API is running. Use POST /analyze to analyze code."}

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
