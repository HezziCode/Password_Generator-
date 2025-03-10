import streamlit as st
import random
import string

# Set page configuration
st.set_page_config(
    page_title="Password Generator & Checker",
    page_icon="🔒",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: 4rem;
        white-space: pre-wrap;
        border-radius: 4px 4px 0px 0px;
        padding: 1rem 1rem;
        font-size: 1rem;
    }
    .password-display {
        padding: 1rem;
        background-color: #e0e0e0;
        color: #000000;
        border-radius: 0.5rem;
        font-family: monospace;
        font-size: 1.2rem;
        margin: 1rem 0;
    }
    .header-container {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    .strength-meter {
        height: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Title with icon
st.markdown('<div class="header-container"><h1>🔒 Password Generator & Strength Checker</h1></div>', unsafe_allow_html=True)
st.markdown("Create strong passwords and check the strength of existing ones")

# Create tabs for generator and checker
tab1, tab2 = st.tabs(["Password Generator", "Password Strength Checker"])

# Password generation function
def generate_password(length, use_lowercase, use_uppercase, use_digits, use_special):
    characters = ""
    if use_lowercase:
        characters += string.ascii_lowercase
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_digits:
        characters += string.digits
    if use_special:
        characters += string.punctuation
    
    if not characters:
        return "Please select at least one character type"
    
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

# Password strength evaluation function
def check_password_strength(password):
    score = 0
    feedback = []
    
    # Check length
    if len(password) >= 12:
        score += 25
    elif len(password) >= 8:
        score += 15
    elif len(password) >= 6:
        score += 10
    else:
        feedback.append("Password is too short")
    
    # Check for character types
    if any(c.islower() for c in password):
        score += 15
    else:
        feedback.append("Add lowercase letters")
    
    if any(c.isupper() for c in password):
        score += 15
    else:
        feedback.append("Add uppercase letters")
    
    if any(c.isdigit() for c in password):
        score += 15
    else:
        feedback.append("Add numbers")
    
    if any(c in string.punctuation for c in password):
        score += 15
    else:
        feedback.append("Add special characters")
    
    # Check for common patterns
    if password.lower() in ["password", "123456", "qwerty"]:
        score = 0
        feedback.append("Avoid common passwords")
    
    # Determine strength category
    if score >= 80:
        strength = "Strong"
        color = "#28a745"  # Green
    elif score >= 50:
        strength = "Moderate"
        color = "#ffc107"  # Yellow
    else:
        strength = "Weak"
        color = "#dc3545"  # Red
    
    return {
        "score": score,
        "strength": strength,
        "color": color,
        "feedback": feedback
    }

# Password Generator Tab
with tab1:
    st.subheader("Generate a Secure Password")
    
    col1, col2 = st.columns(2)
    
    with col1:
        length = st.slider("Password Length", min_value=4, max_value=30, value=12)
    
    with col2:
        st.write("Character Types")
        use_lowercase = st.checkbox("Include Lowercase Letters", value=True)
        use_uppercase = st.checkbox("Include Uppercase Letters", value=True)
        use_digits = st.checkbox("Include Numbers", value=True)
        use_special = st.checkbox("Include Special Characters", value=True)
    
    if st.button("Generate Password", key="generate_btn"):
        password = generate_password(length, use_lowercase, use_uppercase, use_digits, use_special)
        st.session_state.generated_password = password
    
    # Display generated password
    if "generated_password" in st.session_state:
        password = st.session_state.generated_password
        
        # Check strength of generated password
        result = check_password_strength(password)
        
        st.markdown("### Generated Password:")
        st.markdown(f'<div class="password-display">{password}</div>', unsafe_allow_html=True)
        
        # Display strength meter
        st.markdown(f"### Password Strength: {result['strength']}")
        st.markdown(f'<div class="strength-meter" style="width: {result["score"]}%; background-color: {result["color"]};"></div>', unsafe_allow_html=True)
        
        # Display feedback
        if result["feedback"]:
            st.markdown("### Suggestions to improve:")
            for tip in result["feedback"]:
                st.markdown(f"- {tip}")
        
        # Copy button (using Streamlit's built-in clipboard functionality)
        st.code(password, language="text")
        st.write("Click the copy button in the top-right corner of the code block above to copy the password.")

# Password Strength Checker Tab
with tab2:
    st.subheader("Check Your Password Strength")
    
    # Password input with toggle visibility
    show_password = st.checkbox("Show password", value=False, key="show_checker")
    if show_password:
        user_password = st.text_input("Enter a password to check", key="password_input")
    else:
        user_password = st.text_input("Enter a password to check", type="password", key="password_input_hidden")
    
    # Real-time strength checking
    if user_password:
        result = check_password_strength(user_password)
        
        # Display strength result
        st.markdown(f"### Password Strength: {result['strength']}")
        st.markdown(f'<div class="strength-meter" style="width: {result["score"]}%; background-color: {result["color"]};"></div>', unsafe_allow_html=True)
        
        # Display score
        st.markdown(f"Score: {result['score']}/100")
        
        # Display detailed feedback
        if result["feedback"]:
            st.markdown("### How to improve your password:")
            for tip in result["feedback"]:
                st.markdown(f"- {tip}")
        else:
            st.success("Great job! Your password meets all security criteria.")
        
        # Password security tips
        with st.expander("Password Security Tips"):
            st.markdown("""
            ### Tips for creating strong passwords:
            - Use at least 12 characters
            - Mix uppercase and lowercase letters
            - Include numbers and special characters
            - Avoid using personal information
            - Don't use common words or patterns
            - Use different passwords for different accounts
            - Consider using a password manager
            """)

# Footer
st.markdown("---")
st.markdown("Built with ❤️ by Muhammad Huzaifa")
st.markdown("Check out my [GitHub](http://github.com/HezziCode/) for more projects.")
