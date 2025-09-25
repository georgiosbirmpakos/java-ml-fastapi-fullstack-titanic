package com.titanic.managedbean;

import com.titanic.service.ChatbotService;
import com.titanic.service.ChatbotService.ChatbotResponse;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Named;

@Named("aiAgentBean")
@ApplicationScoped
public class AIAgentBean {
    
    private ChatbotService chatbotService;
    
    private String userMessage = "";
    private ChatbotResponse response;
    private boolean hasResponse = false;
    private String errorMessage = "";
    
    public AIAgentBean() {
        System.out.println("AIAgentBean constructor called - Bean is being created!");
    }
    
    public void predictSurvival() {
        try {
            if (userMessage == null || userMessage.trim().isEmpty()) {
                errorMessage = "Please enter a description of the passenger.";
                return;
            }
            
            // Create service instance manually
            if (chatbotService == null) {
                chatbotService = new ChatbotService();
            }
            
            response = chatbotService.predictFromNaturalLanguage(userMessage.trim());
            hasResponse = true;
            errorMessage = "";
            
        } catch (Exception e) {
            errorMessage = "Error: " + e.getMessage();
            hasResponse = false;
            response = null;
        }
    }
    
    public void clearForm() {
        System.out.println("clearForm() called");
        userMessage = "";
        response = null;
        hasResponse = false;
        errorMessage = "";
    }
    
    // Getters and Setters
    public String getUserMessage() {
        System.out.println("getUserMessage() called, returning: " + userMessage);
        return userMessage;
    }
    
    public void setUserMessage(String userMessage) {
        this.userMessage = userMessage;
    }
    
    public ChatbotResponse getResponse() {
        return response;
    }
    
    public boolean isHasResponse() {
        return hasResponse;
    }
    
    public String getErrorMessage() {
        return errorMessage;
    }
    
    public boolean isHasError() {
        return errorMessage != null && !errorMessage.isEmpty();
    }
}
