"""
India Crop Yield Prediction Model
Trained on Government of India Agricultural Statistics
Based on data from Ministry of Agriculture & Farmers Welfare
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import joblib
import os
from pathlib import Path

# Paths
DATA_DIR = Path(__file__).parent / 'data'
MODEL_DIR = Path(__file__).parent / 'models'

def train_model():
    """Train Random Forest model on India crop data"""
    
    # Load data
    df = pd.read_csv(DATA_DIR / 'india_crop_data.csv')
    
    # Create encoders
    encoders = {}
    categorical_cols = ['State', 'District', 'Crop', 'Season', 'Soil_Type']
    
    for col in categorical_cols:
        encoders[col] = LabelEncoder()
        df[f'{col}_encoded'] = encoders[col].fit_transform(df[col])
    
    # Features for prediction
    feature_cols = [
        'State_encoded', 'District_encoded', 'Crop_encoded', 
        'Season_encoded', 'Soil_Type_encoded',
        'Annual_Rainfall_mm', 'Irrigation_Percent', 
        'Fertilizer_Kg_Ha', 'Temperature_Avg_C'
    ]
    
    X = df[feature_cols]
    y = df['Yield_Kg_Ha']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train Random Forest
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=15,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    
    # Score
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    
    print(f"Training R² Score: {train_score:.4f}")
    print(f"Testing R² Score: {test_score:.4f}")
    
    # Feature importance
    importance = dict(zip(feature_cols, model.feature_importances_))
    print("\nFeature Importance:")
    for feat, imp in sorted(importance.items(), key=lambda x: x[1], reverse=True):
        print(f"  {feat}: {imp:.4f}")
    
    # Save model and encoders
    MODEL_DIR.mkdir(exist_ok=True)
    joblib.dump(model, MODEL_DIR / 'yield_model.pkl')
    joblib.dump(encoders, MODEL_DIR / 'encoders.pkl')
    
    # Save training stats
    stats = {
        'train_score': train_score,
        'test_score': test_score,
        'feature_importance': importance,
        'n_samples': len(df),
        'unique_states': df['State'].nunique(),
        'unique_crops': df['Crop'].nunique(),
        'unique_districts': df['District'].nunique()
    }
    joblib.dump(stats, MODEL_DIR / 'model_stats.pkl')
    
    print(f"\nModel saved to {MODEL_DIR}")
    print(f"Trained on {len(df)} samples from {df['State'].nunique()} states")
    
    return model, encoders, stats

if __name__ == '__main__':
    train_model()
