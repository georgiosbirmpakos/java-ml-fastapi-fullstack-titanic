# Titanic ML Model

This directory contains the machine learning pipeline for predicting Titanic passenger survival using the actual Kaggle dataset.

## Features

- **Real Data**: Uses the actual Titanic dataset from Kaggle
- **Data Exploration**: Comprehensive analysis and visualization
- **Feature Engineering**: Advanced preprocessing and feature creation
- **Model Training**: Random Forest classifier with hyperparameter tuning
- **Model Persistence**: Pickle serialization for production use

## Quick Start

### Option 1: Automated Setup
```bash
cd ml-model
python setup_and_train.py
```

### Option 2: Manual Setup

1. **Download the dataset:**
```bash
python download_data.py
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Train the model:**
```bash
python train.py
```

## Dataset

The script will automatically download the Titanic dataset. If automatic download fails, you can manually download it from:
- [Kaggle Titanic Competition](https://www.kaggle.com/c/titanic/data)
- Place `train.csv` in the `data/` directory

## Files Generated

After training, the following files will be created:

- `models/titanic_model.pkl` - Trained Random Forest model
- `models/encoders.pkl` - Feature encoders for categorical variables
- `models/feature_columns.pkl` - List of features used in training
- `data/titanic_exploration.png` - Data visualization plots

## Model Performance

The model typically achieves:
- **Accuracy**: ~80-85% on test set
- **Features**: 12 engineered features including age groups, family size, title extraction
- **Algorithm**: Random Forest with 100 estimators

## Usage in Production

The trained model can be loaded and used for predictions:

```python
from predict import TitanicPredictor

# Initialize predictor
predictor = TitanicPredictor()

# Make prediction
passenger_data = {
    'Pclass': 1,
    'Name': 'Mr. John Doe',
    'Sex': 'male',
    'Age': 35.0,
    'SibSp': 0,
    'Parch': 0,
    'Fare': 50.0,
    'Embarked': 'S'
}

result = predictor.predict_survival(passenger_data)
print(result)
```

## Data Preprocessing

The model performs extensive preprocessing:

1. **Missing Value Handling**: Age and Fare imputation
2. **Feature Engineering**: 
   - Family size calculation
   - Title extraction from names
   - Age and fare grouping
   - Alone passenger flag
3. **Categorical Encoding**: Label encoding for all categorical variables

## Model Architecture

- **Algorithm**: Random Forest Classifier
- **Parameters**:
  - n_estimators: 100
  - max_depth: 10
  - min_samples_split: 5
  - min_samples_leaf: 2
  - random_state: 42

## Next Steps

After training the model, you can:
1. Start the FastAPI backend: `cd ../fastapi-backend && python main.py`
2. Test the API: `python test_api.py`
3. Run the Java frontend application
