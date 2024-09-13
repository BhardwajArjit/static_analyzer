import java.io.File;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.security.SecureRandom;
import java.util.Scanner;

public class Test {

    public static void main(String[] args) {
        // Insecure File Permissions
        File file = new File("sensitive_data.txt");
        file.setReadable(true, false);
        file.setWritable(true, false);

        // Rooted Device Access Simulation
        Scanner scanner = new Scanner(System.in);
        System.out.println("Enter device ID:");
        String deviceId = scanner.nextLine();
        System.out.println("Accessing device with ID: " + deviceId);

        // Lack of Hashing
        String data = "password123";
        try {
            MessageDigest md = MessageDigest.getInstance("MD5");
            byte[] hash = md.digest(data.getBytes());
            System.out.println("MD5 hash: " + new String(hash));
        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
        }
    }
}
