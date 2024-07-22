import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
import auth_functions

# ========= ACCOUNT TAB =========
cred = credentials.Certificate('<--PATH OF YOUR FIREBASE KEY-->')

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
