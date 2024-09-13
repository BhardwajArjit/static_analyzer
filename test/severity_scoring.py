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

dart_code = """
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(title: Text('Rooted Device Access Check')),
        body: Center(
          child: RootCheckButton(),
        ),
      ),
    );
  }
}

class RootCheckButton extends StatelessWidget {
  static const platform = MethodChannel('com.example/root_check');

  Future<void> _checkRoot() async {
    try {
      final bool isRooted = await platform.invokeMethod('isRooted');
      if (isRooted) {
        print('Device is rooted');
      } else {
        print('Device is not rooted');
      }
    } on PlatformException catch (e) {
      print("Failed to check root status: '${e.message}'.");
    }
  }

  @override
  Widget build(BuildContext context) {
    return ElevatedButton(
      onPressed: _checkRoot,
      child: Text('Check if Device is Rooted'),
    );
  }
}
"""

# Make a prediction
java_predicted_severity_id = classify_severity(java_code)
dart_predicted_severity_id = classify_severity(dart_code)

# Map label id back to severity label
severity_set = ['Safe', 'Low', 'Medium', 'High']
java_predicted_severity = severity_set[dart_predicted_severity_id]
dart_predicted_severity = severity_set[dart_predicted_severity_id]

print(f"Predicted severity level: {java_predicted_severity}")
print(f"Predicted severity level: {dart_predicted_severity}")
