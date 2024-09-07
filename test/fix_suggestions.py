import torch
from transformers import RobertaTokenizer, RobertaForSequenceClassification

# Load the fine-tuned model and tokenizer for fix suggestions
model = RobertaForSequenceClassification.from_pretrained('../models/fix_suggestions_codebert')
tokenizer = RobertaTokenizer.from_pretrained('../models/fix_suggestions_codebert')

# Define a function to generate fix suggestions for a Java code snippet
def generate_fix_suggestions(code):
    # Tokenize the input code
    inputs = tokenizer(code, padding='max_length', truncation=True, return_tensors="pt")

    # Get model predictions
    with torch.no_grad():
        outputs = model(**inputs)

    # Get predicted fix suggestion
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
predicted_fix_id = generate_fix_suggestions(example_code)

# Map label id back to fix suggestion
fix_suggestions = [
    "Use parameterized queries to prevent SQL injection.",
    "Sanitize and validate user input.",
    "Use prepared statements for secure database queries.",
    "Ensure proper exception handling and logging.",
    "No fix needed."
]
predicted_fix_suggestion = fix_suggestions[predicted_fix_id]

print(f"Suggested fix: {predicted_fix_suggestion}")
