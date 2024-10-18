import streamlit as st
import base64
import uuid
from rag import rag  # Assuming rag is your custom function

# Function to encode the local image file as base64
def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return encoded_string

# Set the page configuration
st.set_page_config(page_title="Primal Health Bot", layout="wide")

# Load the image and encode it in base64
image_path = "./static/images/healthy_food.jpg"  # replace with your local image path
base64_image = get_base64_image(image_path)

# Custom CSS to style the background and input box with the encoded image
st.markdown(
    f"""
    <style>
    /* Full-page background using base64-encoded image */
    .stApp {{
        background-image: url("data:image/jpg;base64,{base64_image}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        height: 100vh;  /* Ensure the background takes the full viewport */
        background-color: #f4f4f4;
        overflow: hidden;
    }}

    /* Centering the input box */
    .centered {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 0vh;
        width:20%;
        position: relative;
        z-index: 1;  /* Ensure content is above background */
    }}

    /* Styling the input box */
    .input-container {{
        background-color: rgba(0, 0, 0, 0.7);  /* Darker background for readability */
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        width: 9
        0%;  /* Set a width to avoid stretching */
        margin:0 auto;
        max-width: 500px;  /* Maximum width to keep the input compact */
        color: white;  /* Ensure text is visible */
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);  /* Add a shadow for better contrast */
    }}

    /* Customizing the input field */
    input  {{
        width: 60% !important;  /* Set the width to 40%, adjust as needed */
        padding: 10px;
        margin: 15px auto;
        border-radius: 5px;
        border: 1px solid #ccc;#ccc
        font-size: 36px;
        display:block;
        height:100%;
    }}

    /* Button styling */
    .stButton>button {{
        background-color: #28a745;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        font-size: 16px;
        cursor: pointer;
    }}

    /* Button hover effect */
    .stButton>button:hover {{
        background-color: #218838;
    }}

    /* Text styling */
    h1, h2, h3 {{
        color: white;
    }}

    p {{
        color: white;
    }}
    </style>
    
    """,
    unsafe_allow_html=True
)

# Create the centered input box layout
st.markdown('<div class="centered">', unsafe_allow_html=True)

# Create the content inside the input container
st.markdown(
    """
    <div class="input-container">
        <h1>Primal Health Bot</h1>
        <h3>By Wali M. Mohamed</h3>
        <p>Please ask anything about your primal health</p>
    </div>
    """,
    unsafe_allow_html=True
)
# Function to simulate the question handling and answer generation
def handle_question(question):
    if not question:
        st.error("No question provided")
        return None
    
    conversation_id = str(uuid.uuid4())  # Generate a unique conversation ID
    answer_data = rag(question)  # Call your RAG logic to get the answer

    result = {
        "conversation_id": conversation_id,
        "question": question,
        "answer": answer_data,
    }

    return result


# Function to simulate feedback handling
def handle_feedback(conversation_id, feedback):
    if not conversation_id or feedback not in [1, -1]:
        st.error("Invalid feedback input")
        return None

    st.success(f"Feedback received for conversation {conversation_id}: {feedback}")
    
    # Clear the input field after feedback submission
    # st.session_state.question = ''  # Reset the session state for question


# Initialize session state for the input field and result
if 'question' not in st.session_state:
    st.session_state.question = ''
if 'result' not in st.session_state:
    st.session_state.result = None
# Input box for asking a question (Render after updating session state)
question = st.text_input("Enter your question here...", key="question")
# Handle the "Ask" button click
if st.button("Ask", key="ask_button"):
    if st.session_state.question:
        # Handle the question and get the response
        result = handle_question(st.session_state.question)
        if result:
            st.session_state.result = result
           
    else:
        st.error("Please enter a question.")



# If there's a result, display it and the feedback section
if st.session_state.result:
    result = st.session_state.result
    # Display the answer
    st.write(f"**Answer**: {result['answer']}")

    # Feedback section
    feedback = st.radio(
        "Please provide feedback on the response:",
        options=[1, -1],
        format_func=lambda x: "Good" if x == 1 else "Bad",
        key="feedback_radio"
    )

    if st.button("Submit Feedback", key="feedback_button"):
        handle_feedback(result['conversation_id'], feedback)
        # Clear session state variables
        st.session_state.result = None
        st.session_state.feedback = None
        
# Close the centered div
st.markdown('</div>', unsafe_allow_html=True)

# # Initialize session state for the input field
# if 'question' not in st.session_state:
#     st.session_state.question = ''
# if 'result' not in st.session_state:
#     st.session_state.result = None
# # Handle the "Ask" button click
# if st.button("Ask", key="ask_button"):
#     if st.session_state.question:
#         # Handle the question and get the response
#         result = handle_question(st.session_state.question)
#         if result:
#             st.session_state.result = result
#             # Clear the question input
#             st.session_state.question = ''
#     else:
#         st.error("Please enter a question.")




# # Input box for asking a question
# question = st.text_input("Enter your question here...", key="question")

# if st.button("Ask"):
#     # Handle the question and get the response
#     result = handle_question(question)
    
#     if result:
#         # Display the question and the answer
#         st.write(f"**Answer**: {result['answer']}")
        
#         # Feedback section
#         st.write("Please provide feedback on the response:")
#         feedback = st.radio("Feedback", options=[1, -1], format_func=lambda x: "Good" if x == 1 else "Bad")
        
#         if st.button("Submit Feedback"):
#             handle_feedback(result['conversation_id'], feedback)
#             # Clear session state variables
#             st.session_state.result = None
#             st.session_state.feedback = None
#             # Optionally, clear the feedback radio button selection
#             st.session_state.feedback_radio = None

# # Close the centered div
# st.markdown('</div>', unsafe_allow_html=True)
