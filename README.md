# Sanjeevinibot
Sanjeevini Bot is an intelligent chatbot designed to assist users with health-related queries. It provides medicine suggestions, AI-generated responses, and answers frequently asked health questions.

# Overview
    The Chatbot-GUI is a user-friendly interface that enables seamless interactions with a chatbot using visual elements like text boxes, menus, and buttons. This project combines Natural Language Processing (NLP) techniques with Tkinter for GUI development, making it a versatile tool for interactive communication.

# Key Functionalities
    Text Input & Output: Users can type queries in a text box, and responses are displayed in the interface.
    AI-Powered Responses: Leverages NLP and machine learning to generate relevant replies.
    Medicine Suggestions: Provides medicine recommendations based on user input.
    Add Medicine Information: Allows users to expand the chatbot’s knowledge base by adding new medicine-condition pairs.
    Interactive Greetings & FAQs: Responds to greetings and frequently asked questions.
    Expandable Features: Supports voice recognition, text-to-speech, and sentiment analysis.

# How It Works
The chatbot is built using:

Tkinter: For creating graphical elements like buttons, menus, and input fields.
NLTK: For tokenization, lemmatization, and processing natural language.
CSV Module: To store and retrieve medicine-condition pairs.
OpenAI API: For generating advanced AI-powered responses.

# Features
- **AI-Generated Responses**: Get detailed answers using AI for any query.
- **Medicine Suggestions**: Retrieve medicine recommendations by typing `med.<condition>`.
- **FAQ Support**: Ask common health-related questions for instant answers.
- **Interactive Conversations**: Engage with the bot using greetings or casual queries.
- **Add New Medicine Data**: Expand the bot's knowledge by adding new conditions and medicines.

# How to Use
1. **Retrieve Medicine Suggestions**:
   - Use the prefix `med.` followed by the condition.
   - Example: `med.cold`

2. **Get AI-Generated Responses**:
   - Use the prefix `ai.` followed by your question.
   - Example: `ai.What is AI?`

3. **Ask General Questions**:
   - Simply type your question or greeting.
   - Example: `What are the symptoms of flu?` or `Hello`

4. **Add New Medicine Data**:
   - Format: `condition=medicine`
   - Example: `headache=aspirin`

5. **Exit the Chat**:
   - Type `bye`, `exit`, or `quit`.

# Installation
    1. Python 3.7 or higher
    2. Required Libraries:
    3. nltk
    4. tkinter
    5. csv
    6. openai

# Contributors 
   - *Azeem Sheikh*
   - *Chinmay Hegde*
   - *Aman Khan*
   - *Harshith Doijode*
    