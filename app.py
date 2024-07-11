import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import pickle
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
import auth_functions
from fpdf import FPDF
from PIL import Image
import json
import os

hide_st_style = """
                <style>
                #MainMenu {visibility : hidden;}
                footer {visibility : hidden;}
                header {visibility : hidden;}
                </style>
                """

# default data
dataframe = pd.read_csv("Datasets/collegePlacementData.csv")

st.set_page_config(
    page_title="PLACEMATE",
    page_icon="memo",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items=None
)

#remove all the default streamlit configs here
st.markdown(hide_st_style, unsafe_allow_html=True)

with st.sidebar:
    selected = option_menu(
        menu_title = "PLACEMATE",
        options = ["Home", "Login/Register", "Predictions", "Resume Builder", "Bug Report", "Buy Me A Coffee" ,"About Me"],
        icons = ["house", "person-add", "magic", "file-earmark-text", "bug", "cup-hot" ,"person-circle"],
        menu_icon= "robot",
        default_index = 0,
    )

# ========= HOME TAB =========
if selected == "Home":
    col1, col2 = st.columns([2, 1])
    with col1:
        st.title('PLACEMATE :rocket:')
        st.subheader("Resume Ready 📄,")
        st.subheader("Placement Predicted: 🔮")
        st.subheader("Be Job Ready! 👍")
        st.divider()
        st.header("About :memo:")
        st.markdown('''
        #####
        <span style='font-size: 18px;'>
        We are thrilled to introduce you to PLACEMATE, the all-in-one solution for student's
        management and recruitment needs
        providing a comprehensive platform for predicting placement possibility, 
        evaluating academic progress and 
        facilitating career development.
        With PLACEMATE, students can efficiently use their data to
        track their academic performance, and kick-start their placement preparation.                               
        Join us on this exciting journey as we aim revolutionize
        student management and recruitment with PLACEMATE!
        </span>
        ''', unsafe_allow_html=True)
        st.text("")
        st.markdown("#### <span style='font-size: 24px;'> `Create Your Account & Begin Your Placment Journey Now!`</span>", unsafe_allow_html=True)

    with col2:
        st.image("Images/home_tab_pic.png")

# ========= ACCOUNT TAB =========
if selected == "Login/Register":
        cred = credentials.Certificate('launchpred-firebase-adminsdk-l3b9o-c5cdb1c41b.json')

        #firebase_admin.initialize_app(cred)
        st.title("Login/Register Form 👨‍🎓")
        
        if 'user_info' not in st.session_state:
            st.header("Please Login/Register by filling in your details ✏️")
            st.divider()
            col1,col2,col3 = st.columns([1,2,1])

            # Authentication form layout
            do_you_have_an_account = col2.selectbox(label='Choose an Option:',options=('Login','Register','Forgot Password!'))
            auth_form = col2.form(key='Authentication form',clear_on_submit=False)
            email = auth_form.text_input(label='Email')
            password = auth_form.text_input(label='Password',type='password') if do_you_have_an_account in {'Login','Register'} else auth_form.empty()
            username = auth_form.text_input(label='Username') if do_you_have_an_account in {'Register'} else auth_form.empty()
            auth_notification = col2.empty()

            # Sign In
            if do_you_have_an_account == 'Login' and auth_form.form_submit_button(label='Sign In',use_container_width=True,type='primary'):
                with auth_notification, st.spinner('Signing in...'):
                    auth_functions.sign_in(email,password)

            # Create Account
            elif do_you_have_an_account == 'Register' and auth_form.form_submit_button(label='Create Account',use_container_width=True,type='primary'):
                with auth_notification, st.spinner('Creating account...'):
                    auth_functions.create_account(email,password,username)

            # Password Reset
            elif do_you_have_an_account == 'Forgot Password!' and auth_form.form_submit_button(label='Send Password Reset Email',use_container_width=True,type='primary'):
                with auth_notification, st.spinner('Sending password reset link'):
                    auth_functions.reset_password(email)

            # Authentication success and warning messages
            if 'auth_success' in st.session_state:
                auth_notification.success(st.session_state.auth_success)
                del st.session_state.auth_success
            elif 'auth_warning' in st.session_state:
                auth_notification.warning(st.session_state.auth_warning)
                del st.session_state.auth_warning

        ## -------------------------------------------------------------------------------------------------
        ## Logged in --------------------------------------------------------------------------------------
        ## -------------------------------------------------------------------------------------------------
        else:
            # Sign out
            st.header('Sign out: 🙋‍♂️')
            st.button(label='Sign Out',on_click=auth_functions.sign_out,type='primary')

            # Delete Account
            st.header('Delete account: 🥹')
            password = st.text_input(label='Confirm your password',type='password')
            st.button(label='Delete Account',on_click=auth_functions.delete_account,args=[password],type='primary')

# ========= PREDICTION TAB =======
if selected == "Predictions":
    if 'user_info' not in st.session_state:
        st.warning('Please Login with your Email-ID and Password to Know your Placement Status!  ', icon='⚠️')
    else:
        col1, col2 = st.columns([2, 1])
        with col1:
            st.title("Placement Prediction ⚡")
            st.subheader("Provide the inputs below 👇🏻")
            st.divider()
            st.markdown("##### _Here we have used <span style='color:yellow'>Random Forest 🤖</span> Machine Learning Algorithm to create our Model to predict the Placement of Students_.", unsafe_allow_html=True)
            st.markdown("##### _You just need to provide your data to get started and predict your placement probability using our <span style = 'color:yellow'>well trained Model right here</span>_.", unsafe_allow_html=True)
        with col2:
            st.image("Images/prediction_tab_pic.png")

        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            # Get user input for Age
            age = st.slider('Enter the Age 👇🏻', min_value=18, max_value=27, step=1)
            # Get user input for Internships
            internships = st.slider('Enter Number of Internships 👇🏻', min_value=0, max_value=10, step=1)
            # Get user input for CGPA
            cgpa = st.slider('Enter the CGPA 👇🏻', min_value=0.0, max_value=10.0, step=0.1)
            predict_button = st.button("Predict the Placement ⚡")

        with col2:
            # Get user input for Gender
            gender = st.selectbox('Choose Gender 🧑🏻‍🦱👧🏻', ['Male', 'Female'])
            # Get user input for Stream
            stream = st.selectbox('Choose Stream 🎓', ['Electronics And Communication', 'Computer Science', 'Information Technology', 'Mechanical', 'Electrical', 'Civil'])
            # Get user input for Hostel
            hostel = 'No'
            # Get user input for History of Backlogs
            backlogs = st.selectbox("History of Backlogs 👇🏻", ['Yes', "No"])
        
        # encoding the variables here.

        #gender
        if gender == 'Male': gender_encoded = 1
        else: gender_encoded = 0

        # stream
        if stream == 'Electronics And Communication': stream_encoded = 1
        elif stream == 'Computer Science': stream_encoded = 2
        elif stream == 'Information Technology': stream_encoded = 3
        elif stream == 'Mechanical': stream_encoded = 4
        elif stream == 'Electrical': stream_encoded = 5
        elif stream == 'Civil': stream_encoded = 6
        else: 'Invalid Stream Selected'

        # Hostel
        hostel_encoded = 1 if hostel == 'Yes' else 0

        # backlog history
        backlogs_encoded = 1 if backlogs == 'Yes' else 0

        # Check if the Predict Placement button is clicked
        if predict_button:

            

            # Prepare the user input as a dataframe
            user_data = {
                'Age': [age],
                'Gender': [gender],
                'Stream': [stream],
                'Internships': [internships],
                'CGPA': [cgpa],
                'Hostel': [hostel],
                'HistoryOfBacklogs': [backlogs]
            }
            user_df = pd.DataFrame(user_data)
            st.divider()
            

            # Make predictions using the loaded model
            model = pickle.load(open("Models/Placement_Model", 'rb'))

            # Display the prediction result
            prediction = model.predict([[age, gender_encoded, stream_encoded, internships, cgpa, hostel_encoded, backlogs_encoded]])
            st.markdown("* ## Prediction Result ✅")
            if prediction == 1:
                st.balloons()
                st.markdown("### <span style='color:lightgreen'>Placed 🎉</span>", unsafe_allow_html=True)
            else:
                st.markdown("### <span style='color:red'>Not Placed 😢</span>", unsafe_allow_html=True)


        st.divider()

        st.markdown("## Prediction using <span style='color:yellow'>_Random Forest Classifier_ 🦾</span>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("* #### Best Accuracy : <span style='color:yellow'>_89.63%_ 🦾</span>", unsafe_allow_html=True)
            st.markdown("* #### Precision Score : <span style='color:yellow'>_94.08%_ ⚡</span>", unsafe_allow_html=True)

        with col2:
            st.markdown("* #### F1 Score : <span style='color:yellow'>_90.54%_ 🦾</span>", unsafe_allow_html=True)
            st.markdown("* #### Recall Score : <span style='color:yellow'>_87.27%_ ⚡</span>", unsafe_allow_html=True)

# ========= RESUME BUILDER TAB =========
if selected == "Resume Builder":
    # Function to generate the resume in PDF format
    if 'user_info' not in st.session_state:
        st.warning('Please Login with your Email-ID and Password to Get your Resume!  ', icon='⚠️')
    else:
        class PDF(FPDF):
            def __init__(self, profile_picture):
                super().__init__()
                self.profile_picture = profile_picture
                self.set_auto_page_break(auto=False, margin=15)
            
            def header(self):
                if self.profile_picture:
                    self.image(self.profile_picture, 150, 23, 50)
                self.set_font('Times', 'BU', 16)
                self.cell(0, 10, 'CURRICULUM VITAE', 0, 1, 'C')
                self.ln(10)
            
            def footer(self):
                self.set_y(-15)
            
            def add_personal_info(self, name, address, email, phone):
                self.set_font('Times', 'B', 12)
                self.cell(0, 10, name, 0, 1, 'L')
                self.set_font('Times', '', 12)
                self.cell(0, 10, address, 0, 1, 'L')
                self.cell(0, 10, email, 0, 1, 'L')
                self.cell(0, 10, phone, 0, 1, 'L')
                self.ln(10)

            def add_section(self, title, body):
                self.set_font('Times', 'B', 12)
                self.cell(0, 10, title, 0, 1, 'L')
                self.set_font('Times', '', 12)
                self.multi_cell(0, 10, body)
                self.ln(5)

        def generate_pdf(name, address, email, phone, objective, education, strengths, projects, profile_picture):
            pdf = PDF(profile_picture)
            pdf.add_page()

            pdf.add_personal_info(name, address, email, phone)

            
            pdf.add_section("CAREER OBJECTIVE", objective)
            pdf.add_section("EDUCATION QUALIFICATION", education)
            pdf.add_section("STRENGTHS", strengths)
            pdf.add_section("PROJECTS", projects)

            pdf.set_font('Times', 'I', 12)
            pdf.cell(0, 10, "I declare that the above information is true to the best of my knowledge.", 0, 1)
            pdf.ln(5)
            pdf.cell(0, 10, "Date: ", 0, 1)
            pdf.cell(0, 10, "Place: ", 0, 1)

            return pdf

        # Streamlit app
        st.title("Resume Builder 📄")
        st.subheader("Note: 📝")
        st.text("* Please Write Career Objectives, Strengths, Projects in less than 50 Words!")
        st.text("* Please Mention Education Qualification in this format: ")
        st.text("* Course Name  -  College/Institution Name  -  Percentage/CGPA  -  Year")
        st.divider()
        st.header("Personal Information 🧑‍🎓")
        name = st.text_input("Full Name")
        name=name.upper()
        address = st.text_input("Address")
        email = st.text_input("Email-ID")
        phone = st.text_input("Phone Number")
        phone = "Phone No. : " + phone
        st.header("Upload Profile Picture 📷")
        profile_picture = st.file_uploader("Make sure to select .jpg/.jpeg file only", type=["jpg", "jpeg"])

        st.header("Career Objectives 🎯")
        objective = st.text_area("Please Enter Your Career Objectives Below:")

        st.header("Education Qualification 📚")
        education = st.text_area("Please Enter Your Education Details Below:")

        st.header("Strengths 💪")
        strengths = st.text_area("Please Enter Your Strengths Below:")

        st.header("Projects 🧑‍💻")
        projects = st.text_area("Please Tell About the Projects You've Built:")

        if st.button("Generate Resume 🔃"):
            if profile_picture:
                image = Image.open(profile_picture)
                image.save("ProfilePics\\profile_picture.jpg")
                profile_picture_path = "ProfilePics\\profile_picture.jpg"
            else:
                profile_picture_path = None

            resume = generate_pdf(name, address, email, phone, objective, education, strengths, projects, profile_picture_path)
            resume.output("resume.pdf")
            st.balloons()
            st.success("Resume generated successfully!")
            with open("resume.pdf", "rb") as pdf_file:
                st.download_button(label="Download Resume as PDF 📩", data=pdf_file, file_name="resume.pdf", mime="application/pdf")


# ========= BUG REPORT TAB =========
if selected == "Bug Report":
    col1, col2 = st.columns([2, 2])
    with col1:
        # Function to load existing data from the file
        def load_data(filename):
            if os.path.exists(filename):
                with open(filename, 'r') as f:
                    return json.load(f)
            return []

        # Function to save data to a file
        def save_data(data, filename):
            with open(filename, 'w') as f:
                json.dump(data, f, indent=4)

        st.title("Bug Report 🪲")
        st.text("NOTE:")
        st.text("You can also give some suggestions to improve our software!")
        bug_report = st.text_area("Please describe the issue or report a bug:")
        
        uploaded_file = st.file_uploader("Attach Screenshot (Optional):", type=["png", "jpg"])

        image_path = None
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            image_path = os.path.join('bug_images', f"{bug_report.replace(' ', '_')}_uploaded_file.jpg")
            os.makedirs('images', exist_ok=True)
            image.save(image_path)
            st.markdown("**<span style='color:lightgreen'>Screenshot Attached Successfully 👍🏻</span>**", unsafe_allow_html=True)
            with st.expander("Preview Attached Screenshot"):
                st.image(uploaded_file)

        send_button = st.button("Send Report ✈️")
        if send_button:
            # Collect input data
            user_data = {
                "bug_report": bug_report,
                "image_path": image_path if image_path else None
            }

            # Load existing data
            all_data = load_data('bug_data.json')

            # Ensure all_data is a list
            if not isinstance(all_data, list):
                all_data = []

            # Append new data
            all_data.append(user_data)

            # Save updated data
            save_data(all_data, 'bug_data.json')


            st.markdown("<span style = 'color:lightgreen'>Report Sent Successfully, We'll get back to you super soon ⚡</span>", unsafe_allow_html=True)
            st.markdown("## <span style = 'color:white'>Thank You 💖</span>", unsafe_allow_html=True)
            st.markdown("#### <span style = 'color:yellow'>Team HardCoders 🦾</span>", unsafe_allow_html=True)
    with col2:
        st.image("Images/AppSettings.png")


# ========= CONTRIBUTORS =========
if selected == "About Me":
    col1, col2 = st.columns(2)
    with col1:
        st.image("Images/profile-pic.png", width=350)

    with col2:
        st.title("ASHWIN SARATHE 🧑‍💻")
        st.subheader("#️⃣ KALANIKETAN POLYTECHNIC COLLEGE, JABALPUR, M.P.")
        st.subheader("#️⃣ DIPLOMA IN COMPUTER SCIENCE")
        st.subheader("#️⃣ 3RD YEAR STUDENT")
        github="https://github.com/ashwinsarathe123"
        st.markdown("### <span style = 'color:white'>#️⃣ GITHUB LINK ➡️ [CLICK HERE!!](% s)</span>" % github, unsafe_allow_html=True)
    
    st.divider()
    st.header("Special Thanks To -")
    st.header("Mrs. Rashmi Gupta Mam for Guiding us! 🙏")

# ========= BUY ME A COFFEE =========
if selected == "Buy Me A Coffee":
    url = 'https://www.buymeacoffee.com/ashwin_sarathe'
    col1, col2 = st.columns(2)
    with col1:
        st.title("Buy Me A Coffee ☕")
        st.divider()
        st.header('Please Show your Support by ')
        st.header("Buying me a Coffee!")
        st.subheader("")
        st.markdown(f'<a href="{url}" target="_blank" style="background-color: #008CBA; color: white; padding: 15px 30px; font-size: 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 4px;">Donate</a>', unsafe_allow_html=True)
    with col2:
        st.image("Images/c.png")
