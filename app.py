import streamlit as st
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

# Page Configuration
st.set_page_config(
    page_title="Agriculture Chatbot",
    page_icon="🌾",
    layout="centered"
)

# Custom CSS for Background and Typography
custom_css = """
<style>
/* Main app background with a subtle overlay for contrast */
.stApp {
    background: linear-gradient(rgba(255, 255, 255, 0.88), rgba(255, 255, 255, 0.88)),
                url("https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=1920&q=80");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* Card container for the header and form */
div.css-1r6slb0, div.stForm, div.stTextArea {
    background-color: rgba(255, 255, 255, 0.95);
    border-radius: 12px;
    padding: 10px;
}

/* Styled Heading */
h1 {
    color: #1b4332 !important;
    font-weight: 700;
    text-shadow: 1px 1px 2px rgba(255,255,255,0.8);
}

/* Subtitle and Paragraphs */
p, label {
    color: #2d6a4f !important;
    font-weight: 500;
}

/* Custom primary button styling */
.stButton > button {
    background-color: #2d6a4f;
    color: white !important;
    font-size: 16px;
    font-weight: 600;
    border-radius: 8px;
    border: none;
    padding: 8px 24px;
    transition: all 0.3s ease;
    width: 100%;
}

.stButton > button:hover {
    background-color: #1b4332;
    color: white !important;
    border: none;
}

/* Success Box Styling */
.stSuccess {
    background-color: rgba(235, 247, 238, 0.95);
    border-left: 5px solid #2d6a4f;
    border-radius: 8px;
}
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# Application UI Header
st.title("🌾 Agriculture AI Advisor")
st.markdown("Your intelligent companion for crop guidance, soil health, and best farming practices.")

st.divider()

# Input Section inside a container
with st.container():
    question = st.text_area(
        label="Ask your agriculture query:",
        placeholder="e.g., What are the best organic pest control methods for tomato plants?",
        height=120
    )

    ask_button = st.button("Get Expert Answer 🚜")

# Process Query
if ask_button:
    if not question.strip():
        st.warning("Please enter a question before submitting.")
    else:
        with st.spinner("Analyzing your agriculture query..."):
            llm = ChatGroq(
                model="llama-3.1-8b-instant",
                temperature=0.3
            )

            prompt = ChatPromptTemplate.from_template(
                """
You are an Agriculture Expert.

Your job is to answer ONLY agriculture-related questions.

Topics include:
- Crops
- Soil
- Fertilizers
- Irrigation
- Seeds
- Farming
- Pest Control
- Organic Farming
- Plant Diseases
- Harvesting

If the user asks anything outside agriculture,
reply:

"Sorry, I only answer Agriculture related questions."

Question
{question}

Provide:
1. Simple explanation
2. Step-by-step guidance
3. Best Practices
4. Precautions if needed
"""
            )
            
            chain = prompt | llm

            response = chain.invoke({"question": question})

            st.markdown("### 📋 Expert Advice")
            st.success(response.content)