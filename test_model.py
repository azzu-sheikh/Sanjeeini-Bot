import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

def train_and_test_model():
    print("Loading datasets...")
    # Load training data
    train_df = pd.read_csv('training.csv')
    test_df = pd.read_csv('test_cases.csv')
    
    # Create and fit the vectorizer
    print("\nCreating TF-IDF vectorizer...")
    vectorizer = TfidfVectorizer(max_features=1000)
    X_train = vectorizer.fit_transform(train_df['Symptoms'])
    
    # Create and fit label encoder
    print("Encoding labels...")
    label_encoder = LabelEncoder()
    y_train = label_encoder.fit_transform(train_df['Condition'])
    
    # Train the model
    print("\nTraining Random Forest model...")
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    
    # Test accuracy on training data
    train_pred = clf.predict(X_train)
    train_accuracy = accuracy_score(y_train, train_pred)
    print(f"\nTraining Accuracy: {train_accuracy*100:.2f}%")
    
    # Test on test cases
    print("\nTesting on test cases...")
    X_test = vectorizer.transform(test_df['Symptoms'])
    y_test = label_encoder.transform(test_df['Expected_Condition'])
    
    # Get predictions
    test_pred = clf.predict(X_test)
    test_accuracy = accuracy_score(y_test, test_pred)
    
    print(f"\nTest Accuracy: {test_accuracy*100:.2f}%")
    print("\nClassification Report:")
    print(classification_report(y_test, test_pred, target_names=label_encoder.classes_))
    
    # Save the model and preprocessors
    print("\nSaving model and preprocessors...")
    joblib.dump(clf, 'medical_model.joblib')
    joblib.dump(vectorizer, 'tfidf_vectorizer.joblib')
    joblib.dump(label_encoder, 'label_encoder.joblib')
    
    # Test some example queries
    print("\nTesting example queries...")
    test_queries = [
        "I have fever and headache",
        "My stomach hurts and I feel nauseous",
        "I can't stop sneezing and my eyes are itchy",
        "I feel very tired and dizzy",
        "My chest feels tight and I'm having trouble breathing"
    ]
    
    X_queries = vectorizer.transform(test_queries)
    predictions = clf.predict(X_queries)
    probabilities = clf.predict_proba(X_queries)
    
    for i, query in enumerate(test_queries):
        condition = label_encoder.inverse_transform([predictions[i]])[0]
        confidence = np.max(probabilities[i]) * 100
        print(f"\nQuery: {query}")
        print(f"Predicted Condition: {condition}")
        print(f"Confidence: {confidence:.1f}%")

if __name__ == "__main__":
    train_and_test_model()
