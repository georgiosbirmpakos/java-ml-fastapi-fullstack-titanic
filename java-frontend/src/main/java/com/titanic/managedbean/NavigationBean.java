package com.titanic.managedbean;

import jakarta.enterprise.context.SessionScoped;
import jakarta.inject.Named;
import java.io.Serializable;

/**
 * Navigation managed bean for handling page navigation
 */
@Named("navigationBean")
@SessionScoped
public class NavigationBean implements Serializable {
    
    private static final long serialVersionUID = 1L;
    
    private String currentPage = "ml-approach";
    
    /**
     * Navigate to Machine Learning Approach page
     */
    public String goToMLApproach() {
        currentPage = "ml-approach";
        return "index?faces-redirect=true";
    }
    
    /**
     * Navigate to AI Agent Approach page
     */
    public String goToAIAgent() {
        currentPage = "ai-agent";
        return "ai_agent?faces-redirect=true";
    }
    
    /**
     * Check if current page is ML Approach
     */
    public boolean isMLApproachActive() {
        return "ml-approach".equals(currentPage);
    }
    
    /**
     * Check if current page is AI Agent
     */
    public boolean isAIAgentActive() {
        return "ai-agent".equals(currentPage);
    }
    
    // Getters and Setters
    public String getCurrentPage() {
        return currentPage;
    }
    
    public void setCurrentPage(String currentPage) {
        this.currentPage = currentPage;
    }
}
