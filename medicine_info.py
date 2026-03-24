import pandas as pd
import os

class MedicineInfo:
    def __init__(self):
        self.medicines_data = {}
        self._load_medicines_data()
        
    def _load_medicines_data(self):
        """Load medicine data from CSV file"""
        try:
            # Read the CSV file
            with open('medicine.csv', 'r') as file:
                for line in file:
                    # Split each line into condition and medicine info
                    parts = line.strip().split(',', 1)
                    if len(parts) == 2:
                        condition = parts[0].strip()
                        medicine_info = parts[1].strip()
                        self.medicines_data[condition.lower()] = medicine_info
        except Exception as e:
            print(f"Error loading medicine data: {str(e)}")
            
    def get_medicine_for_condition(self, condition):
        """Get medicine information for a specific condition"""
        condition = condition.lower()
        return self.medicines_data.get(condition, "Medicine information not available for this condition.")
        
    def get_medicine_info(self, medicine_name):
        """Get information about a specific medicine"""
        medicine_name = medicine_name.lower()
        # Search through all medicine information for the medicine name
        for condition, info in self.medicines_data.items():
            if medicine_name in info.lower():
                return f"Medicine: {medicine_name}\nUsed for: {condition}\nInformation: {info}"
        return f"Information not available for {medicine_name}"
