import pandas as pd

# Data for severity scoring
severity_data = {
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


# Data for fix suggestions
fix_data = {
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
    "fixed_code": [
        # SQL Injection fix (use prepared statements)
        "import java.sql.Connection; import java.sql.DriverManager; import java.sql.PreparedStatement; import java.sql.SQLException; public class SQLInjectionExample { public static void main(String[] args) { String userInput = \"1\"; try { Connection connection = DriverManager.getConnection(\"jdbc:your_database_url\", \"username\", \"password\"); String query = \"SELECT * FROM users WHERE id = ?\"; PreparedStatement statement = connection.prepareStatement(query); statement.setString(1, userInput); statement.executeQuery(); } catch (SQLException e) { e.printStackTrace(); } } }",

        # Insecure Data Storage fix (encrypt sensitive data)
        "import java.util.ArrayList; import java.util.List; import javax.crypto.Cipher; import javax.crypto.KeyGenerator; import javax.crypto.SecretKey; public class SecureDataStorageExample { private List<String> sensitiveData = new ArrayList<>(); public void addData(String data) throws Exception { SecretKey key = KeyGenerator.getInstance(\"AES\").generateKey(); Cipher cipher = Cipher.getInstance(\"AES\"); cipher.init(Cipher.ENCRYPT_MODE, key); byte[] encryptedData = cipher.doFinal(data.getBytes()); sensitiveData.add(new String(encryptedData)); } public List<String> getData() { return sensitiveData; } }",

        # Hardcoded Credentials fix (externalize credentials)
        "import java.util.Properties; import java.io.InputStream; public class ExternalizedCredentials { public static void main(String[] args) { try (InputStream input = ClassLoader.getSystemResourceAsStream(\"config.properties\")) { Properties prop = new Properties(); prop.load(input); String username = prop.getProperty(\"username\"); String password = prop.getProperty(\"password\"); System.out.println(\"Login as: \" + username); } catch (Exception e) { e.printStackTrace(); } } }",

        # Insecure Random Number Generation fix (use SecureRandom)
        "import java.security.SecureRandom; public class SecureRandomExample { public static void main(String[] args) { SecureRandom secureRandom = new SecureRandom(); int secureNumber = secureRandom.nextInt(); System.out.println(\"Secure random number: \" + secureNumber); } }",

        # Insecure File Permissions fix (restrict file access to owner)
        "import java.io.File; public class SecureFilePermissions { public static void main(String[] args) { File file = new File(\"sensitive_data.txt\"); file.setReadable(true, true); file.setWritable(true, true); } }",

        # Secure code example (no change needed)
        "import java.security.SecureRandom; public class SecureRandomExample { public static void main(String[] args) { SecureRandom secureRandom = new SecureRandom(); int secureNumber = secureRandom.nextInt(); System.out.println(\"Secure random number: \" + secureNumber); } }",

        # Secure code example (no change needed)
        "import java.sql.Connection; import java.sql.PreparedStatement; import java.sql.SQLException; public class SecureSQL { public static void main(String[] args) { try { Connection connection = DriverManager.getConnection(\"jdbc:your_database_url\", \"username\", \"password\"); String query = \"SELECT * FROM users WHERE id = ?\"; PreparedStatement stmt = connection.prepareStatement(query); stmt.setInt(1, 1); stmt.executeQuery(); } catch (SQLException e) { e.printStackTrace(); } } }"
    ]
}

# Validation data for severity scoring
severity_validation_data = {
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

# Validation data for fix suggestions
fix_validation_data = {
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
    "fixed_code": [
        # SQL Injection fix (use prepared statements)
        "import java.sql.Connection; import java.sql.DriverManager; import java.sql.PreparedStatement; import java.sql.SQLException; public class SQLInjectionExample { public static void main(String[] args) { String userInput = \"1\"; try { Connection connection = DriverManager.getConnection(\"jdbc:your_database_url\", \"username\", \"password\"); String query = \"SELECT * FROM users WHERE id = ?\"; PreparedStatement statement = connection.prepareStatement(query); statement.setString(1, userInput); statement.executeQuery(); } catch (SQLException e) { e.printStackTrace(); } } }",

        # Hardcoded Credentials fix (externalize credentials)
        "import java.util.Properties; import java.io.InputStream; public class ExternalizedCredentials { public static void main(String[] args) { try (InputStream input = ClassLoader.getSystemResourceAsStream(\"config.properties\")) { Properties prop = new Properties(); prop.load(input); String username = prop.getProperty(\"username\"); String password = prop.getProperty(\"password\"); System.out.println(\"Login as: \" + username); } catch (Exception e) { e.printStackTrace(); } } }",

        # Insecure Random Number Generation fix (use SecureRandom)
        "import java.security.SecureRandom; public class SecureRandomExample { public static void main(String[] args) { SecureRandom secureRandom = new SecureRandom(); int secureNumber = secureRandom.nextInt(); System.out.println(\"Secure random number: \" + secureNumber); } }",

        # Insecure Data Storage fix (encrypt sensitive data)
        "import java.util.ArrayList; import java.util.List; import javax.crypto.Cipher; import javax.crypto.KeyGenerator; import javax.crypto.SecretKey; public class SecureDataStorageExample { private List<String> sensitiveData = new ArrayList<>(); public void addData(String data) throws Exception { SecretKey key = KeyGenerator.getInstance(\"AES\").generateKey(); Cipher cipher = Cipher.getInstance(\"AES\"); cipher.init(Cipher.ENCRYPT_MODE, key); byte[] encryptedData = cipher.doFinal(data.getBytes()); sensitiveData.add(new String(encryptedData)); } public List<String> getData() { return sensitiveData; } }",

        # Secure code example (no change needed)
        "import java.security.SecureRandom; public class SecureRandomExample { public static void main(String[] args) { SecureRandom secureRandom = new SecureRandom(); int secureNumber = secureRandom.nextInt(); System.out.println(\"Secure random number: \" + secureNumber); } }",

        # Secure code example (no change needed)
        "import java.sql.Connection; import java.sql.PreparedStatement; import java.sql.SQLException; public class SecureSQL { public static void main(String[] args) { try { Connection connection = DriverManager.getConnection(\"jdbc:your_database_url\", \"username\", \"password\"); String query = \"SELECT * FROM users WHERE id = ?\"; PreparedStatement stmt = connection.prepareStatement(query); stmt.setInt(1, 1); stmt.executeQuery(); } catch (SQLException e) { e.printStackTrace(); } } }"
    ]
}

# Save the extended data to CSV files
pd.DataFrame(severity_data).to_csv('severity_scoring_train_data.csv', index=False)
pd.DataFrame(fix_data).to_csv('fix_suggestions_train_data.csv', index=False)

pd.DataFrame(severity_validation_data).to_csv('severity_scoring_validation_data.csv', index=False)
pd.DataFrame(fix_validation_data).to_csv('fix_suggestions_validation_data.csv', index=False)


