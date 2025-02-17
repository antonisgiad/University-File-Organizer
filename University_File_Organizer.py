import os
import shutil
import time
import tkinter as tk
from tkinter import filedialog

# Get the current user's name dynamically
USER_NAME = os.getlogin()

# Define the desktop and downloads paths dynamically
DESKTOP_PATH = f"C:\\Users\\{USER_NAME}\\OneDrive\\Desktop\\University"
DOWNLOADS_PATH = f"C:\\Users\\{USER_NAME}\\Downloads"

# Function to create folder structure
def create_folders():
    print("Creating university folder structure...")
    years = input("Enter the years (comma-separated, e.g. '1st Year, 2nd Year'): ").split(",")
    semesters = input("Enter the semesters (comma-separated, e.g. 'Fall, Spring'): ").split(",")
    subjects = input("Enter the subjects (comma-separated, e.g. 'Math, Physics'): ").split(",")
    
    subfolders = ["Lectures", "Exercises", "Labs", "Exams"]

    for year in map(str.strip, years):
        year_path = os.path.join(DESKTOP_PATH, year)
        os.makedirs(year_path, exist_ok=True)
        print(f"Created folder for {year} at: {year_path}")

        for semester in map(str.strip, semesters):
            semester_path = os.path.join(year_path, semester)
            os.makedirs(semester_path, exist_ok=True)
            print(f"Created folder for {semester} in {year} at: {semester_path}")

            for subject in map(str.strip, subjects):
                subject_path = os.path.join(semester_path, subject)
                os.makedirs(subject_path, exist_ok=True)
                print(f"Created folder for {subject} in {semester} at: {subject_path}")

                for subfolder in subfolders:
                    subfolder_path = os.path.join(subject_path, subfolder)
                    os.makedirs(subfolder_path, exist_ok=True)
                    print(f"Created subfolder {subfolder} in {subject} at: {subfolder_path}")

    print("Folder structure created successfully.")

def is_file_download_complete(file_path, retries=20, wait_time=5):
    if not os.path.exists(file_path):
        print(f"❌ File {file_path} was deleted or moved.")
        return False

    if file_path.endswith('.tmp'):
        print(f"⏳ File is still in .tmp form: {file_path}")
        time.sleep(wait_time)  # Wait before checking again
        return False

    initial_creation_time = os.path.getctime(file_path)
    
    for _ in range(retries):
        if os.path.exists(file_path):
            current_creation_time = os.path.getctime(file_path)
            file_size = os.path.getsize(file_path)
            
            if current_creation_time == initial_creation_time and file_size > 0:
                print(f"✅ File download complete: {file_path}")
                return True
            else:
                print(f"⏳ File download is still in progress or being renamed: {file_path}")
                initial_creation_time = current_creation_time
        else:
            print(f"❌ File {file_path} does not exist or was deleted.")
            return False

    print(f"❌ File {file_path} did not finish downloading after {retries} attempts.")
    return False

# Function to suggest similar folder names
def suggest_similar_folder(folder_name, available_folders):
    suggestions = difflib.get_close_matches(folder_name, available_folders, n=3, cutoff=0.6)
    if suggestions:
        print(f"Did you mean one of these? {', '.join(suggestions)}")
    return suggestions

# Function to move files with retries and better error handling
def move_file(file_path):
    if not os.path.exists(file_path):  # Check if the file exists
        print(f"❌ The file '{file_path}' does not exist or has been deleted.")
        return

    file_name = os.path.basename(file_path)
    print(f"\n🔍 Sorting the file: '{file_name}'...")

    # Ensure the file is fully downloaded before processing
    if not is_file_download_complete(file_path):
        print(f"⏳ File {file_name} is still downloading. Please wait...")
        return

    year = input(f"Enter the year for '{file_name}' (e.g., '1st Year', '2nd Year'): ").strip()
    while not year or not os.path.exists(os.path.join(DESKTOP_PATH, year)):
        print("❌ Year does not exist. Please enter a valid year.")
        year = input(f"Enter the year for '{file_name}' (e.g., '1st Year', '2nd Year'): ").strip()

    semester = input(f"Enter the semester for '{file_name}' (e.g., 'Fall', 'Spring'): ").strip()
    while not semester or not os.path.exists(os.path.join(DESKTOP_PATH, year, semester)):
        print("❌ Semester does not exist. Please enter a valid semester.")
        semester = input(f"Enter the semester for '{file_name}' (e.g., 'Fall', 'Spring'): ").strip()

    subject = input(f"Enter the subject for '{file_name}' (e.g., 'Math', 'Physics'): ").strip()
    while not subject or not os.path.exists(os.path.join(DESKTOP_PATH, year, semester, subject)):
        print("❌ Subject does not exist. Please enter a valid subject.")
        subject = input(f"Enter the subject for '{file_name}' (e.g., 'Math', 'Physics'): ").strip()

    category = input("Enter the category for this file (Lectures, Exercises, Labs, Past Exams Solutions): ").strip().capitalize()
    while category not in ["Lectures", "Exercises", "Labs", "Past Exams Solutions"]:
        print("❌ Invalid category. Please enter one of the following: Lectures, Exercises, Labs, Past Exams Solutions.")
        category = input("Enter the category for this file (Lectures, Exercises, Labs, Past Exams Solutions): ").strip().capitalize()

    destination = os.path.join(DESKTOP_PATH, year, semester, subject, category)

    if not os.path.exists(destination):
        print(f"❌ The folder {destination} doesn't exist yet.")
        available_folders = [d for d in os.listdir(os.path.join(DESKTOP_PATH, year, semester, subject)) if os.path.isdir(os.path.join(DESKTOP_PATH, year, semester, subject, d))]
        suggestions = suggest_similar_folder(category, available_folders)
        
        if suggestions:
            category = input(f"Enter the corrected category for this file (e.g., '{suggestions[0]}'): ").strip().capitalize()
            destination = os.path.join(DESKTOP_PATH, year, semester, subject, category)
        
        if not os.path.exists(destination):
            print(f"❌ The folder {destination} still doesn't exist. Creating it now...")
            os.makedirs(destination, exist_ok=True)

    try:
        shutil.move(file_path, destination)
        print(f"✅ Successfully moved '{file_name}' to {destination}.")
    except Exception as e:
        print(f"❌ Error moving the file: {e}")
        print("⏳ Retrying...")  
        time.sleep(2)
        move_file(file_path)

# Function to get file path via a file dialog
def select_file():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(title="Select a file to move")
    return file_path

# Main program
def main():
    while True:
        print("\nChoose an action:")
        print("1: Create folder structure")
        print("2: Move a downloaded file")
        print("3: Quit")

        choice = input("Enter your choice (1/2/3): ").strip()

        if choice == "1":
            create_folders()
        elif choice == "2":
            # Get the file path using a file dialog instead of typing
            file_path = select_file()
            if file_path:
                move_file(file_path)
        elif choice == "3":
            print("👋 Thank you for using the program! Have a great day!")
            time.sleep(2)  # Pausing for 2 seconds before exit to make it smoother
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Run the program
if __name__ == "__main__":
    main() 