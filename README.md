# Static Code Analyzer for Android Vulnerabilities

This project provides a **comprehensive static analysis framework** for detecting common vulnerabilities in Android code (currently only for Java and Flutter/Dart). It uses **machine learning models fine-tuned on CodeBERT** to detect security issues, suggest fixes, and classify the severity of the vulnerabilities.

## Features

- **Vulnerability Detection**: Detects ten key types of vulnerabilities:
  - Hardcoded Credentials
  - Insecure Data Storage
  - SQL Injection
  - Insecure Random
  - Insecure File Permissions
  - Memory Leaks
  - Lack of Data Obfuscation
  - Lack of Hashing
  - Rooted Device Access
  - No Vulnerability
- **Severity Scoring**: Classifies the severity of the detected vulnerabilities into:
  - Safe
  - Low
  - Medium
  - High
- **Fix Suggestions**: Provides automatic suggestions to fix the identified vulnerabilities.

## Why Choose Us?

Unlike traditional static analysis tools like **SonarQube**, **MobSF**, **Android Lint**, and **Snyk**, our **CodeBERT-based approach** offers significant advantages. It leverages **machine learning** to go beyond rule-based systems, providing **context-aware** analysis, reducing false positives, and offering **customized, accurate fix suggestions**. 

To learn more about how our approach compares to existing tools and why it provides a better solution for Android security, see the detailed [Why Choose Us?](why_choose_us.md) file.

## Setup

### Prerequisites

- Python 3.11 or later
- Docker (if deploying with Docker)

### Install Dependencies

You can install the required dependencies by running the following command:

```bash
pip install -r requirements.txt
```

Alternatively, you can use the provided Docker setup for easy deployment.

### Docker Setup

To run the application using Docker, follow these steps:

1. **Build the Docker image:**

   ```bash
   docker build -t static-analyzer .
   ```

2. **Run the Docker container:**

   ```bash
   docker run -p 8000:8000 static-analyzer
   ```

3. The FastAPI server will start on `http://0.0.0.0:8000`.

## API Usage

The FastAPI server exposes a POST endpoint to analyze Java code for vulnerabilities.

### POST `/analyze`

- **Input**: JSON object containing the Java code to analyze.
- **Output**: JSON response with the predicted vulnerability, severity score, and fix suggestion.

Example input:

```json
{
  "code": "public class Sample { ... }"
}
```

Example response:

```json
{
  "vulnerability": "insecure_file_permissions",
  "line_number": 10,
  "line_content": "File file = new File(\"sensitive_data.txt\");",
  "severity": "Medium",
  "fix": "Restrict file permissions to only those who require access."
}
```

### Testing with Postman

You can test the API with Postman by sending a POST request to the following URL:

```
http://localhost:8000/analyze
```

- **Request Body**: Raw JSON with the key `"code"` and the Java code to analyze as the value.

## Models

The models are hosted on Hugging Face under the repository `BhardwajArjit/static_analyzer_models`, and include:

- **Severity Scoring Model**: Used to classify the severity of vulnerabilities.
- **Fix Suggestions Model**: Provides automated suggestions for resolving vulnerabilities.
- **Vulnerability Detection Model**: Detects different types of vulnerabilities in the code.

## Known Limitations

- Fix suggestions are currently generalized.
- Analysis of Proguard and Gradle files has not been implemented.
  
## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
