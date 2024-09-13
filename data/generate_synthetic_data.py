import pandas as pd

# Data for severity scoring
java_severity_training_data = {
    "code": [
        # SQL Injection vulnerability (High severity)
        "import java.sql.Connection; import java.sql.DriverManager; import java.sql.PreparedStatement; import java.sql.SQLException; public class SQLInjectionExample { public static void main(String[] args) { String userInput = \"1 OR 1=1\"; try { Connection connection = DriverManager.getConnection(\"jdbc:your_database_url\", \"username\", \"password\"); String query = \"SELECT * FROM users WHERE id = \" + userInput; PreparedStatement statement = connection.prepareStatement(query); statement.executeQuery(); } catch (SQLException e) { e.printStackTrace(); } } }",

        # Insecure Data Storage vulnerability (Medium severity)
        "import java.util.ArrayList; import java.util.List; public class InsecureDataStorageExample { private List<String> sensitiveData = new ArrayList<>(); public void addData(String data) { sensitiveData.add(data); } public List<String> getData() { return sensitiveData; } }",

        # Hardcoded Credentials vulnerability (High severity)
        "public class HardcodedCredentials { public static void main(String[] args) { String username = \"admin\"; String password = \"password123\"; System.out.println(\"Login as: \" + username); } }",

        # Insecure Random Number Generation vulnerability (Medium severity)
        "import java.util.Random; public class InsecureRandomExample { public static void main(String[] args) { Random random = new Random(); int insecureRandom = random.nextInt(); System.out.println(\"Random number: \" + insecureRandom); } }",

        # Insecure File Permissions vulnerability (High severity)
        "import java.io.File; public class InsecureFilePermissions { public static void main(String[] args) { File file = new File(\"sensitive_data.txt\"); file.setReadable(true, false); file.setWritable(true, false); } }",

        # Code that requires no changes (Low severity)
        "import java.util.concurrent.ThreadLocalRandom; public class RandomNumberGenerator { public static void main(String[] args) { int randomNumber = ThreadLocalRandom.current().nextInt(0, 100); System.out.println(\"Random number: \" + randomNumber); } }",

        # Code that requires no changes (None severity)
        "import java.security.SecureRandom; public class SecureRandomExample { public static void main(String[] args) { SecureRandom secureRandom = new SecureRandom(); int secureNumber = secureRandom.nextInt(); System.out.println(\"Secure random number: \" + secureNumber); } }",

        # Code that requires no changes (None severity)
        "import java.sql.Connection; import java.sql.PreparedStatement; import java.sql.SQLException; public class SecureSQL { public static void main(String[] args) { try { Connection connection = DriverManager.getConnection(\"jdbc:your_database_url\", \"username\", \"password\"); String query = \"SELECT * FROM users WHERE id = ?\"; PreparedStatement stmt = connection.prepareStatement(query); stmt.setInt(1, 1); stmt.executeQuery(); } catch (SQLException e) { e.printStackTrace(); } } }"
    ],
    "severity": ["High", "Medium", "High", "Medium", "High", "Low", "Low", "Low"]
}

flutter_severity_training_data = {
    "code": [
        # SQL Injection vulnerability (High severity)
        "import 'package:http/http.dart' as http; void fetchData(String userInput) async { var query = 'SELECT * FROM users WHERE id = ' + userInput; var response = await http.get(Uri.parse('http://example.com/data?query=$query')); print(response.body); }",

        # Insecure Data Storage vulnerability (Medium severity)
        "import 'dart:io'; class InsecureDataStorage { List<String> sensitiveData = []; void addData(String data) { sensitiveData.add(data); File('data.txt').writeAsStringSync(sensitiveData.join(', ')); } List<String> getData() { return sensitiveData; } }",

        # Hardcoded Credentials vulnerability (High severity)
        "class HardcodedCredentials { void login() { String username = 'admin'; String password = 'password123'; print('Login with username: $username and password: $password'); } }",

        # Insecure Random Number Generation vulnerability (Medium severity)
        "import 'dart:math'; class InsecureRandomExample { void generateRandomNumber() { var random = Random(); int insecureRandom = random.nextInt(100); print('Random number: $insecureRandom'); } }",

        # Insecure File Permissions vulnerability (High severity)
        "import 'dart:io'; class InsecureFilePermissions { void setPermissions() { var file = File('sensitive_data.txt'); file.writeAsStringSync('Sensitive data'); file.setLastAccessedSync(DateTime.now()); } }",

        # Code that requires no changes (Low severity)
        "import 'dart:math'; class SecureRandomExample { void generateRandomNumber() { var secureRandom = Random.secure(); int secureRandomNumber = secureRandom.nextInt(100); print('Secure random number: $secureRandomNumber'); } }",

        # Code that requires no changes (None severity)
        "import 'package:crypto/crypto.dart'; class SecureHashExample { void generateHash(String input) { var bytes = utf8.encode(input); var digest = sha256.convert(bytes); print('Hash: \$digest'); } }",

        # Code that requires no changes (None severity)
        "import 'package:http/http.dart' as http; void fetchSecureData() async { var response = await http.get(Uri.parse('http://example.com/data?userId=1')); print(response.body); }"
    ],
    "severity": ["High", "Medium", "High", "Medium", "High", "Low", "Low", "Low"]
}

# Data for fix suggestions
java_fix_training_data = {
    "code": [
        # SQL Injection vulnerability (needs fix)
        "import java.sql.Connection; import java.sql.DriverManager; import java.sql.PreparedStatement; import java.sql.SQLException; public class SQLInjectionExample { public static void main(String[] args) { String userInput = \"1 OR 1=1\"; try { Connection connection = DriverManager.getConnection(\"jdbc:your_database_url\", \"username\", \"password\"); String query = \"SELECT * FROM users WHERE id = \" + userInput; PreparedStatement statement = connection.prepareStatement(query); statement.executeQuery(); } catch (SQLException e) { e.printStackTrace(); } } }",

        # Insecure Data Storage vulnerability (needs fix)
        "import java.util.ArrayList; import java.util.List; public class InsecureDataStorageExample { private List<String> sensitiveData = new ArrayList<>(); public void addData(String data) { sensitiveData.add(data); } public List<String> getData() { return sensitiveData; } }",

        # Hardcoded Credentials vulnerability (needs fix)
        "public class HardcodedCredentials { public static void main(String[] args) { String username = \"admin\"; String password = \"password123\"; System.out.println(\"Login as: \" + username); } }",

        # Insecure Random Number Generation vulnerability (needs fix)
        "import java.util.Random; public class InsecureRandomExample { public static void main(String[] args) { Random random = new Random(); int insecureRandom = random.nextInt(); System.out.println(\"Random number: \" + insecureRandom); } }",

        # Insecure File Permissions vulnerability (needs fix)
        "import java.io.File; public class InsecureFilePermissions { public static void main(String[] args) { File file = new File(\"sensitive_data.txt\"); file.setReadable(true, false); file.setWritable(true, false); } }",

        # Code that requires no changes (already secure)
        "import java.security.SecureRandom; public class SecureRandomExample { public static void main(String[] args) { SecureRandom secureRandom = new SecureRandom(); int secureNumber = secureRandom.nextInt(); System.out.println(\"Secure random number: \" + secureNumber); } }",

        # Code that requires no changes (already secure)
        "import java.sql.Connection; import java.sql.PreparedStatement; import java.sql.SQLException; public class SecureSQL { public static void main(String[] args) { try { Connection connection = DriverManager.getConnection(\"jdbc:your_database_url\", \"username\", \"password\"); String query = \"SELECT * FROM users WHERE id = ?\"; PreparedStatement stmt = connection.prepareStatement(query); stmt.setInt(1, 1); stmt.executeQuery(); } catch (SQLException e) { e.printStackTrace(); } } }"
    ],
    "fix_suggestions": [
        # SQL Injection fix suggestion
        "Use parameterized queries to prevent SQL injection.",

        # Insecure Data Storage fix suggestion
        "Ensure encryption for sensitive data before storing it.",

        # Hardcoded Credentials fix suggestion
        "Externalize sensitive information such as credentials to secure storage or environment variables.",

        # Insecure Random Number Generation fix suggestion
        "Use SecureRandom to generate random numbers for security-sensitive operations.",

        # Insecure File Permissions fix suggestion
        "Ensure that file permissions are restricted to the owner only.",

        # Secure code example (no fix needed)
        "No fix needed.",

        # Secure code example (no fix needed)
        "No fix needed."
    ]
}

flutter_fix_training_data = {
    "code": [
        # SQL Injection vulnerability (needs fix)
        "import 'package:http/http.dart' as http; void fetchData(String userInput) async { var query = 'SELECT * FROM employees WHERE name = ' + userInput; var response = await http.get(Uri.parse('http://example.com/employees?query=$query')); print(response.body); }",

        # Insecure Data Storage vulnerability (needs fix)
        "import 'dart:io'; class InsecureDataStorageExample { List<String> sensitiveData = []; void addData(String data) { sensitiveData.add(data); File('data.txt').writeAsStringSync(sensitiveData.join(', ')); } List<String> getData() { return sensitiveData; } }",

        # Hardcoded Credentials vulnerability (needs fix)
        "class HardcodedCredentialsExample { void login() { String username = 'admin'; String password = 'password123'; print('Logging in with username: \$username and password: \$password'); } }",

        # Insecure Random Number Generation vulnerability (needs fix)
        "import 'dart:math'; class InsecureRandomExample { void generateRandomNumber() { var random = Random(); int insecureRandom = random.nextInt(1000); print('Insecure random number: \$insecureRandom'); } }",

        # Insecure File Permissions vulnerability (needs fix)
        "import 'dart:io'; class InsecureFilePermissionsExample { void setPermissions() { var file = File('confidential.txt'); file.writeAsStringSync('Sensitive information'); file.setLastModifiedSync(DateTime.now()); } }",

        # Code that requires no changes (already secure)
        "import 'dart:math'; class SecureRandomExample { void generateSecureRandomNumber() { var secureRandom = Random.secure(); int secureRandomNumber = secureRandom.nextInt(100); print('Secure random number: \$secureRandomNumber'); } }",

        # Code that requires no changes (already secure)
        "import 'package:http/http.dart' as http; void fetchSecureData() async { var response = await http.get(Uri.parse('http://example.com/employees?userId=1')); print(response.body); }"
    ],
    "fix_suggestions": [
        # SQL Injection fix suggestion
        "Use parameterized queries to prevent SQL injection.",

        # Insecure Data Storage fix suggestion
        "Encrypt sensitive data before storage.",

        # Hardcoded Credentials fix suggestion
        "Externalize credentials to configuration files or environment variables.",

        # Insecure Random Number Generation fix suggestion
        "Use SecureRandom for generating secure random numbers.",

        # Insecure File Permissions fix suggestion
        "Restrict file permissions to prevent unauthorized access.",

        # No fix needed for secure random number generation
        "No fix needed.",

        # No fix needed for secure data fetching
        "No fix needed."
    ]
}

# Validation data for severity scoring
java_severity_validation_data = {
    "code": [
        # High severity: SQL Injection vulnerability
        "import java.sql.Connection; import java.sql.DriverManager; import java.sql.PreparedStatement; import java.sql.SQLException; public class SQLInjectionExample { public static void main(String[] args) { String userInput = \"1 OR 1=1\"; try { Connection connection = DriverManager.getConnection(\"jdbc:your_database_url\", \"username\", \"password\"); String query = \"SELECT * FROM users WHERE id = \" + userInput; PreparedStatement statement = connection.prepareStatement(query); statement.executeQuery(); } catch (SQLException e) { e.printStackTrace(); } } }",

        # High severity: Hardcoded credentials vulnerability
        "public class HardcodedCredentials { public static void main(String[] args) { String username = \"admin\"; String password = \"password123\"; System.out.println(\"Login as: \" + username); } }",

        # Medium severity: Insecure random number generation vulnerability
        "import java.util.Random; public class InsecureRandomExample { public static void main(String[] args) { Random random = new Random(); int insecureRandom = random.nextInt(); System.out.println(\"Random number: \" + insecureRandom); } }",

        # Medium severity: Insecure data storage vulnerability
        "import java.util.ArrayList; import java.util.List; public class InsecureDataStorageExample { private List<String> sensitiveData = new ArrayList<>(); public void addData(String data) { sensitiveData.add(data); } public List<String> getData() { return sensitiveData; } }",

        # Low severity: Insecure file permissions
        "import java.io.File; public class InsecureFilePermissions { public static void main(String[] args) { File file = new File(\"sensitive_data.txt\"); file.setReadable(true, false); file.setWritable(true, false); file.setExecutable(true, false); } }",

        # Secure code (No vulnerability)
        "import java.security.SecureRandom; public class SecureRandomExample { public static void main(String[] args) { SecureRandom secureRandom = new SecureRandom(); int secureNumber = secureRandom.nextInt(); System.out.println(\"Secure random number: \" + secureNumber); } }",

        # Secure code (No vulnerability)
        "import java.sql.Connection; import java.sql.PreparedStatement; import java.sql.SQLException; public class SecureSQL { public static void main(String[] args) { try { Connection connection = DriverManager.getConnection(\"jdbc:your_database_url\", \"username\", \"password\"); String query = \"SELECT * FROM users WHERE id = ?\"; PreparedStatement stmt = connection.prepareStatement(query); stmt.setInt(1, 1); stmt.executeQuery(); } catch (SQLException e) { e.printStackTrace(); } } }"
    ],
    "severity": ["High", "High", "Medium", "Medium", "Low", "Safe", "Safe"]
}

flutter_severity_validation_data = {
    "code": [
        # SQL Injection vulnerability (High severity)
        "import 'package:http/http.dart' as http; void fetchData(String userInput) async { var query = 'SELECT * FROM employees WHERE name = ' + userInput; var response = await http.get(Uri.parse('http://example.com/employees?query=$query')); print(response.body); }",

        # Insecure Data Storage vulnerability (Medium severity)
        "import 'dart:io'; class InsecureDataStorageValidation { List<String> sensitiveData = []; void addData(String data) { sensitiveData.add(data); File('data.txt').writeAsStringSync(sensitiveData.join(', ')); } List<String> getData() { return sensitiveData; } }",

        # Hardcoded Credentials vulnerability (High severity)
        "class HardcodedCredentialsValidation { void login() { String username = 'root'; String password = 'toor123'; print('Logging in with username: \$username and password: \$password'); } }",

        # Insecure Random Number Generation vulnerability (Medium severity)
        "import 'dart:math'; class InsecureRandomValidation { void generateRandomNumber() { var random = Random(); int insecureRandom = random.nextInt(1000); print('Insecure random number: \$insecureRandom'); } }",

        # Insecure File Permissions vulnerability (High severity)
        "import 'dart:io'; class InsecureFilePermissionsValidation { void setPermissions() { var file = File('confidential.txt'); file.writeAsStringSync('Sensitive information'); file.setLastModifiedSync(DateTime.now()); } }",

        # Code that requires no changes (Low severity)
        "import 'dart:math'; class SecureRandomValidation { void generateSecureRandomNumber() { var secureRandom = Random.secure(); int secureRandomNumber = secureRandom.nextInt(100); print('Secure random number: \$secureRandomNumber'); } }",

        # Code that requires no changes (None severity)
        "import 'package:crypto/crypto.dart'; class SecureHashValidation { void generateHash(String input) { var bytes = utf8.encode(input); var digest = sha256.convert(bytes); print('SHA-256 Hash: \$digest'); } }",

        # Code that requires no changes (None severity)
        "import 'package:http/http.dart' as http; void fetchSecureData() async { var response = await http.get(Uri.parse('http://example.com/employees?userId=1')); print(response.body); }"
    ],
    "severity": ["High", "Medium", "High", "Medium", "High", "Low", "Low", "Low"]
}

# Validation data for fix suggestions
java_fix_validation_data = {
    "code": [
        # SQL Injection vulnerability (needs fix)
        "import java.sql.Connection; import java.sql.DriverManager; import java.sql.PreparedStatement; import java.sql.SQLException; public class SQLInjectionExample { public static void main(String[] args) { String userInput = \"1 OR 1=1\"; try { Connection connection = DriverManager.getConnection(\"jdbc:your_database_url\", \"username\", \"password\"); String query = \"SELECT * FROM users WHERE id = \" + userInput; PreparedStatement statement = connection.prepareStatement(query); statement.executeQuery(); } catch (SQLException e) { e.printStackTrace(); } } }",

        # Hardcoded Credentials vulnerability (needs fix)
        "public class HardcodedCredentials { public static void main(String[] args) { String username = \"admin\"; String password = \"password123\"; System.out.println(\"Login as: \" + username); } }",

        # Insecure Random Number Generation vulnerability (needs fix)
        "import java.util.Random; public class InsecureRandomExample { public static void main(String[] args) { Random random = new Random(); int insecureRandom = random.nextInt(); System.out.println(\"Random number: \" + insecureRandom); } }",

        # Insecure Data Storage vulnerability (needs fix)
        "import java.util.ArrayList; import java.util.List; public class InsecureDataStorageExample { private List<String> sensitiveData = new ArrayList<>(); public void addData(String data) { sensitiveData.add(data); } public List<String> getData() { return sensitiveData; } }",

        # Code that requires no changes (safe code example)
        "import java.security.SecureRandom; public class SecureRandomExample { public static void main(String[] args) { SecureRandom secureRandom = new SecureRandom(); int secureNumber = secureRandom.nextInt(); System.out.println(\"Secure random number: \" + secureNumber); } }",

        # Code that requires no changes (safe code example)
        "import java.sql.Connection; import java.sql.PreparedStatement; import java.sql.SQLException; public class SecureSQL { public static void main(String[] args) { try { Connection connection = DriverManager.getConnection(\"jdbc:your_database_url\", \"username\", \"password\"); String query = \"SELECT * FROM users WHERE id = ?\"; PreparedStatement stmt = connection.prepareStatement(query); stmt.setInt(1, 1); stmt.executeQuery(); } catch (SQLException e) { e.printStackTrace(); } } }"
    ],
    "fix_suggestions": [
        # SQL Injection fix suggestion
        "Use parameterized queries to prevent SQL injection.",

        # Hardcoded Credentials fix suggestion
        "Externalize sensitive information such as credentials to secure storage or environment variables.",

        # Insecure Random Number Generation fix suggestion
        "Use SecureRandom to generate random numbers for security-sensitive operations.",

        # Insecure Data Storage fix suggestion
        "Ensure encryption for sensitive data before storing it.",

        # Secure code example (no fix needed)
        "No fix needed.",

        # Secure code example (no fix needed)
        "No fix needed."
    ]
}

flutter_fix_validation_data = {
    "code": [
        # SQL Injection vulnerability (needs fix)
        "import 'package:http/http.dart' as http; void getData(String userInput) async { var query = 'SELECT * FROM orders WHERE id = ' + userInput; var response = await http.get(Uri.parse('http://example.com/orders?query=$query')); print(response.body); }",

        # Insecure Data Storage vulnerability (needs fix)
        "import 'dart:io'; class InsecureDataStorageExample { List<String> sensitiveData = []; void saveData(String data) { sensitiveData.add(data); File('secrets.txt').writeAsStringSync(sensitiveData.join(', ')); } List<String> getData() { return sensitiveData; } }",

        # Hardcoded Credentials vulnerability (needs fix)
        "class HardcodedCredentialsExample { void authenticate() { String apiKey = 'apikey123'; print('Authenticating with API key: \$apiKey'); } }",

        # Insecure Random Number Generation vulnerability (needs fix)
        "import 'dart:math'; class InsecureRandomExample { void generateInsecureRandomNumber() { var random = Random(); int insecureNumber = random.nextInt(1000); print('Insecure random number: \$insecureNumber'); } }",

        # Insecure File Permissions vulnerability (needs fix)
        "import 'dart:io'; class InsecureFilePermissionsExample { void setInsecurePermissions() { var file = File('private_data.txt'); file.setLastModifiedSync(DateTime.now()); file.writeAsStringSync('Confidential info'); } }",

        # Code that requires no changes (already secure)
        "import 'dart:math'; class SecureRandomExample { void generateSecureNumber() { var secureRandom = Random.secure(); int secureNumber = secureRandom.nextInt(100); print('Secure random number: \$secureNumber'); } }",

        # Code that requires no changes (already secure)
        "import 'package:http/http.dart' as http; void getSecureData() async { var response = await http.get(Uri.parse('http://example.com/orders?userId=1')); print(response.body); }"
    ],
    "fix_suggestions": [
        # SQL Injection fix suggestion
        "Use prepared statements to prevent SQL injection.",

        # Insecure Data Storage fix suggestion
        "Ensure encryption for sensitive data before storing it.",

        # Hardcoded Credentials fix suggestion
        "Externalize sensitive information such as API keys to environment variables or secure storage.",

        # Insecure Random Number Generation fix suggestion
        "Use a secure random number generator.",

        # Insecure File Permissions fix suggestion
        "Ensure file permissions are restricted to authorized users only.",

        # No fix needed for secure random number generation
        "No fix needed.",

        # No fix needed for secure data fetching
        "No fix needed."
    ]
}

# Combine java and flutter dataframes into one dataframe
severity_training_data = {
    "code": java_severity_training_data["code"] + flutter_severity_training_data["code"],
    "severity": java_severity_training_data["severity"] + flutter_severity_training_data["severity"]
}

severity_validation_data = {
    "code": java_severity_validation_data["code"] + flutter_severity_validation_data["code"],
    "severity": java_severity_validation_data["severity"] + flutter_severity_validation_data["severity"]
}

fix_training_data = {
    "code": java_fix_training_data["code"] + flutter_fix_training_data["code"],
    "fix_suggestions": java_fix_training_data["fix_suggestions"] + flutter_fix_training_data["fix_suggestions"]
}

fix_validation_data = {
    "code": java_fix_validation_data["code"] + flutter_fix_validation_data["code"],
    "fix_suggestions": java_fix_validation_data["fix_suggestions"] + flutter_fix_validation_data["fix_suggestions"]
}


# Save the extended data to CSV files
pd.DataFrame(severity_training_data).to_csv('severity_scoring_train_data.csv', index=False)
pd.DataFrame(fix_training_data).to_csv('fix_suggestions_train_data.csv', index=False)

pd.DataFrame(severity_validation_data).to_csv('severity_scoring_validation_data.csv', index=False)
pd.DataFrame(fix_validation_data).to_csv('fix_suggestions_validation_data.csv', index=False)


