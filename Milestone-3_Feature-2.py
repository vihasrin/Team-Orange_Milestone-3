#This code was create with help from chapgpt OpenAI
import streamlit as st
import os
from openai import OpenAI

# Use environment variable for API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) 

# List of Santa Clara County zip codes
santa_clara_zip_codes = {
    "95002", "95008", "95013", "95014", "95020", "95032", "95035", "95037",
    "95046", "95101", "95110", "95111", "95112", "95113", "95116", "95117",
    "95118", "95119", "95120", "95121", "95122", "95123", "95124", "95125",
    "95126", "95127", "95128", "95129", "95130", "95131", "95132", "95133",
    "95134", "95135", "95136", "95138", "95139", "95140", "95141", "95148",
    "95150", "95151", "95152", "95153", "95154", "95155", "95156", "95157",
    "95158", "95159", "95160", "95161", "95164", "95170", "95172", "95173",
    "95190", "95191", "95192", "95193", "95194", "95196"
}

# Create a wrapper function
def get_completion(prompt, model="gpt-3.5-turbo"):
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": "You are a flood preparedness expert. Provide detailed, actionable advice on flood prevention, safety, equipment, and preparation. Generate local resources based on the given zip code. Create a personalized emergency kit checklist based on user input about residence type and pets. Generate five relevant FAQs based on common concerns related to flood preparedness."},
                      {"role": "user", "content": prompt}]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error generating advice: {str(e)}"

# Create our Streamlit app
st.set_page_config(page_title="Flood Preparedness Advisor", layout="wide")
st.title("Santa Clara County Flood Preparedness Advisor")
st.markdown("### Get personalized flood preparedness advice based on your location and needs.")

# Main form layout
with st.form(key="chat"):
    # User input section
    st.subheader("Your Information")
    
    zip_code = st.text_input("Enter your zip code (Santa Clara County only)", placeholder="e.g., 95112")
    prompt = st.text_input("What would you like to know about flood preparedness?", placeholder="Ask your question here...")
    
    # Additional user inputs for personalization
    residence_type = st.selectbox("Type of residence", ["House", "Apartment", "Mobile Home", "Other"])
    has_pets = st.checkbox("Do you have pets?")
    specific_concerns = st.text_input("Any specific concerns (e.g., flooding history, health conditions)", placeholder="Describe your concerns...")
    wheelchair_accessibility = st.checkbox("Include wheelchair accessibility considerations")
    preferred_communication = st.selectbox("Preferred communication method", ["Text", "Email", "Phone Call"])
    
    submitted = st.form_submit_button("Submit")
    
    # Modify the prompt based on user inputs
    if wheelchair_accessibility:
        prompt += "\n\nAlso, please provide specific advice considering wheelchair accessibility."
        
    # Adding user residence type, pets, and specific concerns to the prompt
    prompt += f"\n\nUser lives in a {residence_type}. "
    if has_pets:
        prompt += "User has pets that need consideration in the plan. "
    if specific_concerns:
        prompt += f"User has the following specific concerns: {specific_concerns}. "
    prompt += f"User prefers to receive information via {preferred_communication}. "
    prompt += f"User's zip code is {zip_code}."

    # Check if the zip code is within Santa Clara County
    if submitted:
        if zip_code in santa_clara_zip_codes:
            with st.spinner("Generating advice..."):
                response = get_completion(prompt)
            st.success("Here’s your flood preparedness advice:")
            st.markdown(response)
        else:
            st.warning("Please enter a valid zip code within Santa Clara County.")






