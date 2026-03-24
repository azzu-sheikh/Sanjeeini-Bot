import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import pandas as pd
from ttkthemes import ThemedTk
import os

class DoctorManagementGUI:
    def __init__(self, parent):
        self.root = parent
        self.root.title("Doctor Directory - Sanjeevini Bot")
        self.root.geometry("1000x600")
        
        # Configure grid weights
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=3)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Create main frames
        self.create_sidebar()
        self.create_main_content()
        
        # Load doctor data
        self.load_doctors()

    def create_sidebar(self):
        # Sidebar frame
        sidebar = ttk.Frame(self.root, padding="10")
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_columnconfigure(0, weight=1)
        
        # Search section
        ttk.Label(sidebar, text="Search Doctors", font=('Helvetica', 12, 'bold')).grid(row=0, column=0, pady=(0,10))
        
        # Search type
        self.search_type = tk.StringVar(value="name")
        search_types = [
            ("By Name", "name"),
            ("By Specialization", "specialization"),
            ("By Location", "location")
        ]
        
        for i, (text, value) in enumerate(search_types):
            ttk.Radiobutton(sidebar, text=text, value=value, variable=self.search_type).grid(
                row=i+1, column=0, sticky="w", pady=2
            )
        
        # Search entry
        self.search_entry = ttk.Entry(sidebar)
        self.search_entry.grid(row=4, column=0, sticky="ew", pady=(10,5))
        
        # Search button
        ttk.Button(sidebar, text="Search", command=self.search_doctors).grid(
            row=5, column=0, sticky="ew", pady=5
        )
        
        # Load doctors button
        ttk.Button(sidebar, text="Load All Doctors", command=self.load_doctors).grid(
            row=6, column=0, sticky="ew", pady=5
        )
        
        # Stats section
        ttk.Separator(sidebar).grid(row=7, column=0, sticky="ew", pady=20)
        ttk.Label(sidebar, text="Statistics", font=('Helvetica', 12, 'bold')).grid(row=8, column=0, pady=(0,10))
        
        self.stats_text = tk.StringVar()
        ttk.Label(sidebar, textvariable=self.stats_text, wraplength=200).grid(row=9, column=0, sticky="w")

    def create_main_content(self):
        # Main content frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=1, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        
        # Title
        title_frame = ttk.Frame(main_frame)
        title_frame.grid(row=0, column=0, sticky="ew", pady=(0,10))
        ttk.Label(title_frame, text="Doctor Directory", font=('Helvetica', 14, 'bold')).pack(side="left")
        
        # Create Treeview
        self.tree = ttk.Treeview(main_frame, columns=("DoctorID", "Name", "Specialization", "Education", "Location", "Available_Hours", "Rating"), show="headings")
        
        # Configure columns
        self.tree.heading("DoctorID", text="ID", command=lambda: self.sort_treeview("DoctorID"))
        self.tree.heading("Name", text="Name", command=lambda: self.sort_treeview("Name"))
        self.tree.heading("Specialization", text="Specialization", command=lambda: self.sort_treeview("Specialization"))
        self.tree.heading("Education", text="Education", command=lambda: self.sort_treeview("Education"))
        self.tree.heading("Location", text="Location", command=lambda: self.sort_treeview("Location"))
        self.tree.heading("Available_Hours", text="Hours", command=lambda: self.sort_treeview("Available_Hours"))
        self.tree.heading("Rating", text="Rating", command=lambda: self.sort_treeview("Rating"))
        
        # Column widths
        self.tree.column("DoctorID", width=50)
        self.tree.column("Name", width=150)
        self.tree.column("Specialization", width=150)
        self.tree.column("Education", width=200)
        self.tree.column("Location", width=200)
        self.tree.column("Available_Hours", width=100)
        self.tree.column("Rating", width=50)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Grid treeview and scrollbar
        self.tree.grid(row=1, column=0, sticky="nsew")
        scrollbar.grid(row=1, column=1, sticky="ns")
        
        # Bind double-click event
        self.tree.bind("<Double-1>", self.show_doctor_details)

    def load_doctors(self):
        try:
            # Clear existing items
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Load doctor data from the correct path
            script_dir = os.path.dirname(os.path.abspath(__file__))
            df = pd.read_csv(os.path.join(script_dir, "doctors_database.csv"))
            
            # Update stats
            total_doctors = len(df)
            specializations = df['Specialization'].nunique()
            locations = df['Location'].nunique()
            self.stats_text.set(f"Total Doctors: {total_doctors}\nSpecializations: {specializations}\nLocations: {locations}")
            
            # Add to treeview
            for _, row in df.iterrows():
                self.tree.insert("", "end", values=(
                    row['DoctorID'],
                    row['Name'],
                    row['Specialization'],
                    row['Education'],
                    row['Location'],
                    row['Available_Hours'],
                    row['Rating']
                ))
                
        except Exception as e:
            messagebox.showerror("Error", f"Error loading doctors: {str(e)}")

    def search_doctors(self):
        search_text = self.search_entry.get().strip().lower()
        search_by = self.search_type.get()
        
        if not search_text:
            self.load_doctors()
            return
        
        try:
            # Clear existing items
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Load and filter data from the correct path
            script_dir = os.path.dirname(os.path.abspath(__file__))
            df = pd.read_csv(os.path.join(script_dir, "doctors_database.csv"))
            
            # Convert relevant columns to string and handle NaN values
            df['Name'] = df['Name'].astype(str)
            df['Specialization'] = df['Specialization'].astype(str)
            df['Location'] = df['Location'].astype(str)
            
            if search_by == "name":
                df = df[df['Name'].str.lower().str.contains(search_text, na=False)]
            elif search_by == "specialization":
                df = df[df['Specialization'].str.lower().str.contains(search_text, na=False)]
            elif search_by == "location":
                df = df[df['Location'].str.lower().str.contains(search_text, na=False)]
            
            # Update stats
            total_doctors = len(df)
            specializations = df['Specialization'].nunique()
            locations = df['Location'].nunique()
            self.stats_text.set(f"Search Results:\nDoctors Found: {total_doctors}\nSpecializations: {specializations}\nLocations: {locations}")
            
            # Add filtered results to treeview
            for _, row in df.iterrows():
                self.tree.insert("", "end", values=(
                    row['DoctorID'],
                    row['Name'],
                    row['Specialization'],
                    row['Education'],
                    row['Location'],
                    row['Available_Hours'],
                    row['Rating']
                ))
            
            if total_doctors == 0:
                messagebox.showinfo("Search Results", "No doctors found matching your search criteria.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error searching doctors: {str(e)}")

    def show_doctor_details(self, event):
        try:
            item = self.tree.selection()[0]
            doctor = self.tree.item(item)["values"]
            
            # Create details window
            details_window = tk.Toplevel(self.root)
            details_window.title(f"{doctor[1]} - Details")
            details_window.geometry("600x400")
            
            # Add details
            ttk.Label(details_window, text=doctor[1], font=('Helvetica', 14, 'bold')).pack(pady=10)
            ttk.Label(details_window, text=f"Doctor ID: {doctor[0]}").pack(pady=5)
            ttk.Label(details_window, text=f"Specialization: {doctor[2]}").pack(pady=5)
            ttk.Label(details_window, text=f"Education: {doctor[3]}").pack(pady=5)
            ttk.Label(details_window, text=f"Location: {doctor[4]}").pack(pady=5)
            ttk.Label(details_window, text=f"Available Hours: {doctor[5]}").pack(pady=5)
            ttk.Label(details_window, text=f"Rating: {doctor[6]}/5").pack(pady=5)
            
            # Add close button
            ttk.Button(details_window, text="Close", command=details_window.destroy).pack(pady=20)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error showing doctor details: {str(e)}")

    def sort_treeview(self, col):
        """Sort treeview when column header is clicked"""
        l = [(self.tree.set(k, col), k) for k in self.tree.get_children('')]
        l.sort()
        
        # Rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            self.tree.move(k, '', index)

    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    root = ThemedTk(theme="arc")  # Modern theme
    app = DoctorManagementGUI(root)
    app.run()
