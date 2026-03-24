from tkinter import *
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from PIL import Image, ImageTk
from bot import get_bot_instance
from medical_prediction import MedicalDiagnosisModel
from doctor_gui import DoctorManagementGUI
import os
import threading
import pyttsx3
import csv
import logging

# Set up logging
logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')
# Suppress comtypes debug output
logging.getLogger('comtypes').setLevel(logging.WARNING)

class ChatInterface(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        
        # Initialize bot instance
        self.bot = get_bot_instance()

        # Track if introduction has been shown
        self.intro_shown = False

        # Default colors and fonts
        self.tl_bg = "#EEEEEE"
        self.tl_bg2 = "#EEEEEE"
        self.tl_fg = "#000000"
        self.font = "Verdana 12"

        # Initialize voice engine
        self.engine = pyttsx3.init()
        self.voice = 'female'  # Default voice
        self.update_voice()

        # Create menu bar
        self.create_menu_bar()

        # Load and resize icons
        script_dir = os.path.dirname(os.path.abspath(__file__))
        bot_icon = Image.open(os.path.join(script_dir, "bot_icon.png"))
        human_icon = Image.open(os.path.join(script_dir, "human_icon.png"))
        
        # Resize icons to 40x40 pixels
        bot_icon = bot_icon.resize((50, 50), Image.Resampling.LANCZOS)
        human_icon = human_icon.resize((50, 50), Image.Resampling.LANCZOS)
        
        self.bot_photo = ImageTk.PhotoImage(bot_icon)
        self.human_photo = ImageTk.PhotoImage(human_icon)

        # Chat display frame
        self.text_frame = Frame(self.master, bd=6)
        self.text_frame.pack(expand=True, fill=BOTH)

        # Scrollbar for chat messages
        self.text_box_scrollbar = Scrollbar(self.text_frame, bd=0)
        self.text_box_scrollbar.pack(fill=Y, side=RIGHT)

        # Chat messages text box
        self.text_box = Text(self.text_frame, yscrollcommand=self.text_box_scrollbar.set, state=DISABLED,
                             bd=1, padx=6, pady=6, wrap=WORD, font=self.font, relief=GROOVE)
        self.text_box.pack(expand=True, fill=BOTH)
        self.text_box_scrollbar.config(command=self.text_box.yview)

        # Configure tags for different message types
        self.text_box.tag_configure("human", foreground="#007AFF", font="Verdana 12 bold")
        self.text_box.tag_configure("bot", foreground="#4CAF50", font="Verdana 12")

        # Find Doctor Button frame
        self.doctor_frame = Frame(self.master, bd=1)
        self.doctor_frame.pack(fill=X, padx=5, pady=(5,0))
        
        self.doctors_button = Button(
            self.doctor_frame,
            text="Find Doctor",
            font="Verdana 10 bold",
            bg="#4CAF50",
            fg="white",
            command=self.handle_doctors_button
        )
        self.doctors_button.pack(side=LEFT, padx=5, pady=5)

        # AI Button
        self.ai_button = Button(
            self.doctor_frame,
            text="AI",
            font="Verdana 10 bold",
            bg="#007AFF",
            fg="white",
            command=self.handle_ai_button
        )
        self.ai_button.pack(side=LEFT, padx=5, pady=5)

        # Entry field frame with send button
        self.entry_frame = Frame(self.master, bd=1)
        self.entry_frame.pack(fill=BOTH, padx=5, pady=5)

        # Entry field
        self.text_input = Text(self.entry_frame, bd=1, font="Verdana 12", height=2)
        self.text_input.pack(side=LEFT, fill=X, expand=True, padx=5, pady=5)
        self.text_input.bind("<Return>", self.send_message)

        # Send button
        self.send_button = Button(
            self.entry_frame,
            text="Send",
            font="Verdana 12 bold",
            width=8,
            bg="#00b894",
            fg="#ffffff",
            command=self.send_message
        )
        self.send_button.pack(side=RIGHT, padx=5, pady=5)

        # Create a separate frame for last sent label below entry field
        self.status_frame = Frame(self.master, bd=1)
        self.status_frame.pack(fill=X, padx=5)

        self.last_sent_label(date="No messages sent.")

    def create_menu_bar(self):
        """Create the menu bar with all options"""
        menu = Menu(self.master)
        self.master.config(menu=menu, bd=5)

        # File Menu
        file_menu = Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Clear Chat", command=self.clear_chat)
        file_menu.add_command(label="Exit", command=self.chatexit)

        # Options Menu
        options_menu = Menu(menu, tearoff=0)
        menu.add_cascade(label="Options", menu=options_menu)

        # Font submenu
        font_menu = Menu(options_menu, tearoff=0)
        options_menu.add_cascade(label="Font", menu=font_menu)
        font_menu.add_command(label="Default", command=lambda: self.change_font("Verdana 12"))
        font_menu.add_command(label="Times", command=lambda: self.change_font("Times 10"))
        font_menu.add_command(label="System", command=lambda: self.change_font("System 10"))
        font_menu.add_command(label="Helvetica", command=lambda: self.change_font("Helvetica 10"))
        font_menu.add_command(label="Fixedsys", command=lambda: self.change_font("Fixedsys 10"))

        # Theme submenu
        theme_menu = Menu(options_menu, tearoff=0)
        options_menu.add_cascade(label="Theme", menu=theme_menu)
        theme_menu.add_command(label="Default", command=self.theme_default)
        theme_menu.add_command(label="Night", command=self.theme_dark)
        theme_menu.add_command(label="Grey", command=self.theme_grey)
        theme_menu.add_command(label="Blue", command=self.theme_blue)
        theme_menu.add_command(label="Hacker", command=self.theme_hacker)

        # Voice submenu
        voice_menu = Menu(options_menu, tearoff=0)
        options_menu.add_cascade(label="Voice", menu=voice_menu)
        voice_menu.add_command(label="Male", command=self.set_male_voice)
        voice_menu.add_command(label="Female", command=self.set_female_voice)

        # Help Menu
        help_menu = Menu(menu, tearoff=0)
        menu.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About Sanjeevini Bot", command=self.show_about)
        help_menu.add_command(label="Developers", command=self.show_developers)

    def create_function_buttons(self):
        """Create the function buttons"""
        pass  # No longer needed as the doctor button is now in the entry frame

    def clear_chat(self):
        """Clear all messages from the chat"""
        self.text_box.config(state=NORMAL)
        self.text_box.delete(1.0, END)
        self.text_box.config(state=DISABLED)
        self.last_sent_label(date="No messages sent.")

    def chatexit(self):
        """Exit the application"""
        exit()

    def set_male_voice(self):
        """Set voice to male"""
        self.voice = 'male'
        self.update_voice()

    def set_female_voice(self):
        """Set voice to female"""
        self.voice = 'female'
        self.update_voice()

    def update_voice(self):
        """Update the voice engine settings"""
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[0].id if self.voice == 'male' else voices[1].id)

    def play_response(self, response):
        """Play the bot's response using text-to-speech"""
        try:
            def speak():
                try:
                    self.engine.say(response)
                    self.engine.runAndWait()
                except RuntimeError:
                    # Ignore runtime errors from pyttsx3
                    pass
                except Exception as e:
                    logging.error(f"Error in text-to-speech: {str(e)}")
            
            # Run text-to-speech in a separate thread
            threading.Thread(target=speak, daemon=True).start()
        except Exception as e:
            logging.error(f"Error starting text-to-speech thread: {str(e)}")

    def change_font(self, font):
        """Change the font of the chat interface"""
        self.font = font
        self.text_box.config(font=font)

    def theme_default(self):
        """Set default color theme"""
        self.master.config(bg="#FFFFFF")
        self.text_box.config(bg="#FFFFFF", fg="#000000")

    def theme_dark(self):
        """Set dark color theme"""
        self.master.config(bg="#2C2F33")
        self.text_box.config(bg="#2C2F33", fg="#FFFFFF")

    def theme_grey(self):
        """Set grey color theme"""
        self.master.config(bg="#808080")
        self.text_box.config(bg="#808080", fg="#FFFFFF")

    def theme_blue(self):
        """Set blue color theme"""
        self.master.config(bg="#0000FF")
        self.text_box.config(bg="#0000FF", fg="#FFFFFF")

    def theme_hacker(self):
        """Set hacker color theme"""
        self.master.config(bg="#0F0F0F")
        self.text_box.config(bg="#0F0F0F", fg="#00FF00")

    def show_about(self):
        """Show information about Sanjeevini Bot"""
        about_text = """Sanjeevini Bot - Your Medical Assistant

This AI-powered medical chat bot helps you:
• Diagnose common medical conditions
• Get medicine recommendations
• Find appropriate doctors
• Learn about precautions and treatments

Note: This bot provides general medical information and 
should not be used as a replacement for professional 
medical advice."""

        messagebox.showinfo("About Sanjeevini Bot", about_text)

    def show_developers(self):
        """Show information about the developers"""
        dev_text = """Developers:

• Azeem Sheikh
• Chinmay Hegde
• Aman Khan
• Harshith Doijode

 2024 Sanjeevini Bot Team"""

        messagebox.showinfo("Developers", dev_text)

    def last_sent_label(self, date):
        """Update the last sent message label"""
        try:
            self.sent_label.destroy()
        except AttributeError:
            pass

        self.sent_label = Label(self.status_frame, font="Verdana 7", text=date, fg="#666666")
        self.sent_label.pack(side=LEFT, padx=5, pady=(0, 5))

    def get_bot_response(self, user_input):
        """Get response from bot"""
        try:
            logging.info(f"Processing user input: {user_input}")
            response = self.bot.chat(user_input)
            logging.info(f"Bot response: {response}")
            return response
        except Exception as e:
            logging.error(f"Error in get_bot_response: {str(e)}")
            return "I apologize, but I'm having trouble processing your request. Please try again."

    def send_message(self, event=None):
        """Send message to bot and display response"""
        try:
            # Get user input
            user_input = self.text_input.get("1.0", tk.END).strip()
            if not user_input:
                return
            
            logging.info(f"Sending message: {user_input}")
            
            # Clear input box
            self.text_input.delete("1.0", tk.END)
            
            # Display user message
            self.text_box.config(state=NORMAL)
            self.text_box.insert(END, "\n\n")
            self.text_box.image_create(END, image=self.human_photo)
            self.text_box.insert(END, " : ", "human")
            self.text_box.insert(END, user_input)
            self.text_box.config(state=DISABLED)
            self.text_box.see(END)

            # Get bot response
            bot_response = self.get_bot_response(user_input)
            logging.info(f"Got bot response: {bot_response}")
            
            # Display bot response
            if bot_response:
                self.text_box.config(state=NORMAL)
                self.text_box.insert(END, "\n\n")
                self.text_box.image_create(END, image=self.bot_photo)
                self.text_box.insert(END, " : ", "bot")
                self.text_box.insert(END, bot_response)
                self.text_box.config(state=DISABLED)
                self.text_box.see(END)
                # Play the response using text-to-speech
                self.play_response(bot_response)
            else:
                self.text_box.config(state=NORMAL)
                self.text_box.insert(END, "\n\n")
                self.text_box.image_create(END, image=self.bot_photo)
                self.text_box.insert(END, " : ", "bot")
                self.text_box.insert(END, "I apologize, but I couldn't process your request.")
                self.text_box.config(state=DISABLED)
                self.text_box.see(END)
                # Play the error message
                self.play_response("I apologize, but I couldn't process your request.")
                
            # Update last sent time
            from datetime import datetime
            current_time = datetime.now().strftime("%I:%M %p")
            self.last_sent_label(date=f"Last message sent at {current_time}")

        except Exception as e:
            logging.error(f"Error in send_message: {str(e)}")
            self.text_box.config(state=NORMAL)
            self.text_box.insert(END, "\n\n")
            self.text_box.image_create(END, image=self.bot_photo)
            self.text_box.insert(END, " : ", "bot")
            self.text_box.insert(END, "I apologize, but I'm having trouble processing your request.")
            self.text_box.config(state=DISABLED)
            self.text_box.see(END)

    def handle_doctors_button(self):
        """Handle the Find Doctor button click"""
        from ttkthemes import ThemedTk
        doctor_window = ThemedTk(theme="arc")
        doctor_window.title("Doctor Management")
        DoctorManagementGUI(doctor_window)
        doctor_window.focus_set()

    def handle_ai_button(self):
        """Handle the AI button click"""
        user_input = self.text_input.get("1.0", 'end-1c').strip()
        if not user_input:
            messagebox.showinfo("Input Required", "Please enter your question first!")
            return
            
        # Add 'ai.' prefix if not present
        display_input = user_input  # Store original input for display
        if not user_input.startswith("ai."):
            user_input = "ai." + user_input
            
        # Get AI response
        ai_response = self.bot.ai_generated_response(user_input)
        
        # Display the conversation in the chat
        self.text_box.config(state=NORMAL)
        self.text_box.insert(END, "\n\n")
        
        # Insert user message with icon
        self.text_box.image_create(END, image=self.human_photo)
        self.text_box.insert(END, " : ", "human")
        self.text_box.insert(END, display_input)  # Use original input without ai. prefix
        
        # Insert bot response with icon
        self.text_box.insert(END, "\n\n")
        self.text_box.image_create(END, image=self.bot_photo)
        self.text_box.insert(END, " : ", "bot")
        self.text_box.insert(END, ai_response)
        
        # Clear input field and scroll to bottom
        self.text_input.delete("1.0", END)
        self.text_box.see(END)
        self.text_box.config(state=DISABLED)

        # Play the AI response using text-to-speech
        self.play_response(ai_response)

def main():
    root = Tk()
    root.title("Sanjeevini Bot")
    root.geometry("500x600")
    app = ChatInterface(root)
    
  
    root.mainloop()

if __name__ == "__main__":
    main()
