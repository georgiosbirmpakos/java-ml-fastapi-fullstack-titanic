"""
Prediction utility for Titanic survival model
This module provides functions to load the trained model and make predictions.
"""

import pickle
import pandas as pd
import numpy as np
from typing import Dict, List, Any

class TitanicPredictor:
    """Titanic survival prediction class"""
    
    def __init__(self, model_path='models/titanic_model.pkl', 
                 encoders_path='models/encoders.pkl',
                 feature_columns_path='models/feature_columns.pkl'):
        """Initialize the predictor with trained model and encoders"""
        self.model = None
        self.encoders = None
        self.feature_columns = None
        
        try:
            with open(model_path, 'rb') as f:
                self.model = pickle.load(f)
            
            with open(encoders_path, 'rb') as f:
                self.encoders = pickle.load(f)
            
            with open(feature_columns_path, 'rb') as f:
                self.feature_columns = pickle.load(f)
                
            print("Model loaded successfully!")
            
        except FileNotFoundError as e:
            print(f"Error loading model files: {e}")
            print("Please run train.py first to train and save the model.")
    
    def preprocess_passenger(self, passenger_data: Dict[str, Any]) -> pd.DataFrame:
        """Preprocess a single passenger's data for prediction"""
        # Create DataFrame from passenger data
        df = pd.DataFrame([passenger_data])
        
        # Handle missing values
        df['Age'].fillna(df['Age'].median() if not df['Age'].isna().all() else 30, inplace=True)
        df['Fare'].fillna(df['Fare'].median() if not df['Fare'].isna().all() else 30, inplace=True)
        df['Embarked'].fillna('S', inplace=True)
        
        # Feature engineering
        df['FamilySize'] = df['SibSp'] + df['Parch'] + 1
        df['IsAlone'] = (df['FamilySize'] == 1).astype(int)
        
        # Extract title from name
        df['Title'] = df['Name'].str.extract(' ([A-Za-z]+)\.', expand=False)
        df['Title'] = df['Title'].replace(['Lady', 'Countess','Capt', 'Col',
                                         'Don', 'Dr', 'Major', 'Rev', 'Sir', 'Jonkheer', 'Dona'], 'Rare')
        df['Title'] = df['Title'].replace('Mlle', 'Miss')
        df['Title'] = df['Title'].replace('Ms', 'Miss')
        df['Title'] = df['Title'].replace('Mme', 'Mrs')
        df['Title'].fillna('Mr', inplace=True)  # Fill NaN titles with 'Mr'
        
        # Age groups
        df['AgeGroup'] = pd.cut(df['Age'], bins=[0, 12, 18, 35, 60, 100], 
                               labels=['Child', 'Teen', 'Adult', 'Middle', 'Senior'])
        df['AgeGroup'].fillna('Adult', inplace=True)  # Fill NaN age groups with 'Adult'
        
        # Fare groups - handle duplicate values
        try:
            df['FareGroup'] = pd.qcut(df['Fare'], q=4, labels=['Low', 'Medium', 'High', 'VeryHigh'], duplicates='drop')
        except ValueError:
            # If qcut fails due to duplicates, use cut instead
            df['FareGroup'] = pd.cut(df['Fare'], bins=4, labels=['Low', 'Medium', 'High', 'VeryHigh'])
        df['FareGroup'].fillna('Medium', inplace=True)  # Fill NaN fare groups with 'Medium'
        
        return df
    
    def encode_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Encode categorical features using saved encoders"""
        df_encoded = df.copy()
        
        # Encode categorical variables
        df_encoded['Sex'] = self.encoders['sex'].transform(df_encoded['Sex'])
        df_encoded['Embarked'] = self.encoders['embarked'].transform(df_encoded['Embarked'])
        df_encoded['Title'] = self.encoders['title'].transform(df_encoded['Title'])
        df_encoded['AgeGroup'] = self.encoders['age_group'].transform(df_encoded['AgeGroup'])
        df_encoded['FareGroup'] = self.encoders['fare_group'].transform(df_encoded['FareGroup'])
        
        return df_encoded
    
    def predict_survival(self, passenger_data: Dict[str, Any]) -> Dict[str, Any]:
        """Predict survival probability for a single passenger"""
        if self.model is None:
            return {"error": "Model not loaded"}
        
        try:
            # Preprocess passenger data
            df_processed = self.preprocess_passenger(passenger_data)
            
            # Encode features
            df_encoded = self.encode_features(df_processed)
            
            # Select features
            X = df_encoded[self.feature_columns]
            
            # Make prediction
            survival_prob = self.model.predict_proba(X)[0]
            prediction = self.model.predict(X)[0]
            
            return {
                "survived": int(prediction),
                "survival_probability": float(survival_prob[1]),
                "death_probability": float(survival_prob[0])
            }
            
        except Exception as e:
            return {"error": f"Prediction failed: {str(e)}"}
    
    def predict_batch(self, passengers_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Predict survival for multiple passengers"""
        if self.model is None:
            return [{"error": "Model not loaded"} for _ in passengers_data]
        
        results = []
        for passenger_data in passengers_data:
            result = self.predict_survival(passenger_data)
            results.append(result)
        
        return results

# Example usage and testing
if __name__ == "__main__":
    # Initialize predictor
    predictor = TitanicPredictor()
    
    # Example passenger data
    sample_passenger = {
        'Pclass': 1,
        'Name': 'Mr. John Doe',
        'Sex': 'male',
        'Age': 35,
        'SibSp': 0,
        'Parch': 0,
        'Fare': 50.0,
        'Embarked': 'S'
    }
    
    # Make prediction
    result = predictor.predict_survival(sample_passenger)
    print("Sample prediction result:")
    print(result)
