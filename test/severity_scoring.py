import torch
from transformers import RobertaTokenizer, RobertaForSequenceClassification

# Load the fine-tuned model and tokenizer for severity scoring
model = RobertaForSequenceClassification.from_pretrained('../models/severity_scoring_codebert')
tokenizer = RobertaTokenizer.from_pretrained('../models/severity_scoring_codebert')

# Define a function to classify the severity of a Java code snippet
def classify_severity(code):
    # Tokenize the input code
    inputs = tokenizer(code, padding='max_length', truncation=True, return_tensors="pt")

    # Get model predictions
    with torch.no_grad():
        outputs = model(**inputs)

    # Get predicted severity label
    logits = outputs.logits
    predicted_class_id = torch.argmax(logits, dim=-1).item()

    return predicted_class_id

# Example Java code snippet
example_code = """
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

# Make a prediction
predicted_severity_id = classify_severity(example_code)

# Map label id back to severity label
severity_set = ['Safe', 'Low', 'Medium', 'High']
predicted_severity = severity_set[predicted_severity_id]

print(f"Predicted severity level: {predicted_severity}")
