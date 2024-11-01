import streamlit as st
import requests
from bs4 import BeautifulSoup

# Function to extract flood-related information from a URL, excluding headings or titles
def extract_flood_info_from_url(url, keyword=None, max_paragraphs=5):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract title separately
        title = soup.title.string if soup.title else 'No title found'
        
        # Extract paragraphs only, filtering out likely titles or very short text
        paragraphs = [
            para.get_text().strip() for para in soup.find_all('p') 
            if para.get_text().strip() and len(para.get_text().strip()) > 30  # Avoid very short text
        ]
        
        # If a keyword is provided, filter paragraphs to include only those with the keyword
        if keyword:
            paragraphs = [para for para in paragraphs if keyword.lower() in para.lower()]
        
        # Limit the paragraphs to the specified max_paragraphs
        key_points = paragraphs[:max_paragraphs]

        return title, key_points
    except Exception as e:
        return str(e), []

# Streamlit UI
st.set_page_config(page_title="Flood Information Extractor", page_icon="🌊")

# Sidebar for inputs
st.sidebar.header("Flood Information Extractor 🌊")
st.sidebar.write("Extract relevant flood-related information from any webpage.")

# User input for URL and keyword
url_input = st.sidebar.text_input("Enter the URL of the flood-related website:")
keyword_input = st.sidebar.text_input("Optional: Specify a flood-related term to focus on:")
max_paragraphs = st.sidebar.slider("Number of key points to display:", min_value=1, max_value=20, value=5)

# Main page content
st.title("🌊 Flood Information Extractor")
st.write("Use this tool to quickly retrieve key flood information from any webpage. Simply enter the URL, specify a keyword if desired, and get flood-related insights in bullet points.")

st.markdown("---")  # Divider

# Fetch and display information when the button is clicked
if st.sidebar.button("Extract Flood Info"):
    if url_input:
        with st.spinner("Extracting information... Please wait."):
            title, key_points = extract_flood_info_from_url(url_input, keyword=keyword_input, max_paragraphs=max_paragraphs)
        
        st.subheader("🔍 Extracted Information")
        
        if title:
            st.markdown(f"**Page Title:** {title}")
        
        if key_points:
            st.write("### Key Flood Information:")
            for i, point in enumerate(key_points, 1):
                st.write(f"{i}. {point}")
        else:
            st.warning("No relevant flood information found. Try refining your keyword or checking the URL content.")
        
    else:
        st.sidebar.error("Please enter a valid URL.")
else:
    st.info("Enter a URL in the sidebar and click 'Extract Flood Info' to start.")








