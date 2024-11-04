import streamlit as st
import pandas as pd
from opencage.geocoder import OpenCageGeocode
from io import BytesIO
import firebase_admin
from firebase_admin import credentials, firestore
import folium
from streamlit_folium import st_folium
from PIL import Image

# Initialize Firebase app
cred = credentials.Certificate("/Users/harshilpurohit/Desktop/Projects/floodguard-ai-firebase-adminsdk-1gehw-297a26cec3.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

# Initialize Firestore client
db = firestore.client()

# Initialize OpenCage Geocoder
geocoder = OpenCageGeocode("469906be508849a68838fbcb10c31ce0")

# Initialize map data list
if 'flood_data' not in st.session_state:
    st.session_state.flood_data = []

# Title and description
st.title('Community Flood Reporting Map')
st.write("Report flood incidents in your area, and see them displayed on the map in real-time.")

# Sidebar form for reporting a flood incident
st.sidebar.header("Report a Flood")
with st.sidebar.form("flood_form"):
    street_address = st.text_input("Street Address")
    
    # Dropdown for flood type
    flood_type = st.selectbox("Cause of Flood", ["Storm Drain Blockage", "Well/Reservoir Overflow", "Pipe Burst", "Debris", "Other"])
    
    # Conditional text input for custom flood type
    if flood_type == "Other":
        custom_flood_type = st.text_input("Please specify the cause of flooding")
    else:
        custom_flood_type = flood_type  # Use selected flood type if it's not "Other"
    
    severity = st.slider("Flood Severity (1 = Minor, 5 = Severe)", min_value=1, max_value=5)
    image = st.file_uploader("Upload a flood image", type=["jpg", "png", "jpeg"])

    submitted = st.form_submit_button("Submit Report")

# Function to get latitude and longitude from an address
def get_lat_lon(address):
    result = geocoder.geocode(address)
    if result:
        return result[0]['geometry']['lat'], result[0]['geometry']['lng']
    else:
        st.error("Could not find the location. Please enter a valid address.")
        return None, None

# Process form submission
if submitted and street_address:
    lat, lon = get_lat_lon(street_address)
    if lat is not None and lon is not None:
        # Save the data in the session state
        flood_entry = {
            "lat": lat,
            "lon": lon,
            "type": custom_flood_type,
            "severity": severity,
            "address": street_address,
            "image": image.read() if image is not None else None  # Read the image bytes if present
        }
        st.session_state.flood_data.append(flood_entry)

        # Save to Firebase Firestore
        db.collection("flood_reports").add(flood_entry)

        # Confirmation message
        st.success(f"Flood report added at {street_address}. See it on the map below.")

# Fetch flood reports from Firebase Firestore
def fetch_flood_reports():
    docs = db.collection("flood_reports").stream()
    return [
        {
            "lat": doc.get("lat"),
            "lon": doc.get("lon"),
            "type": doc.get("type"),
            "severity": doc.get("severity"),
            "address": doc.get("address"),
            "image": doc.get("image")  # Ensure we get the image data from Firestore
        } for doc in docs
    ]

# Load flood data from Firebase into session state on app load
if not st.session_state.flood_data:
    st.session_state.flood_data = fetch_flood_reports()

# Convert session data to DataFrame for mapping
df = pd.DataFrame(st.session_state.flood_data)

# Create a folium map
if not df.empty:
    m = folium.Map(location=[df["lat"].mean(), df["lon"].mean()], zoom_start=12)

    # Add red circle markers to the map with clickable popups
    for _, row in df.iterrows():
        folium.Marker(
            location=[row["lat"], row["lon"]],
            popup=folium.Popup(
                f"Address: {row['address']}<br>Type: {row['type']}<br>Severity: {row['severity']}",
                parse_html=True
            ),
            icon=folium.Icon(color="red")  # Red icon for flood reports
        ).add_to(m)

    # Display the map in Streamlit
    st_folium(m, width=700, height=500)
else:
    st.info("No flood reports submitted yet.")

# Display the flood reports as text
if not df.empty:
    st.write("### Reported Flood Incidents:")
    for idx, row in df.iterrows():
        st.write(f"**Location**: {row['address']}")
        st.write(f"**Flood Type**: {row['type']}")
        st.write(f"**Severity**: {row['severity']}")
        
        # Display image if available
        if row['image'] is not None:
            # Convert image bytes to a PIL image and display it
            image = Image.open(BytesIO(row['image']))
            st.image(image, caption=f"Flood at {row['address']}", use_column_width=True)
        
        st.write("---")
