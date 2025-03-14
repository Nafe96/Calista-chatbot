import streamlit as st
import requests  # For sending requests to the FastAPI server
import base64

# Define the backend API URL
API_URL = "http://127.0.0.1:8000/chat/"


st.set_page_config(page_title="Calisnova", page_icon="💬", layout="wide")

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()





 #Custom CSS Styling
st.markdown(
    """
    <style>
    /* Set background color */
    body {
        background-color: #F8F9FA;
    }
    
    /* Title Styling */
    .title {
        font-size: 32px;
        font-weight: bold;
        color: #2E76C1 !important; /* Blue from logo */
        text-align: center;
        margin-bottom: 20px;
    }



    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #D9E4F5; /* Light Blue */
        padding: 10px;
    }
    /* Chat input field */
    input {
        background-color: #29A1E5 !important;
        border-radius: 10px !important;
    }

    /* Chat bubble styling */
    .stChatMessage {
        background-color: #D9E4F5 !important; /* Green from logo */
        color: white !important;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)



# Function to handle chatbot responses by sending a request to the FastAPI backend
def chatbot_response(user_input):
    try:
        # Send a POST request to the backend with the user's input
        response = requests.post(API_URL, json={"user_input": user_input})
        response_data = response.json()  # Parse the response JSON
        return response_data.get("response", "Sorry, something went wrong.")
    except Exception as e:
        return f"Error connecting to the chatbot: {e}"

# UI Enhancements


  
logo_path = "loogo.png"


# Sidebar Info
with st.sidebar:
    st.markdown(
        f"""
        <div style="display: flex; justify-content: center; align-items: center; margin-bottom: 10px;">
            <img src="data:image/png;base64,{st.image(logo_path, output_format="PNG")}" width="0">
        </div>
        """,
        unsafe_allow_html=True 
    )                                            
    st.title("     Calista - Calisnova AI")
    st.write("A chatbot designed to assist with inquiries about Calisnova.")
    st.markdown("----")
    st.write("**Developed by Calisnova**")                                                  
    st.write("📍**Location:** Ramdeobaba University,gittikhadan,Nagpur 440013")
    st.markdown("🌐 Website: [calisnova1.odoo.com](https://calisnova1.odoo.com)")

   


# Main Chat Section
st.markdown('<p class="title">Chat with Calista</p>', unsafe_allow_html=True)

# Initialize chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Display previous chat messages
for message in st.session_state.history:
    with st.chat_message("user" if message["role"] == "user" else "assistant"):
        st.markdown(message["text"])

# Chat Input
user_input = st.chat_input("Type your message here...")




if user_input:
    # Store user input
    st.session_state.history.append({"role": "user", "text": user_input})
    
    # Get chatbot response
    response = chatbot_response(user_input)
    
    # Store chatbot response
    st.session_state.history.append({"role": "assistant", "text": response})

    # Re-render chat messages
    st.rerun()
