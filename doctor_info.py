import pandas as pd
import os

class DoctorInfo:
    def __init__(self):
        self.doctors_file = 'doctors_database.csv'
        self.doctors_data = None
        self.load_doctors_data()
        
        # Mapping conditions to specializations
        self.condition_to_specialist = {
            'cold': 'General Physician',
            'fever': 'General Physician',
            'headache': 'General Physician',
            'migraine': 'Neurologist',
            'skin infection': 'Dermatologist',
            'acne': 'Dermatologist',
            'heart': 'Cardiologist',
            'chest pain': 'Cardiologist',
            'ear pain': 'ENT Specialist',
            'throat': 'ENT Specialist',
            'bone': 'Orthopedic',
            'joint pain': 'Orthopedic',
            'depression': 'Psychiatrist',
            'anxiety': 'Psychiatrist',
            'eye': 'Ophthalmologist',
            'vision': 'Ophthalmologist'
        }

    def load_doctors_data(self):
        """Load doctors data from CSV file"""
        try:
            if os.path.exists(self.doctors_file):
                self.doctors_data = pd.read_csv(self.doctors_file)
            else:
                print(f"Error: {self.doctors_file} not found")
                self.doctors_data = None
        except Exception as e:
            print(f"Error loading doctors data: {str(e)}")
            self.doctors_data = None

    def get_doctor_by_specialization(self, specialization):
        """Get doctors by specialization"""
        if self.doctors_data is None:
            return "Doctor information not available at the moment."
        
        doctors = self.doctors_data[self.doctors_data['Specialization'] == specialization]
        if doctors.empty:
            return "No doctors found for this specialization."
        
        # Sort by rating and get top doctors
        doctors = doctors.sort_values('Rating', ascending=False)
        
        # Format doctor information
        doctor_info = []
        for _, doctor in doctors.iterrows():
            info = (
                f"Name: {doctor['Name']}\n"
                f"Specialization: {doctor['Specialization']}\n"
                f"Experience: {doctor['Experience']} years\n"
                f"Location: {doctor['Location']}\n"
                f"Contact: {doctor['Contact']}\n"
                f"Available Hours: {doctor['Available_Hours']}\n"
                f"Rating: {doctor['Rating']}/5.0"
            )
            doctor_info.append(info)
        
        return "\n\n".join(doctor_info)

    def get_recommended_doctors(self, condition):
        """Get recommended doctors based on condition"""
        if self.doctors_data is None:
            return "Doctor information not available at the moment."
        
        # Convert condition to lowercase for matching
        condition = condition.lower()
        
        # Find matching specialization
        specialization = None
        for key, value in self.condition_to_specialist.items():
            if key in condition:
                specialization = value
                break
        
        # If no specific match found, default to General Physician
        if not specialization:
            specialization = 'General Physician'
        
        return self.get_doctor_by_specialization(specialization)

    def search_doctors(self, query):
        """Search doctors by name, specialization, or location"""
        if self.doctors_data is None:
            return "Doctor information not available at the moment."
        
        query = query.lower()
        results = []
        
        for _, doctor in self.doctors_data.iterrows():
            if (query in doctor['Name'].lower() or 
                query in doctor['Specialization'].lower() or 
                query in doctor['Location'].lower()):
                info = (
                    f"Name: {doctor['Name']}\n"
                    f"Specialization: {doctor['Specialization']}\n"
                    f"Experience: {doctor['Experience']} years\n"
                    f"Location: {doctor['Location']}\n"
                    f"Contact: {doctor['Contact']}\n"
                    f"Available Hours: {doctor['Available_Hours']}\n"
                    f"Rating: {doctor['Rating']}/5.0"
                )
                results.append(info)
        
        if not results:
            return "No doctors found matching your search criteria."
        
        return "\n\n".join(results)
