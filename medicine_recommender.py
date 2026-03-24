import pandas as pd
import os

class MedicineRecommender:
    def __init__(self):
        """Initialize the medicine recommender"""
        print("Initializing MedicineRecommender...")
        self.medicine_df = None
        self.load_medicine_data()
        
    def load_medicine_data(self):
        """Load medicine database"""
        try:
            # Get absolute path to medicine.csv
            script_dir = os.path.dirname(os.path.abspath(__file__))
            medicine_path = os.path.join(script_dir, 'medicine.csv')
            print(f"Loading medicine data from: {medicine_path}")
            
            # Load the CSV file
            self.medicine_df = pd.read_csv(medicine_path)
            print(f"Loaded {len(self.medicine_df)} medicine records")
            
            # Clean the data
            self.medicine_df = self.medicine_df.fillna('')
            for col in ['Condition', 'Medicine', 'Dosage', 'Precautions']:
                self.medicine_df[col] = self.medicine_df[col].astype(str).str.strip()
            
            print("Medicine database loaded successfully")
            print(f"Available conditions: {', '.join(self.medicine_df['Condition'].unique())}")
            
        except Exception as e:
            print(f"Error loading medicine database: {str(e)}")
            self.medicine_df = None

    def get_recommendation(self, condition):
        """Get medicine recommendation for a condition"""
        try:
            if self.medicine_df is None:
                print("Medicine database not loaded")
                return None
                
            if not condition:
                print("No condition provided")
                return None
            
            # Clean and standardize the condition
            condition = str(condition).strip().lower()
            print(f"Looking for medicine for condition: {condition}")
            
            # Try exact match first
            match = self.medicine_df[self.medicine_df['Condition'].str.lower() == condition]
            print(f"Found {len(match)} exact matches for condition: {condition}")
            
            if len(match) > 0:
                row = match.iloc[0]
                result = {
                    'Medicine': str(row['Medicine']).strip(),
                    'Dosage': str(row['Dosage']).strip(),
                    'Precautions': str(row['Precautions']).strip()
                }
                print(f"Returning medicine info: {result}")
                return result
            
            # Try partial match if exact match fails
            partial_matches = self.medicine_df[self.medicine_df['Condition'].str.lower().str.contains(condition)]
            if len(partial_matches) > 0:
                row = partial_matches.iloc[0]
                result = {
                    'Medicine': str(row['Medicine']).strip(),
                    'Dosage': str(row['Dosage']).strip(),
                    'Precautions': str(row['Precautions']).strip()
                }
                print(f"Found partial match. Returning: {result}")
                return result
            
            # Try checking if condition contains any medicine condition
            for idx, row in self.medicine_df.iterrows():
                if row['Condition'].lower() in condition:
                    result = {
                        'Medicine': str(row['Medicine']).strip(),
                        'Dosage': str(row['Dosage']).strip(),
                        'Precautions': str(row['Precautions']).strip()
                    }
                    print(f"Found reverse partial match. Returning: {result}")
                    return result
            
            print(f"No medicine found for condition: {condition}")
            print(f"Available conditions: {', '.join(self.medicine_df['Condition'].unique())}")
            return None
            
        except Exception as e:
            print(f"Error in get_recommendation: {str(e)}")
            print(f"Error type: {type(e)}")
            return None

# Create a singleton instance
_recommender_instance = None

def get_recommender():
    """Get or create the singleton medicine recommender instance"""
    global _recommender_instance
    if _recommender_instance is None:
        print("Creating new MedicineRecommender instance")
        _recommender_instance = MedicineRecommender()
    return _recommender_instance
