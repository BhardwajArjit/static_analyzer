from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
import re
import json
from concurrent.futures import ThreadPoolExecutor
from time import time

app = FastAPI()

# Define regex patterns for common vulnerabilities
regex_patterns = {
    'hardcoded_credentials': r'\b(?:password|passwd|secret|apikey|api_key|token|access_token|credential|auth_token)\b\s*[=:]\s*["\'].*["\']',
    'insecure_data_storage': r'\b(?:getSharedPreferences|openFileOutput|SharedPreferences|store|save|write|db\.put)\b',
    'sql_injection': r'\b(?:Statement|PreparedStatement|executeQuery|executeUpdate|execSQL|rawQuery)\b[^;]*',
    'insecure_random': r'\b(?:Random(?!\s*\.nextInt)|SecureRandom)\b',
    'insecure_file_permissions': r'\b(?:File|FileOutputStream|FileReader|chmod|chown|openFileOutput|writeFile)\b[^;]*',
    'memory_leaks': r'\b(?:close\(\)|finalize\(\)|dispose\(\)|release\(\)|flush\(\)|gc\(\))\b',
    'lack_of_data_obfuscation': r'\b(?:Base64\.encode|Base64\.decode|encodeToString|decodeToString|obfuscate)\b[^;]*',
    'lack_of_hashing': r'\b(?:Hash|MessageDigest|Digest|SHA-1|MD5|hashCode)\b[^;]*',
    'rooted_device_access': r'\b(?:isRooted|checkRooted|test-keys|ro\.secure|ro\.debuggable|su)\b'
}

# Define severity levels for each vulnerability
severity_levels = {
    'hardcoded_credentials': 'High',
    'insecure_data_storage': 'Medium',
    'sql_injection': 'High',
    'insecure_random': 'Medium',
    'insecure_file_permissions': 'Medium',
    'memory_leaks': 'Low',
    'lack_of_data_obfuscation': 'Low',
    'lack_of_hashing': 'Medium',
    'rooted_device_access': 'High',
}

# Mapping of vulnerabilities to fix suggestions
fix_suggestions_map = {
    'sql_injection': "Use parameterized queries or prepared statements to prevent SQL injection.",
    'insecure_data_storage': "Encrypt sensitive data using strong encryption before storing it.",
    'hardcoded_credentials': "Store sensitive information such as credentials in secure storage solutions, not hardcoded in the code.",
    'insecure_random': "Use a cryptographically secure random number generator for security-sensitive operations.",
    'insecure_file_permissions': "Restrict file permissions to only those who require access.",
    'memory_leaks': "Ensure proper resource management by closing resources such as streams, files, and database connections after use.",
    'lack_of_data_obfuscation': "Obfuscate sensitive data, such as API keys, using encryption or other appropriate methods.",
    'lack_of_hashing': "Use a secure hashing algorithm (e.g., SHA-256 or stronger) for hashing sensitive data.",
    'rooted_device_access': "Implement security mechanisms to detect unauthorized access or tampering of the system.",
}


# Define Pydantic model for request body
class CodeSnippet(BaseModel):
    code: str


# Function to detect vulnerabilities using regex and get their lines
def detect_vulnerabilities_with_lines(code_snippet):
    lines = code_snippet.split('\n')
    vulnerabilities = {}

    for line_number, line in enumerate(lines, start=1):
        # Skip import statements and comments for Java, Kotlin, Dart/Flutter
        if line.strip().startswith(('import', '//', '/*', '*', 'package')):
            continue

        for label, pattern in regex_patterns.items():
            if re.search(pattern, line, re.IGNORECASE):
                if label not in vulnerabilities:
                    vulnerabilities[label] = []
                vulnerabilities[label].append((line_number, line.strip()))

    return vulnerabilities


# Function to get the fix suggestion based on the detected vulnerability
def get_fix_suggestion(vulnerability):
    return fix_suggestions_map.get(vulnerability, "No fix needed.")


# Function to get severity level based on the detected vulnerability
def get_severity(vulnerability):
    return severity_levels.get(vulnerability, 'Low')


# Function to analyze vulnerabilities and suggest fixes with severity scoring
def analyze_vulnerabilities(vulnerabilities):
    results = []
    if not vulnerabilities:
        return {"results": [{"vulnerability": "None", "severity": "Safe", "fix": "No fix needed"}]}

    for label, lines in vulnerabilities.items():
        for line_number, line in lines:
            severity = get_severity(label)
            fix_suggestion = get_fix_suggestion(label)
            results.append({
                "vulnerability": label,
                "line_number": line_number,
                "line_content": line,
                "severity": severity,
                "fix": fix_suggestion
            })
    return {"results": results}


@app.post("/analyze")
async def analyze_code(snippet: CodeSnippet):
    try:
        # Extract code content from request
        code_content = snippet.code

        # Execute the regex-based detection and vulnerability analysis
        with ThreadPoolExecutor() as executor:
            future_vulnerabilities = executor.submit(detect_vulnerabilities_with_lines, code_content)
            detected_vulnerabilities = future_vulnerabilities.result()

            if detected_vulnerabilities:
                future_analysis = executor.submit(analyze_vulnerabilities, detected_vulnerabilities)
                analysis_results = future_analysis.result()
            else:
                analysis_results = analyze_vulnerabilities({})

        return analysis_results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
