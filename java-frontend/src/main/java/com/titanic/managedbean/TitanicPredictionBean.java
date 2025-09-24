package com.titanic.managedbean;

import com.titanic.model.Passenger;
import com.titanic.model.PredictionResult;
import com.titanic.service.TitanicApiService;
import jakarta.faces.application.FacesMessage;
import jakarta.faces.context.FacesContext;
import jakarta.faces.view.ViewScoped;
import jakarta.inject.Named;
import lombok.Data;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;

/**
 * ManagedBean for handling Titanic survival prediction
 */
@Named("titanicBean")
@ViewScoped
@Data
public class TitanicPredictionBean implements Serializable {
    
    private static final Logger logger = LoggerFactory.getLogger(TitanicPredictionBean.class);
    private static final long serialVersionUID = 1L;
    
    private TitanicApiService apiService = new TitanicApiService();
    
    // Form data
    private Passenger passenger = new Passenger();
    private PredictionResult predictionResult;
    
    // UI state
    private boolean predictionCompleted = false;
    private boolean apiHealthy = false;
    private String apiStatusMessage = "";
    
    // Sample passengers for quick testing
    private List<Passenger> samplePassengers = new ArrayList<>();
    
    public TitanicPredictionBean() {
        initializeSamplePassengers();
        checkApiHealth();
    }
    
    /**
     * Initialize sample passengers for quick testing
     */
    private void initializeSamplePassengers() {
        samplePassengers.add(new Passenger(1, "Mr. John Astor", "male", 47.0, 1, 0, 211.34, "C"));
        samplePassengers.add(new Passenger(1, "Mrs. Charlotte Cardeza", "female", 36.0, 0, 1, 512.33, "C"));
        samplePassengers.add(new Passenger(3, "Miss Bridget Delia", "female", 22.0, 0, 0, 7.75, "Q"));
        samplePassengers.add(new Passenger(2, "Master William Carter", "male", 11.0, 1, 2, 120.0, "S"));
        samplePassengers.add(new Passenger(3, "Mr. Patrick Dooley", "male", 32.0, 0, 0, 7.75, "Q"));
    }
    
    /**
     * Check API health status
     */
    public void checkApiHealth() {
        try {
            apiHealthy = apiService.isApiHealthy();
            apiStatusMessage = apiService.getApiStatus();
            logger.info("API health check completed: {}", apiHealthy ? "HEALTHY" : "UNHEALTHY");
        } catch (Exception e) {
            logger.error("Error checking API health", e);
            apiHealthy = false;
            apiStatusMessage = "Error checking API status: " + e.getMessage();
        }
    }
    
    /**
     * Predict survival for the current passenger
     */
    public void predictSurvival() {
        try {
            logger.info("Starting prediction for passenger: {}", passenger.getName());
            
            // Validate passenger data
            if (!isPassengerValid()) {
                addErrorMessage("Please fill in all required fields correctly.");
                return;
            }
            
            // Call API service
            predictionResult = apiService.predictSurvival(passenger);
            
            if (predictionResult != null) {
                predictionCompleted = true;
                
                // Get probability with null safety
                Double probability = predictionResult.isSurvived() ? 
                    predictionResult.getSurvivalProbability() : 
                    predictionResult.getDeathProbability();
                
                String message;
                if (probability != null) {
                    message = String.format("Prediction completed: %s with %.1f%% probability", 
                        predictionResult.getSurvivalStatus(), probability * 100);
                } else {
                    message = String.format("Prediction completed: %s", 
                        predictionResult.getSurvivalStatus());
                }
                
                addSuccessMessage(message);
                logger.info("Prediction successful: {}", message);
            } else {
                addErrorMessage("Failed to get prediction from API. Please check if the API is running.");
                logger.error("Prediction failed - no result from API");
            }
            
        } catch (Exception e) {
            logger.error("Error during prediction", e);
            addErrorMessage("An error occurred during prediction: " + e.getMessage());
        }
    }
    
    /**
     * Load a sample passenger for testing
     */
    public void loadSamplePassenger(Passenger samplePassenger) {
        this.passenger = new Passenger(
            samplePassenger.getPclass(),
            samplePassenger.getName(),
            samplePassenger.getSex(),
            samplePassenger.getAge(),
            samplePassenger.getSibsp(),
            samplePassenger.getParch(),
            samplePassenger.getFare(),
            samplePassenger.getEmbarked()
        );
        this.predictionCompleted = false;
        this.predictionResult = null;
        
        addInfoMessage("Sample passenger loaded: " + samplePassenger.getName());
        logger.info("Loaded sample passenger: {}", samplePassenger.getName());
    }
    
    /**
     * Reset the form
     */
    public void resetForm() {
        this.passenger = new Passenger();
        this.predictionResult = null;
        this.predictionCompleted = false;
        
        addInfoMessage("Form reset successfully");
        logger.info("Form reset");
    }
    
    /**
     * Validate passenger data
     */
    private boolean isPassengerValid() {
        return passenger.getPclass() != null && 
               passenger.getName() != null && !passenger.getName().trim().isEmpty() &&
               passenger.getSex() != null && !passenger.getSex().trim().isEmpty();
    }
    
    /**
     * Add success message to FacesContext
     */
    private void addSuccessMessage(String message) {
        FacesContext.getCurrentInstance().addMessage(null, 
            new FacesMessage(FacesMessage.SEVERITY_INFO, "Success", message));
    }
    
    /**
     * Add error message to FacesContext
     */
    private void addErrorMessage(String message) {
        FacesContext.getCurrentInstance().addMessage(null, 
            new FacesMessage(FacesMessage.SEVERITY_ERROR, "Error", message));
    }
    
    /**
     * Add info message to FacesContext
     */
    private void addInfoMessage(String message) {
        FacesContext.getCurrentInstance().addMessage(null, 
            new FacesMessage(FacesMessage.SEVERITY_WARN, "Info", message));
    }
    
    /**
     * Get CSS class for prediction result
     */
    public String getPredictionCssClass() {
        if (predictionResult == null) {
            return "";
        }
        return predictionResult.isSurvived() ? "survived" : "died";
    }
    
    /**
     * Get icon for prediction result
     */
    public String getPredictionIcon() {
        if (predictionResult == null) {
            return "";
        }
        return predictionResult.isSurvived() ? "pi pi-check-circle" : "pi pi-times-circle";
    }
}
