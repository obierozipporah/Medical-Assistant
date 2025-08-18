import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()

# ✅ Configure Gemini with API key from .env
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# ✅ Initialize model
model = genai.GenerativeModel("gemini-1.5-flash")

# ✅ Streamlit app setup
st.set_page_config(page_title="Medical Assistant", page_icon="🩺")
st.title("🩺 AI Medical Assistant")

# ✅ Session state for conversation memory
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# Function to get Gemini response
def get_gemini_response(user_input, conversation):
    # Combine conversation history into the prompt
    history = "\n".join(
        [f"Patient: {msg['user']}\nDoctor: {msg['assistant']}" for msg in conversation]
    )

    prompt = f"""
    Imagine you are a medical expert and you are giving accurate medical advice to a patient.
    You are presented with a medical query and asked to provide a response with a detailed explanation.
    Note that don't mention any inaccurate or misleading information.

    Conversation History:
    {history}

    Current Medical Query: {user_input}

    Key Details:
    - Provide precise information related to the patient's medical concern.
    - Indicate if any diagnostic tests or examinations have been performed.
    - Specify the current medications or treatments prescribed.
    - The response should be in a paragraph format but not in point-wise.
    - If only a specific disease name is mentioned, response must contain the symptoms, causes, and treatment of the disease in a paragraph format.

    Guidelines:
    - Use clear and concise language.
    - The vocabulary should be appropriate for the medical context.
    - Include specific parameters or considerations within the medical context.
    - If the response contains a list of items, convert it into a paragraph format.
    - Avoid using abbreviations or acronyms.
    - Refrain from presenting inaccurate or ambiguous information.
    - Ensure the query is focused and not overly broad.
    """

    response = model.generate_content(prompt)
    return response.text.strip()

# ✅ User Input
user_input = st.text_input("Enter your medical query:")

if st.button("Get Advice") and user_input:
    with st.spinner("Analyzing..."):
        gemini_response = get_gemini_response(user_input, st.session_state.conversation)

        # Save to conversation memory
        st.session_state.conversation.append(
            {"user": user_input, "assistant": gemini_response}
        )

# ✅ Display conversation history
if st.session_state.conversation:
    st.subheader("Conversation")
    for chat in st.session_state.conversation:
        st.markdown(f"**🧑 Patient:** {chat['user']}")
        st.markdown(f"**👨‍⚕️ Doctor:** {chat['assistant']}")
        st.markdown("---")
