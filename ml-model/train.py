"""
Titanic Survival Prediction Model Training Script
This script trains a Random Forest classifier to predict passenger survival.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
import pickle
import os
import matplotlib.pyplot as plt
import seaborn as sns

def load_data():
    """Load Titanic dataset from CSV file"""
    train_file = 'data/train.csv'
    
    # Check if data file exists
    if not os.path.exists(train_file):
        print("Titanic dataset not found!")
        print("Please run: python download_data.py")
        print("Or manually download from Kaggle and place train.csv in data/ directory")
        raise FileNotFoundError(f"Dataset file not found: {train_file}")
    
    # Load the actual Titanic dataset
    print(f"Loading Titanic dataset from {train_file}...")
    df = pd.read_csv(train_file)
    
    print(f"Dataset loaded successfully!")
    print(f"Shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print(f"Survival rate: {df['Survived'].mean():.3f}")
    
    return df

def explore_data(df):
    """Explore the Titanic dataset"""
    print("\n" + "="*50)
    print("DATASET EXPLORATION")
    print("="*50)
    
    # Basic info
    print(f"Dataset shape: {df.shape}")
    print(f"Missing values:")
    print(df.isnull().sum())
    
    # Survival statistics
    print(f"\nSurvival Statistics:")
    print(f"Overall survival rate: {df['Survived'].mean():.3f}")
    print(f"Survival by sex:")
    print(df.groupby('Sex')['Survived'].agg(['count', 'sum', 'mean']))
    print(f"Survival by class:")
    print(df.groupby('Pclass')['Survived'].agg(['count', 'sum', 'mean']))
    
    # Create visualizations
    plt.figure(figsize=(15, 10))
    
    # Survival by sex
    plt.subplot(2, 3, 1)
    sns.countplot(data=df, x='Sex', hue='Survived')
    plt.title('Survival by Sex')
    
    # Survival by class
    plt.subplot(2, 3, 2)
    sns.countplot(data=df, x='Pclass', hue='Survived')
    plt.title('Survival by Passenger Class')
    
    # Age distribution
    plt.subplot(2, 3, 3)
    df['Age'].hist(bins=30, alpha=0.7)
    plt.title('Age Distribution')
    plt.xlabel('Age')
    
    # Fare distribution
    plt.subplot(2, 3, 4)
    df['Fare'].hist(bins=30, alpha=0.7)
    plt.title('Fare Distribution')
    plt.xlabel('Fare')
    
    # Survival by age groups
    plt.subplot(2, 3, 5)
    df['AgeGroup'] = pd.cut(df['Age'], bins=[0, 12, 18, 35, 60, 100], 
                           labels=['Child', 'Teen', 'Adult', 'Middle', 'Senior'])
    survival_by_age = df.groupby('AgeGroup')['Survived'].mean()
    survival_by_age.plot(kind='bar')
    plt.title('Survival Rate by Age Group')
    plt.ylabel('Survival Rate')
    plt.xticks(rotation=45)
    
    # Correlation heatmap
    plt.subplot(2, 3, 6)
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    correlation_matrix = df[numeric_cols].corr()
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
    plt.title('Feature Correlation')
    
    plt.tight_layout()
    plt.savefig('data/titanic_exploration.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f"\nExploration plots saved to: data/titanic_exploration.png")

def preprocess_data(df):
    """Preprocess the dataset for training"""
    # Create a copy to avoid modifying original data
    df_processed = df.copy()
    
    # Handle missing values
    df_processed['Age'].fillna(df_processed['Age'].median(), inplace=True)
    df_processed['Fare'].fillna(df_processed['Fare'].median(), inplace=True)
    df_processed['Embarked'].fillna('S', inplace=True)
    
    # Feature engineering
    df_processed['FamilySize'] = df_processed['SibSp'] + df_processed['Parch'] + 1
    df_processed['IsAlone'] = (df_processed['FamilySize'] == 1).astype(int)
    
    # Extract title from name
    df_processed['Title'] = df_processed['Name'].str.extract(' ([A-Za-z]+)\.', expand=False)
    df_processed['Title'] = df_processed['Title'].replace(['Lady', 'Countess','Capt', 'Col',
                                                         'Don', 'Dr', 'Major', 'Rev', 'Sir', 'Jonkheer', 'Dona'], 'Rare')
    df_processed['Title'] = df_processed['Title'].replace('Mlle', 'Miss')
    df_processed['Title'] = df_processed['Title'].replace('Ms', 'Miss')
    df_processed['Title'] = df_processed['Title'].replace('Mme', 'Mrs')
    
    # Age groups
    df_processed['AgeGroup'] = pd.cut(df_processed['Age'], bins=[0, 12, 18, 35, 60, 100], 
                                     labels=['Child', 'Teen', 'Adult', 'Middle', 'Senior'])
    
    # Fare groups - handle duplicate values
    try:
        df_processed['FareGroup'] = pd.qcut(df_processed['Fare'], q=4, labels=['Low', 'Medium', 'High', 'VeryHigh'], duplicates='drop')
    except ValueError:
        # If qcut fails due to duplicates, use cut instead
        df_processed['FareGroup'] = pd.cut(df_processed['Fare'], bins=4, labels=['Low', 'Medium', 'High', 'VeryHigh'])
    
    return df_processed

def encode_categorical_features(df):
    """Encode categorical features for machine learning"""
    df_encoded = df.copy()
    
    # Label encode categorical variables
    le_sex = LabelEncoder()
    le_embarked = LabelEncoder()
    le_title = LabelEncoder()
    le_age_group = LabelEncoder()
    le_fare_group = LabelEncoder()
    
    df_encoded['Sex'] = le_sex.fit_transform(df_encoded['Sex'])
    df_encoded['Embarked'] = le_embarked.fit_transform(df_encoded['Embarked'])
    df_encoded['Title'] = le_title.fit_transform(df_encoded['Title'])
    df_encoded['AgeGroup'] = le_age_group.fit_transform(df_encoded['AgeGroup'])
    df_encoded['FareGroup'] = le_fare_group.fit_transform(df_encoded['FareGroup'])
    
    # Save encoders for later use
    encoders = {
        'sex': le_sex,
        'embarked': le_embarked,
        'title': le_title,
        'age_group': le_age_group,
        'fare_group': le_fare_group
    }
    
    return df_encoded, encoders

def train_model(X_train, y_train, X_test, y_test):
    """Train Random Forest model"""
    # Initialize Random Forest classifier
    rf_model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42
    )
    
    # Train the model
    rf_model.fit(X_train, y_train)
    
    # Make predictions
    y_pred = rf_model.predict(X_test)
    
    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"Model Accuracy: {accuracy:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    return rf_model

def save_model_and_encoders(model, encoders, feature_columns):
    """Save the trained model and encoders"""
    # Create models directory if it doesn't exist
    os.makedirs('models', exist_ok=True)
    
    # Save the model
    with open('models/titanic_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    # Save encoders
    with open('models/encoders.pkl', 'wb') as f:
        pickle.dump(encoders, f)
    
    # Save feature columns
    with open('models/feature_columns.pkl', 'wb') as f:
        pickle.dump(feature_columns, f)
    
    print("Model and encoders saved successfully!")

def main():
    """Main training pipeline"""
    print("Loading Titanic dataset...")
    df = load_data()
    
    print("Exploring dataset...")
    explore_data(df)
    
    print("Preprocessing data...")
    df_processed = preprocess_data(df)
    
    print("Encoding categorical features...")
    df_encoded, encoders = encode_categorical_features(df_processed)
    
    # Select features for training
    feature_columns = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked', 
                      'FamilySize', 'IsAlone', 'Title', 'AgeGroup', 'FareGroup']
    
    X = df_encoded[feature_columns]
    y = df_encoded['Survived']
    
    print("Splitting data into train and test sets...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training Random Forest model...")
    model = train_model(X_train, y_train, X_test, y_test)
    
    print("Saving model and encoders...")
    save_model_and_encoders(model, encoders, feature_columns)
    
    print("\nTraining completed successfully!")
    print("Model saved to: models/titanic_model.pkl")
    print("Encoders saved to: models/encoders.pkl")
    print("Feature columns saved to: models/feature_columns.pkl")

if __name__ == "__main__":
    main()
