import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import joblib
import re
import os

class MedicalDiagnosisModel:
    def __init__(self):
        """Initialize the model"""
        self.trained = False
        self.classifier = None
        self.vectorizer = None
        self.label_encoder = None
        
        # Try to load pre-trained model
        try:
            self.load_model('medical_model.joblib')
        except Exception as e:
            print(f"No pre-trained model found: {str(e)}")
    
    def load_model(self, model_path='medical_model.joblib'):
        """Load a trained model from files"""
        try:
            if not os.path.exists(model_path):
                print(f"Model file {model_path} not found")
                return False
                
            if not os.path.exists('tfidf_vectorizer.joblib') or not os.path.exists('label_encoder.joblib'):
                print("Vectorizer or label encoder files not found")
                return False
                
            self.classifier = joblib.load(model_path)
            self.vectorizer = joblib.load('tfidf_vectorizer.joblib')
            self.label_encoder = joblib.load('label_encoder.joblib')
            self.trained = True
            print("Model loaded successfully")
            return True
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            return False
    
    def preprocess_symptoms(self, symptoms_text):
        """Clean and standardize symptom text"""
        # Convert to lowercase
        text = symptoms_text.lower()
        
        # Remove common words that don't add meaning
        text = text.replace("i am", "")
        text = text.replace("i'm", "")
        text = text.replace("i have", "")
        text = text.replace("having", "")
        text = text.replace("experiencing", "")
        text = text.replace("suffering from", "")
        text = text.replace("feeling", "")
        text = text.replace("got", "")
        text = text.replace("getting", "")
        
        # Handle simple symptom statements
        simple_symptoms = {
            'fever': 'fever, fatigue, high temperature',
            'have fever': 'fever, fatigue, high temperature',
            'got fever': 'fever, fatigue, high temperature',
            'cold': 'cough, runny nose, sneezing',
            'have cold': 'cough, runny nose, sneezing',
            'got cold': 'cough, runny nose, sneezing',
            'cough': 'cough, throat irritation',
            'headache': 'headache, pain in head',
            'body pain': 'body pain, muscle ache',
            'stomach pain': 'stomach pain, abdominal pain',
            'allergy': 'sneezing, itchy eyes, runny nose, skin rash',
            'allergies': 'sneezing, itchy eyes, runny nose, skin rash',
            'allergic': 'sneezing, itchy eyes, runny nose, skin rash'
        }
        
        # Check for simple symptoms first
        for symptom, expanded in simple_symptoms.items():
            if symptom in text:
                text = expanded
                break
        
        # Handle common symptom variations
        replacements = {
            'body pain': 'muscle ache',
            'body ache': 'muscle ache',
            'muscle pain': 'muscle ache',
            'pain in body': 'muscle ache',
            'aches': 'muscle ache',
            'shortness of breath': 'breathing difficulty',
            'cant breathe': 'breathing difficulty',
            'having trouble breathing': 'breathing difficulty',
            'stomach ache': 'stomach pain',
            'head pain': 'headache',
            'pain in head': 'headache',
            'hay fever': 'sneezing, itchy eyes, runny nose',
            'itchy skin': 'skin rash',
            'skin irritation': 'skin rash',
            'rashes': 'skin rash'
        }
        
        for old, new in replacements.items():
            text = text.replace(old, new)
            
        # Remove special characters but keep spaces and commas
        text = re.sub(r'[^a-z\s,]', ' ', text)
        
        return text.strip()
    
    def train(self, training_data_path):
        """Train the model with new data"""
        try:
            # Load and preprocess training data
            df = pd.read_csv(training_data_path)
            
            # Preprocess symptoms
            df['Processed_Symptoms'] = df['Symptoms'].apply(self.preprocess_symptoms)
            
            # Initialize and fit vectorizer
            self.vectorizer = TfidfVectorizer(max_features=1000)
            X = self.vectorizer.fit_transform(df['Processed_Symptoms'])
            
            # Initialize and fit label encoder
            self.label_encoder = LabelEncoder()
            y = self.label_encoder.fit_transform(df['Condition'])
            
            # Train the classifier
            self.classifier = RandomForestClassifier(n_estimators=100, random_state=42)
            self.classifier.fit(X, y)
            
            # Save the model and components
            joblib.dump(self.classifier, 'medical_model.joblib')
            joblib.dump(self.vectorizer, 'tfidf_vectorizer.joblib')
            joblib.dump(self.label_encoder, 'label_encoder.joblib')
            
            self.trained = True
            print("Model trained and saved successfully")
            return True
            
        except Exception as e:
            print(f"Error training model: {str(e)}")
            return False
    
    def predict(self, symptoms_text):
        """Make a prediction based on input symptoms"""
        if not self.trained:
            print("Debug - Model not trained")
            return None, 0
            
        try:
            print(f"\nDebug - MedicalDiagnosisModel.predict - Input: {symptoms_text}")
            
            # Handle empty input
            if not symptoms_text or len(symptoms_text.strip()) < 3:
                print("Debug - Input too short")
                return None, 0
            
            # Preprocess input symptoms
            processed_symptoms = self.preprocess_symptoms(symptoms_text)
            print(f"Debug - Preprocessed symptoms: {processed_symptoms}")
            
            # Handle common simple inputs directly
            simple_conditions = {
                'fever': ('Fever', 85.0),
                'cold': ('Cold', 85.0),
                'headache': ('Headache', 85.0),
                'cough': ('Cold', 75.0),
                'body pain': ('Body Pain', 75.0),
                'muscle ache': ('Body Pain', 75.0),
                'stomach pain': ('GERD', 75.0)
            }
            
            # Check for simple conditions
            for symptom, (condition, confidence) in simple_conditions.items():
                if symptom in processed_symptoms:
                    print(f"Debug - Matched simple condition: {condition}")
                    return condition, confidence
            
            # Transform to TF-IDF features
            try:
                print("Debug - Transforming text to TF-IDF features")
                symptoms_vec = self.vectorizer.transform([processed_symptoms])
                print("Debug - Successfully transformed text")
                
                # Get prediction probabilities
                print("Debug - Getting prediction probabilities")
                probs = self.classifier.predict_proba(symptoms_vec)[0]
                print(f"Debug - Prediction probabilities: {probs}")
                
                # Get top prediction
                top_idx = np.argmax(probs)
                condition = self.label_encoder.inverse_transform([top_idx])[0]
                confidence = float(probs[top_idx]) * 100  # Convert to percentage
                print(f"Debug - Top prediction: {condition} with confidence {confidence}%")
                
                return condition, confidence
                
            except Exception as e:
                print(f"Debug - Error during vectorization/prediction: {str(e)}")
                # Fall back to symptom matching
                print("Debug - Falling back to symptom matching")
                
                symptom_conditions = {
                    'fever': ['fever', 'temperature', 'hot'],
                    'cold': ['cold', 'cough', 'sneezing', 'runny nose'],
                    'headache': ['headache', 'head pain'],
                    'body pain': ['body pain', 'muscle', 'joint'],
                    'stomach': ['stomach', 'abdomen', 'digestive'],
                    'breathing': ['breath', 'wheeze', 'cough'],
                    'allergy': ['allergy', 'rash', 'itchy']
                }
                
                for condition, keywords in symptom_conditions.items():
                    if any(keyword in processed_symptoms for keyword in keywords):
                        print(f"Debug - Matched condition through keywords: {condition}")
                        return condition.title(), 75.0
                        
                return None, 0
                
        except Exception as e:
            print(f"Debug - Error in predict: {str(e)}")
            print(f"Debug - Full error: ", e.__class__.__name__, str(e))
            import traceback
            print("Debug - Traceback:", traceback.format_exc())
            return None, 0
            
    def save_model(self, model_path='medical_model.joblib'):
        """Save the trained model"""
        if not self.trained:
            return False
            
        try:
            joblib.dump(self.classifier, model_path)
            joblib.dump(self.vectorizer, 'tfidf_vectorizer.joblib')
            joblib.dump(self.label_encoder, 'label_encoder.joblib')
            return True
        except Exception as e:
            print(f"Error saving model: {str(e)}")
            return False
