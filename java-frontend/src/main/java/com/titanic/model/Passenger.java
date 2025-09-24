package com.titanic.model;

import jakarta.validation.constraints.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.io.Serializable;

/**
 * Model class representing a Titanic passenger
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Passenger implements Serializable {
    
    private static final long serialVersionUID = 1L;
    
    @NotNull(message = "Passenger class is required")
    @Min(value = 1, message = "Passenger class must be 1, 2, or 3")
    @Max(value = 3, message = "Passenger class must be 1, 2, or 3")
    private Integer pclass;
    
    @NotBlank(message = "Name is required")
    @Size(max = 100, message = "Name must not exceed 100 characters")
    private String name;
    
    @NotBlank(message = "Sex is required")
    @Pattern(regexp = "^(male|female)$", message = "Sex must be either 'male' or 'female'")
    private String sex;
    
    @DecimalMin(value = "0.0", message = "Age must be positive")
    @DecimalMax(value = "120.0", message = "Age must be realistic")
    private Double age;
    
    @Min(value = 0, message = "Siblings/Spouses count cannot be negative")
    @Max(value = 8, message = "Siblings/Spouses count cannot exceed 8")
    private Integer sibsp = 0;
    
    @Min(value = 0, message = "Parents/Children count cannot be negative")
    @Max(value = 6, message = "Parents/Children count cannot exceed 6")
    private Integer parch = 0;
    
    @DecimalMin(value = "0.0", message = "Fare must be positive")
    private Double fare;
    
    @Pattern(regexp = "^(C|Q|S)$", message = "Embarked must be C, Q, or S")
    private String embarked = "S";
}
