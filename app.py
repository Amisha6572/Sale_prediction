import streamlit as st
import numpy as np
import pickle
from PIL import Image
import io
import base64

# Configure page
st.set_page_config(
    page_title="Sales Prediction App",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load trained model
model = pickle.load(open("best_model.pkl", "rb"))

# Custom CSS with background styling
def add_bg_style():
    """Add custom CSS styling with background images and gradients"""
    st.markdown("""
    <style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    /* Title styling */
    .title-container {
        background: rgba(255, 255, 255, 0.95);
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        margin-bottom: 30px;
        text-align: center;
        border-left: 5px solid #667eea;
    }
    
    .title-container h1 {
        color: #2d3748;
        margin: 0;
        font-size: 2.5em;
    }
    
    /* Input section styling */
    .input-section {
        background: rgba(255, 255, 255, 0.95);
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        margin: 20px 0;
        border-left: 5px solid #667eea;
    }
    
    .input-section h3 {
        color: #2d3748;
        margin-top: 0;
    }
    
    /* Input field styling */
    .stNumberInput {
        margin-bottom: 15px;
    }
    
    .stNumberInput > label {
        font-weight: 600;
        color: #4a5568;
    }
    
    /* Column styling */
    .ad-column {
        background: rgba(255, 255, 255, 0.95);
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border-top: 4px solid #667eea;
        margin: 10px 0;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 12px 40px;
        border-radius: 8px;
        font-size: 18px;
        font-weight: 600;
        width: 100%;
        cursor: pointer;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
    }
    
    /* Success message */
    .stSuccess {
        background: rgba(72, 187, 120, 0.1) !important;
        border-left: 4px solid #48bb78 !important;
    }
    
    /* Error message */
    .stError {
        background: rgba(245, 101, 101, 0.1) !important;
        border-left: 4px solid #f56565 !important;
    }
    
    /* Icon styling */
    .icon-large {
        font-size: 3em;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Apply styling
add_bg_style()

# Header with title
st.markdown("""
<div class="title-container">
    <h1>📈 Sales Increase/Decrease Prediction App</h1>
    <p style="color: #718096; font-size: 1.1em; margin: 10px 0 0 0;">
    Predict sales trends based on advertisement spending
    </p>
</div>
""", unsafe_allow_html=True)

# Create sections with columns
col1, col2, col3 = st.columns(3)

# TV Advertisement Section
with col1:
    st.markdown("""
    <div class="ad-column">
        <div style="text-align: center; margin-bottom: 15px;">
            <div class="icon-large">📺</div>
            <h3 style="color: #2d3748; margin: 5px 0;">TV Advertising</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)
    tv = st.number_input("💰 TV Budget ($)", min_value=0.0, key="tv")

# Radio Advertisement Section
with col2:
    st.markdown("""
    <div class="ad-column">
        <div style="text-align: center; margin-bottom: 15px;">
            <div class="icon-large">📻</div>
            <h3 style="color: #2d3748; margin: 5px 0;">Radio Advertising</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)
    radio = st.number_input("💰 Radio Budget ($)", min_value=0.0, key="radio")

# Newspaper Advertisement Section
with col3:
    st.markdown("""
    <div class="ad-column">
        <div style="text-align: center; margin-bottom: 15px;">
            <div class="icon-large">📰</div>
            <h3 style="color: #2d3748; margin: 5px 0;">Newspaper Advertising</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)
    newspaper = st.number_input("💰 Newspaper Budget ($)", min_value=0.0, key="newspaper")

# Prediction section
st.markdown("<div style='margin: 30px 0;'></div>", unsafe_allow_html=True)

# Prediction button and results
col_button1, col_button2, col_button3 = st.columns([1, 2, 1])

with col_button2:
    if st.button("🚀 Predict Sales Trend", key="predict_btn"):
        input_data = np.array([[tv, radio, newspaper]])
        prediction = model.predict(input_data)
        
        # Results display
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        
        if prediction[0] == 1:
            st.markdown("""
            <div style="background: rgba(72, 187, 120, 0.1); 
                        border-left: 5px solid #48bb78;
                        padding: 25px;
                        border-radius: 8px;
                        text-align: center;
                        margin: 20px 0;">
                <h2 style="color: #22863a; margin: 0;">✅ Sales Will Increase 📈</h2>
                <p style="color: #6f42c1; font-size: 1.1em; margin: 10px 0 0 0;">
                Excellent! Your advertisement strategy will boost sales.
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: rgba(245, 101, 101, 0.1); 
                        border-left: 5px solid #f56565;
                        padding: 25px;
                        border-radius: 8px;
                        text-align: center;
                        margin: 20px 0;">
                <h2 style="color: #cb2431; margin: 0;">❌ Sales Will Decrease 📉</h2>
                <p style="color: #6f42c1; font-size: 1.1em; margin: 10px 0 0 0;">
                Consider revising your advertisement strategy.
                </p>
            </div>
            """, unsafe_allow_html=True)

# Footer with info
st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
st.markdown("""
<div style="background: rgba(255, 255, 255, 0.9); 
            padding: 20px;
            border-radius: 8px;
            margin-top: 30px;
            border-top: 3px solid #667eea;
            text-align: center;">
    <p style="color: #4a5568; margin: 0;">
    💡 <strong>Tip:</strong> Adjust your advertisement budget across different channels to find the optimal strategy for sales growth.
    </p>
</div>
""", unsafe_allow_html=True)
