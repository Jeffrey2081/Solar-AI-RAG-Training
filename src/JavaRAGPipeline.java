import java.io.*;
import org.apache.pdfbox.Loader;
import org.apache.pdfbox.text.PDFTextStripper;
import java.net.http.*;
import java.net.*;
import java.nio.charset.StandardCharsets;
import java.util.*;
import org.json.JSONObject;

public class JavaRAGPipeline {

    private static final String PDF_DIRECTORY = "/home/jeff/Solar-Java/pdf";
    private static final String OLLAMA_API_URL = "http://localhost:11434/api/generate";

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter your question: ");
        String question = scanner.nextLine();
        File folder = new File(PDF_DIRECTORY);
        File[] listOfFiles = folder.listFiles((dir, name) -> name.toLowerCase().endsWith(".pdf"));

        if (listOfFiles != null) {
            List<String> documents = new ArrayList<>();
            for (File file : listOfFiles) {
                try {
                    String content = extractTextFromPDF(file);
                    documents.add(content);
                } catch (IOException e) {
                    System.err.println("Failed to process file: " + file.getName());
                    e.printStackTrace();
                }
            }
            String combinedContent = String.join(" ", documents);
            sendQuestionToOllama(combinedContent, question);
        }
    }

    private static String extractTextFromPDF(File file) throws IOException {
        try (var document = Loader.loadPDF(file)) {
            PDFTextStripper pdfStripper = new PDFTextStripper();
            return pdfStripper.getText(document).replace("\n", " ").replace("\r", "").replace("\"", "\\\"");
        }
    }

    private static void sendQuestionToOllama(String content, String question) {
        try {
            HttpClient client = HttpClient.newHttpClient();
            String sanitizedContent = content.replace("\"", "\\\"").replace("\n", " ").replace("\r", "");
            String sanitizedQuestion = question.replace("\"", "\\\"").replace("\n", " ").replace("\r", "");

            String prompt = String.format("Context: %s Question: %s", sanitizedContent, sanitizedQuestion);
            String requestBody = String.format("{\"model\": \"jeff-ai\", \"prompt\": \"%s\", \"stream\": false}", prompt);

            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create(OLLAMA_API_URL))
                    .header("Content-Type", "application/json")
                    .POST(HttpRequest.BodyPublishers.ofString(requestBody, StandardCharsets.UTF_8))
                    .build();

            HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
            JSONObject jsonResponse = new JSONObject(response.body());

            System.out.println("Answer: " + jsonResponse.optString("response"));
            System.out.println("Model name: " + jsonResponse.optString("model"));
            System.out.println("Time taken: " + Math.round(jsonResponse.optLong("total_duration") / 60_000_000_000.0) + " minutes");
        } catch (Exception e) {
            System.err.println("Failed to send data to Ollama");
            e.printStackTrace();
        }
    }
}
