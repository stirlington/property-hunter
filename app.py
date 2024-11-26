import streamlit as st
import requests
from bs4 import BeautifulSoup

def fetch_properties(location, min_price, max_price, bedrooms):
    # Construct the URL for Rightmove search
    location_identifier = location.replace(" ", "+")  # Format the location for the URL
    url = f"https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier={location_identifier}&minPrice={min_price}&maxPrice={max_price}&bedrooms={bedrooms}&radius=0.5"
    
    # Send a GET request to the Rightmove search page
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code != 200:
        st.error("Failed to retrieve data from Rightmove.")
        return []

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find property listings (this will depend on the actual HTML structure)
    properties = []
    for listing in soup.find_all('div', class_='propertyCard'):
        title = listing.find('h2', class_='propertyCard-title').text.strip()
        description = listing.find('div', class_='propertyCard-description').text.strip()
        price = listing.find('div', class_='propertyCard-priceValue').text.strip()
        
        properties.append({
            'title': title,
            'description': description,
            'price': price
        })
    
    return properties

# Streamlit app layout
st.title("Property Search")

# Input fields for search criteria
location = st.text_input("Location")
min_price = st.number_input("Min Price", min_value=0, value=0)
max_price = st.number_input("Max Price", min_value=0, value=1000000)
bedrooms = st.selectbox("Bedrooms", options=["Any", "1", "2", "3", "4", "5+"])

# Search button
if st.button("Search"):
    # Fetch properties based on the criteria
    properties = fetch_properties(location, min_price, max_price, bedrooms)

    # Display properties
    if properties:
        for property in properties:
            st.write(f"**{property['title']}**: {property['description']} - {property['price']}")
    else:
        st.write("No properties found.")
