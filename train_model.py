from medical_prediction import MedicalDiagnosisModel
import os
import pandas as pd

def main():
    # Initialize the model
    model = MedicalDiagnosisModel()

    # Get the absolute paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    training_data_path = os.path.join(current_dir, 'training.csv')
    test_data_path = os.path.join(current_dir, 'test_cases.csv')

    # Train the model
    print("Training model with data from:", training_data_path)
    model.train(training_data_path)

    # Save the trained model
    model.save_model('medical_model.joblib')

    # Load test cases
    test_cases = pd.read_csv(test_data_path)
    
    print("\nTesting model with example symptoms:")
    correct_predictions = 0
    total_cases = len(test_cases)

    for _, test_case in test_cases.iterrows():
        symptoms = test_case['Symptoms']
        expected = test_case['Expected_Condition']
        
        print(f"\nInput symptoms: {symptoms}")
        print(f"Expected condition: {expected}")
        
        prediction = model.predict(symptoms)
        if prediction:
            predicted = prediction['predicted_condition'].replace('"', '')
            confidence = prediction['confidence']
            
            print(f"Predicted condition: {predicted}")
            print(f"Confidence: {confidence:.2%}")
            
            if predicted == expected:
                correct_predictions += 1
                print(" Correct prediction!")
            else:
                print(" Incorrect prediction")
            
            print("\nTop 3 predictions:")
            for pred in prediction['top_3_predictions']:
                condition = pred['condition'].replace('"', '')
                probability = pred['probability']
                print(f"- {condition}: {probability:.2%}")
            
            print("\nImportant symptoms identified:")
            for symptom in prediction['important_symptoms']:
                print(f"- {symptom['term']}: {symptom['importance']:.4f}")
    
    accuracy = (correct_predictions / total_cases) * 100
    print(f"\nOverall Test Accuracy: {accuracy:.1f}%")
    print(f"Correct predictions: {correct_predictions}/{total_cases}")

if __name__ == "__main__":
    main()
