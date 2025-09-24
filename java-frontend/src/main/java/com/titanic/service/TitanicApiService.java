package com.titanic.service;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.titanic.model.Passenger;
import com.titanic.model.PredictionResult;
import okhttp3.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.util.concurrent.TimeUnit;

/**
 * Service class for communicating with the Titanic prediction API
 */
public class TitanicApiService {
    
    private static final Logger logger = LoggerFactory.getLogger(TitanicApiService.class);
    
    private static final String API_BASE_URL = "http://localhost:8000";
    private static final String PREDICT_ENDPOINT = "/predict";
    private static final String HEALTH_ENDPOINT = "/health";
    
    private final OkHttpClient httpClient;
    private final Gson gson;
    
    public TitanicApiService() {
        this.httpClient = new OkHttpClient.Builder()
                .connectTimeout(30, TimeUnit.SECONDS)
                .readTimeout(30, TimeUnit.SECONDS)
                .writeTimeout(30, TimeUnit.SECONDS)
                .build();
        
        this.gson = new GsonBuilder()
                .setPrettyPrinting()
                .create();
    }
    
    /**
     * Check if the API is healthy and available
     * @return true if API is available, false otherwise
     */
    public boolean isApiHealthy() {
        try {
            Request request = new Request.Builder()
                    .url(API_BASE_URL + HEALTH_ENDPOINT)
                    .get()
                    .build();
            
            try (Response response = httpClient.newCall(request).execute()) {
                boolean isHealthy = response.isSuccessful();
                logger.info("API health check: {}", isHealthy ? "HEALTHY" : "UNHEALTHY");
                return isHealthy;
            }
        } catch (IOException e) {
            logger.error("Error checking API health", e);
            return false;
        }
    }
    
    /**
     * Predict survival for a single passenger
     * @param passenger the passenger data
     * @return prediction result or null if error
     */
    public PredictionResult predictSurvival(Passenger passenger) {
        try {
            // Convert passenger to JSON
            String jsonPayload = gson.toJson(passenger);
            logger.debug("Sending prediction request: {}", jsonPayload);
            
            // Create request body
            RequestBody body = RequestBody.create(
                    jsonPayload,
                    MediaType.get("application/json; charset=utf-8")
            );
            
            // Build request
            Request request = new Request.Builder()
                    .url(API_BASE_URL + PREDICT_ENDPOINT)
                    .post(body)
                    .addHeader("Content-Type", "application/json")
                    .build();
            
            // Execute request
            try (Response response = httpClient.newCall(request).execute()) {
                if (!response.isSuccessful()) {
                    logger.error("API request failed with code: {}", response.code());
                    logger.error("Response body: {}", response.body() != null ? response.body().string() : "No body");
                    return null;
                }
                
                String responseBody = response.body() != null ? response.body().string() : "";
                logger.info("Received prediction response: {}", responseBody);
                
                // Parse response
                PredictionResult result = gson.fromJson(responseBody, PredictionResult.class);
                
                // Debug logging
                if (result != null) {
                    logger.info("Parsed result - survived: {}, survival_prob: {}, death_prob: {}", 
                        result.getSurvived(), result.getSurvivalProbability(), result.getDeathProbability());
                } else {
                    logger.error("Failed to parse prediction result from response: {}", responseBody);
                }
                
                return result;
            }
            
        } catch (IOException e) {
            logger.error("Error calling prediction API", e);
            return null;
        } catch (Exception e) {
            logger.error("Unexpected error during prediction", e);
            return null;
        }
    }
    
    /**
     * Get API status information
     * @return status message
     */
    public String getApiStatus() {
        try {
            Request request = new Request.Builder()
                    .url(API_BASE_URL + HEALTH_ENDPOINT)
                    .get()
                    .build();
            
            try (Response response = httpClient.newCall(request).execute()) {
                if (response.isSuccessful() && response.body() != null) {
                    String responseBody = response.body().string();
                    logger.debug("API status response: {}", responseBody);
                    return responseBody;
                } else {
                    return "API is not responding (HTTP " + response.code() + ")";
                }
            }
        } catch (IOException e) {
            logger.error("Error getting API status", e);
            return "API connection error: " + e.getMessage();
        }
    }
    
    /**
     * Close the HTTP client (should be called on application shutdown)
     */
    public void shutdown() {
        if (httpClient != null) {
            httpClient.dispatcher().executorService().shutdown();
            httpClient.connectionPool().evictAll();
        }
    }
}
