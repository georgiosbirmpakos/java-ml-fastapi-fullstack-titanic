package com.titanic.model;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.io.Serializable;

/**
 * Model class representing the prediction result from the ML API
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class PredictionResult implements Serializable {
    
    private static final long serialVersionUID = 1L;
    
    private Integer survived;
    private Double survivalProbability;
    private Double deathProbability;
    
    // Helper methods
    public boolean isSurvived() {
        return survived != null && survived == 1;
    }
    
    public String getSurvivalStatus() {
        return isSurvived() ? "Survived" : "Died";
    }
    
    public String getSurvivalStatusWithProbability() {
        return String.format("%s (%.1f%%)", 
            getSurvivalStatus(), 
            (isSurvived() ? survivalProbability : deathProbability) * 100);
    }
}
