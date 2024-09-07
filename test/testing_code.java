import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.SQLException;

public class VulnerabilityTest {
    public static void main(String[] args) {
        String userInput = "1 OR 1=1";
        try {
            Connection connection = DriverManager.getConnection("jdbc:mysql://localhost:3306/mydb", "root", "password");

            String query = "SELECT * FROM users WHERE id = " + userInput;
            PreparedStatement statement = connection.prepareStatement(query);
            statement.executeQuery();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}
