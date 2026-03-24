from langchain_ollama import OllamaLLM
import logging

class LLMService:
    def __init__(self):
        """Initialize the Phi-3 Mini model via Ollama"""
        try:
            # Initialize with the specific model tag 'phi3:mini'
            self.llm = OllamaLLM(model="phi3:mini") 
            print("Local LLM (Phi-3:mini) initialized successfully")
        except Exception as e:
            logging.error(f"Failed to initialize Ollama: {str(e)}")
            self.llm = None

    def get_response(self, prompt):
        """Generate response using the local LLM with medical context"""
        if not self.llm:
            return "Error: Local LLM service is not available. Please ensure Ollama is running."
        
        try:
            # UPDATED SYSTEM PROMPT: 
            # Instructs the AI to suggest OTC meds (like Dolo/Paracetamol) but enforce a disclaimer.
            system_context = (
                "You are Sanjeevini, a helpful medical AI assistant. "
                "Instructions:\n"
                "1. If the user asks for medicine for common symptoms (like fever, cold, headache, body pain), "
                "you ARE ALLOWED to suggest common Over-The-Counter (OTC) medications (e.g., Dolo-650 or Paracetamol for fever, Cetirizine for cold).\n"
                "2. Do NOT simply refuse to answer. Provide a helpful suggestion.\n"
                "3. You MUST end your response with this exact disclaimer: "
                "'Disclaimer: I am an AI, not a doctor. This is a suggestion, not a prescription. Please consult a healthcare professional before taking any medication.'"
            )
            
            full_prompt = f"{system_context}\n\nUser Question: {prompt}\nSanjeevini:"
            
            response = self.llm.invoke(full_prompt)
            return response
            
        except Exception as e:
            logging.error(f"Error generating LLM response: {str(e)}")
            return "I apologize, but I couldn't generate a response at the moment. Please ensure the local AI service is running."