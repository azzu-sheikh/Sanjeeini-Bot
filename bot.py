import re
import pandas as pd
import os
from medical_prediction import MedicalDiagnosisModel
from medicine_recommender import get_recommender
# Import the separate LLM service
from llm_service import LLMService
import logging

class SanjeeviniBot:
    def __init__(self):
        """Initialize the bot with necessary components"""
        self.model = MedicalDiagnosisModel()
        self.medicine_recommender = None
        self._load_medicine_recommender()
        self._load_or_train_model()
        self.doctors_df = None
        self._load_doctors_database()
        
        # Initialize the Local LLM Service
        self.llm_service = LLMService()
        
    def _load_or_train_model(self):
        """Load or train the medical diagnosis model"""
        try:
            if not self.model.trained:
                logging.error("No trained model found. Please run test_model.py first to train the model.")
                return False
            return True
            
        except Exception as e:
            logging.error(f"Error in load_or_train_model: {str(e)}")
            return False
    
    def _load_doctors_database(self):
        """Load the doctors database"""
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            self.doctors_df = pd.read_csv(os.path.join(script_dir, 'doctors_database.csv'))
        except Exception as e:
            logging.error(f"Error loading doctors database: {str(e)}")
            self.doctors_df = None
    
    def _load_medicine_recommender(self):
        """Load the medicine recommender"""
        try:
            self.medicine_recommender = get_recommender()
            if not self.medicine_recommender:
                logging.error("Failed to load medicine recommender")
        except Exception as e:
            logging.error(f"Error loading medicine recommender: {str(e)}")
            self.medicine_recommender = None

    def _find_doctor(self, condition):
        """Find appropriate doctor based on condition"""
        try:
            if not condition:
                return None

            # Map conditions to specialties
            specialty_map = {
                'Cold': 'General Physician',
                'Fever': 'General Physician',
                'Headache': 'General Physician',
                'Migraine': 'Neurologist',
                'Asthma': 'Pulmonologist',
                'Allergies': 'Allergist',
                'Skin': 'Dermatologist',
                'Joint Pain': 'Orthopedist',
                'Heart': 'Cardiologist',
                'Stomach': 'Gastroenterologist',
                'Mental': 'Psychiatrist',
                'ENT': 'ENT Specialist'
            }
            
            # Get specialty based on condition
            specialty = None
            condition_str = str(condition).lower()
            for key, value in specialty_map.items():
                if key.lower() in condition_str:
                    specialty = value
                    break
            
            if not specialty:
                specialty = 'General Physician'
            
            # Get doctors from database
            try:
                if self.doctors_df is None:
                    script_dir = os.path.dirname(os.path.abspath(__file__))
                    self.doctors_df = pd.read_csv(os.path.join(script_dir, 'doctors_database.csv'))
                
                # Clean the dataframe
                self.doctors_df = self.doctors_df.fillna('')  # Replace NaN with empty string
                
                # Filter by specialty
                matching_doctors = self.doctors_df[self.doctors_df['Specialization'].str.contains(specialty, case=False, na=False)]
                
                if matching_doctors.empty:
                    # Try to find a General Physician if no specialist is found
                    matching_doctors = self.doctors_df[self.doctors_df['Specialization'].str.contains('General', case=False, na=False)]
                
                if not matching_doctors.empty:
                    # Randomly select a doctor from matching specialists
                    doctor = matching_doctors.sample(n=1).iloc[0]
                    name = str(doctor['Name']).replace('Dr. ', '')
                    return f"\nRecommended {specialty}:\n{name}\n{doctor['Specialization']}\n{doctor['Education']}\nAvailable Hours: {doctor['Available_Hours']}\n\nNote: For your condition, I recommend starting with a {specialty} who can refer you to a specialist if needed."
                
            except Exception as e:
                print(f"Error reading doctors database: {str(e)}")
            
            return "I apologize, but I couldn't find a specific doctor recommendation. Please visit your nearest healthcare facility."
            
        except Exception as e:
            print(f"Error finding doctor: {str(e)}")
            return "I apologize, but I couldn't find a specific doctor recommendation. Please visit your nearest healthcare facility."

    def ai_generated_response(self, user_input):
        """Generate AI response using Local LLM (Phi-3)"""
        try:
            # Check for the specific prefix used by the AI button
            if "ai." not in user_input:
                return "Please use the 'ai.' prefix or click the AI button to get an AI-generated response."

            # Extract the actual prompt
            prompt = user_input.split("ai.", 1)[1].strip()

            # Call the local LLM service
            ai_response = self.llm_service.get_response(prompt)
            return ai_response

        except Exception as e:
            logging.error(f"Error in AI response generation: {str(e)}")
            return "Sorry, I couldn't get an AI response at the moment. Please ensure Ollama is running."

    def _format_response(self, condition, confidence, doctor_info):
        """Format the bot's response"""
        try:
            if condition is None:
                return "I apologize, but I couldn't understand the symptoms. Please describe them more clearly or provide more details."
            
            print(f"\nFormatting response for condition: {condition}")
            
            # Build response parts
            response_parts = [f"\nBased on your symptoms, you may have: {condition}"]
            print(f"Initial response parts: {response_parts}")
            
            # Get medicine recommendation
            print("Getting medicine recommendation...")
            if not self.medicine_recommender:
                print("Medicine recommender is None!")
                self._load_medicine_recommender()
            
            if self.medicine_recommender:
                medicine_info = self.medicine_recommender.get_recommendation(condition)
                print(f"Medicine info received: {medicine_info}")
                
                if medicine_info and isinstance(medicine_info, dict):
                    print("Adding medicine info to response")
                    print(f"Medicine keys: {medicine_info.keys()}")
                    try:
                        med_parts = [
                            "\nRecommended Medicine:",
                            f"- Name: {medicine_info.get('Medicine', 'Unknown')}",
                            f"- Dosage: {medicine_info.get('Dosage', 'Unknown')}",
                            f"- Precautions: {medicine_info.get('Precautions', 'Unknown')}"
                        ]
                        print(f"Medicine parts to add: {med_parts}")
                        response_parts.extend(med_parts)
                    except Exception as e:
                        print(f"Error adding medicine parts: {str(e)}")
                else:
                    print(f"Invalid medicine info: {medicine_info}")
            else:
                print("Medicine recommender still None after reload!")
            
            # Add doctor info
            if doctor_info:
                print("Adding doctor info to response")
                response_parts.append(doctor_info)
            
            # Join all parts
            response = "\n".join(response_parts)
            print(f"Final response parts: {response_parts}")
            print(f"Final response: {response}")
            return response
            
        except Exception as e:
            print(f"Error formatting response: {str(e)}")
            print(f"Error type: {type(e)}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            return "I apologize, but I'm having trouble formatting the response. Please try again."

    def chat(self, user_input):
        """Process user input and generate response (Non-AI button flow)"""
        try:
            # Check for empty input
            if not user_input or not user_input.strip():
                return "Please provide some symptoms or ask a health-related question."

            # Get condition and confidence from model
            condition, confidence = self.model.predict(user_input)
            print(f"Predicted condition: {condition} with confidence: {confidence}")

            # Get doctor recommendation
            doctor_info = self._find_doctor(condition) if condition else None
            
            # Format response
            response = self._format_response(condition, confidence, doctor_info)
            print(f"Final response: {response}")
            return response

        except Exception as e:
            print(f"Error in chat: {str(e)}")
            return "I apologize, but I'm having trouble processing your request. Please try again."

# Create a singleton instance
_bot_instance = None

def get_bot_instance():
    """Get or create the singleton bot instance"""
    global _bot_instance
    if _bot_instance is None:
        _bot_instance = SanjeeviniBot()
    return _bot_instance