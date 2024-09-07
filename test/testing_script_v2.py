import torch
from transformers import RobertaTokenizer, RobertaForSequenceClassification
from concurrent.futures import ThreadPoolExecutor
import json

# Paths to the models and tokenizers
severity_model_path = '../models/severity_scoring_codebert'
fix_suggestions_model_path = '../models/fix_suggestions_codebert'
vulnerability_model_path = '../models/vulnerability_detection_codebert'

# Load models and tokenizers
severity_model = RobertaForSequenceClassification.from_pretrained(severity_model_path)
severity_tokenizer = RobertaTokenizer.from_pretrained(severity_model_path)

fix_suggestions_model = RobertaForSequenceClassification.from_pretrained(fix_suggestions_model_path)
fix_suggestions_tokenizer = RobertaTokenizer.from_pretrained(fix_suggestions_model_path)

vulnerability_model = RobertaForSequenceClassification.from_pretrained(vulnerability_model_path)
vulnerability_tokenizer = RobertaTokenizer.from_pretrained(vulnerability_model_path)

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
    'lack_of_hashing'
]
fix_suggestions = [
    "Use parameterized queries to prevent SQL injection.",
    "Sanitize and validate user input.",
    "Use prepared statements for secure database queries.",
    "Ensure proper exception handling and logging.",
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

    # Debugging information
    print(f"Predicted vulnerability class ID: {predicted_class_id}")

    # Ensure the class ID is within the valid range
    if 0 <= predicted_class_id < len(vulnerability_set):
        return vulnerability_set[predicted_class_id]
    else:
        return "Unknown vulnerability"  # Fallback if index is out of range


# Consolidated analysis function
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

    # Convert results to JSON format
    return json.dumps(results, indent=4)


if __name__ == "__main__":
    java_code = """
    import java.sql.Connection;
    import java.sql.DriverManager;
    import java.sql.PreparedStatement;
    import java.sql.SQLException;

    public class SQLInjectionExample {
        public static void main(String[] args) {
            String userInput = "1 OR 1=1";
            try {
                Connection connection = DriverManager.getConnection("jdbc:your_database_url", "username", "password");
                String query = "SELECT * FROM users WHERE id = " + userInput;
                PreparedStatement statement = connection.prepareStatement(query);
                statement.executeQuery();
            } catch (SQLException e) {
                e.printStackTrace();
            }
        }
    }
    """

    # Analyze the code and print results
    results = analyze_code(java_code)
    print(results)
