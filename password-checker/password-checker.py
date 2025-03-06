import streamlit as st
import random
import string

def generate_password(length, use_digits, use_special):
    characters = string.ascii_letters

    if use_digits:
        characters += string.digits

    if use_special:
        characters += (string.punctuation)

    return "".join(random.choice(characters) for _ in range(length))

st.title("Password Generator")

length = st.slider("length of password", min_value=4, max_value=30, value=12)

use_digits = st.checkbox("use digits")

use_special = st.checkbox("use special characters")

if st.button("Generate Password"):
    password = generate_password(length, use_digits, use_special)
    st.write(f"Generated Password `{password}`")

st.write("Made with ❤️ by [Muhammad Huzaifa]")
st.write("Check out my [GitHub](http://github.com/HezziCode/) for more projects.")