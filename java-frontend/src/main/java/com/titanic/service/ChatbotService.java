package com.titanic.service;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.JsonNode;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Named;
import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;

@Named
@ApplicationScoped
public class ChatbotService {
    
    private static final String CHATBOT_BASE_URL = "http://localhost:8010";
    private static final String PREDICT_NL_ENDPOINT = "/predict-nl";
    
    private final HttpClient httpClient;
    private final ObjectMapper objectMapper;
    
    public ChatbotService() {
        this.httpClient = HttpClient.newBuilder()
                .connectTimeout(Duration.ofSeconds(30))
                .followRedirects(HttpClient.Redirect.NORMAL)
                .version(HttpClient.Version.HTTP_1_1)  // Force HTTP/1.1 instead of HTTP/2
                .build();
        this.objectMapper = new ObjectMapper();
    }
    
    public ChatbotResponse predictFromNaturalLanguage(String message) {
        try {
            // Create request payload
            String requestBody = objectMapper.writeValueAsString(new ChatbotRequest(message));
            System.out.println("Sending request to chatbot service:");
            System.out.println("URL: " + CHATBOT_BASE_URL + PREDICT_NL_ENDPOINT);
            System.out.println("Body: " + requestBody);
            
            // Create HTTP request
            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create(CHATBOT_BASE_URL + PREDICT_NL_ENDPOINT))
                    .header("Content-Type", "application/json")
                    .header("Accept", "application/json")
                    .header("User-Agent", "Java-HttpClient")
                    .POST(HttpRequest.BodyPublishers.ofString(requestBody))
                    .timeout(Duration.ofSeconds(60))
                    .build();
            
            // Send request
            System.out.println("About to send request...");
            HttpResponse<String> response;
            try {
                response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
                System.out.println("Request sent successfully");
            } catch (Exception e) {
                System.err.println("Error sending request: " + e.getClass().getSimpleName() + " - " + e.getMessage());
                e.printStackTrace();
                throw e;
            }
            
            System.out.println("Response status: " + response.statusCode());
            System.out.println("Response body: " + response.body());
            
            if (response.statusCode() == 200) {
                return parseResponse(response.body());
            } else {
                System.err.println("Chatbot service error: " + response.statusCode() + " - " + response.body());
                throw new RuntimeException("Chatbot service error: " + response.statusCode() + " - " + response.body());
            }
            
        } catch (IOException | InterruptedException e) {
            throw new RuntimeException("Failed to get prediction from chatbot service: " + e.getMessage(), e);
        }
    }
    
    private ChatbotResponse parseResponse(String responseBody) throws IOException {
        JsonNode root = objectMapper.readTree(responseBody);
        
        // Parse passenger data
        JsonNode passengerNode = root.get("passenger");
        PassengerData passenger = new PassengerData(
                passengerNode.get("pclass").asInt(),
                passengerNode.get("name").asText(),
                passengerNode.get("sex").asText(),
                passengerNode.has("age") && !passengerNode.get("age").isNull() ? 
                        passengerNode.get("age").asDouble() : null,
                passengerNode.get("sibsp").asInt(),
                passengerNode.get("parch").asInt(),
                passengerNode.has("fare") && !passengerNode.get("fare").isNull() ? 
                        passengerNode.get("fare").asDouble() : null,
                passengerNode.get("embarked").asText()
        );
        
        return new ChatbotResponse(
                passenger,
                root.get("survived").asInt(),
                root.get("survival_probability").asDouble(),
                root.get("death_probability").asDouble(),
                root.get("reasoning").asText(),
                root.get("discussion").asText()
        );
    }
    
    // Request/Response classes
    public static class ChatbotRequest {
        public String message;
        
        public ChatbotRequest(String message) {
            this.message = message;
        }
    }
    
    public static class ChatbotResponse {
        public PassengerData passenger;
        public int survived;
        public double survivalProbability;
        public double deathProbability;
        public String reasoning;
        public String discussion;
        
        public ChatbotResponse(PassengerData passenger, int survived, double survivalProbability, 
                             double deathProbability, String reasoning, String discussion) {
            this.passenger = passenger;
            this.survived = survived;
            this.survivalProbability = survivalProbability;
            this.deathProbability = deathProbability;
            this.reasoning = reasoning;
            this.discussion = discussion;
        }
        
        public boolean isSurvived() {
            return survived == 1;
        }
        
        public String getSurvivalStatus() {
            return isSurvived() ? "Survived" : "Did not survive";
        }
        
        public String getSurvivalStatusClass() {
            return isSurvived() ? "survived" : "died";
        }
        
        // Getters for JSF compatibility
        public PassengerData getPassenger() {
            return passenger;
        }
        
        public int getSurvived() {
            return survived;
        }
        
        public double getSurvivalProbability() {
            return survivalProbability;
        }
        
        public double getDeathProbability() {
            return deathProbability;
        }
        
        public String getReasoning() {
            return reasoning;
        }
        
        public String getDiscussion() {
            return discussion;
        }
    }
    
    public static class PassengerData {
        public int pclass;
        public String name;
        public String sex;
        public Double age;
        public int sibsp;
        public int parch;
        public Double fare;
        public String embarked;
        
        public PassengerData(int pclass, String name, String sex, Double age, 
                           int sibsp, int parch, Double fare, String embarked) {
            this.pclass = pclass;
            this.name = name;
            this.sex = sex;
            this.age = age;
            this.sibsp = sibsp;
            this.parch = parch;
            this.fare = fare;
            this.embarked = embarked;
        }
        
        public String getClassText() {
            return switch (pclass) {
                case 1 -> "First Class";
                case 2 -> "Second Class";
                case 3 -> "Third Class";
                default -> "Unknown";
            };
        }
        
        public String getEmbarkedText() {
            return switch (embarked) {
                case "C" -> "Cherbourg";
                case "Q" -> "Queenstown";
                case "S" -> "Southampton";
                default -> embarked;
            };
        }
        
        // Getters for JSF compatibility
        public int getPclass() {
            return pclass;
        }
        
        public String getName() {
            return name;
        }
        
        public String getSex() {
            return sex;
        }
        
        public Double getAge() {
            return age;
        }
        
        public int getSibsp() {
            return sibsp;
        }
        
        public int getParch() {
            return parch;
        }
        
        public Double getFare() {
            return fare;
        }
        
        public String getEmbarked() {
            return embarked;
        }
    }
}
