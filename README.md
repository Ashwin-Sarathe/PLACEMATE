# PLACEMATE 👨‍🎓

Welcome to the PLACEMATE! This web application helps final-year students predict their placement outcomes, build professional resumes, and report any issues they encounter. The tool uses machine learning to provide accurate predictions and offers a user-friendly interface for a seamless experience.


# Link

https://placemate.streamlit.app/


## Features 📱

### 1. User Authentication
- **Create Account:** New users can sign up using their email and password.
- **Login:** Existing users can log in to access the application's features.
- **Firebase Integration:** User authentication is managed securely using Google Firebase.

### 2. Placement Prediction
- **Input Data:** Users can enter their age, number of internships, CGPA, gender, stream, and history of backlogs.
- **Random Forest Model:** The application uses a Random Forest classifier to predict whether the user will be placed or not.
- **Result Display:** The prediction result is displayed as either "Placed" or "Not Placed."

### 3. Resume Builder
- **Personal Information:** Users can enter their name, address, email, phone number, and upload a profile picture.
- **Career Objectives & Strengths:** Users can add their career objectives and strengths.
- **Education & Projects:** Users can input their educational qualifications and project details.
- **PDF Generation:** The application generates a professional resume in PDF format using the FPDF library.

### 4. Bug Report Feature
- **Report Issues:** Users can report bugs or issues they encounter, along with suggestions for improvement.
- **Add Screenshots:** Users can upload screenshots to provide more context for their reports.
- **Local Storage:** Bug reports are saved locally in a JSON file, and screenshots are stored in a designated directory.

## Tools Used 🛠️

- **Streamlit:** For building the web application interface.
- **Python:** The primary programming language used for backend logic.
- **Random Forest (Scikit-learn):** Machine learning model for placement prediction.
- **Google Firebase:** For user authentication and data management.
- **PIL (Python Imaging Library):** For processing profile pictures in the resume builder.
- **FPDF:** For generating PDF resumes.
- **JSON:** For storing bug reports locally.
- **Google Colab:** For developing and training the machine learning model.

## Important Points 🌟

1. For adding "Login" Module in this project, just move both the files out of the "Login" folder. Then add the "login.py" code in "app.py". Also add the "Login" tab in "streamlit_option_menu" in "app.py". You don't need to update anything in "auth_functions.py" file.
1. Then download your key (.json file) for your project from the Firebase interface. Add it's path in "app.py" file in "Login" module code.
2. In "secrets.toml" file, add your "Firebase Web API Key". You will get it from your project's Firebase interface.
3. Download all the necessary packages from the "requirements.txt" file.
4. For opening the project, open CMD in the project folder and write "streamlit run app.py". The app will open in your browser on localhost.

## HAPPY CODING!! 🧑‍💻



