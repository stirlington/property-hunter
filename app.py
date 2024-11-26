import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

def search_properties(property_type, num_rooms, location):
    # Construct the URL for Rightmove search
    url = f"https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=POSTCODE%5E{location}&propertyType={property_type}&minBedrooms={num_rooms}"
    
    # Send a request to Rightmove
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Parse the property listings
    properties = []
    for listing in soup.find_all('div', class_='l-searchResult'):
        title = listing.find('h2', class_='propertyCard-title').text.strip()
        price = listing.find('div', class_='propertyCard-priceValue').text.strip()
        properties.append({'title': title, 'price': price})
    
    return properties

def main():
    st.title("Property Search on Rightmove")
    
    property_type = st.selectbox("Select Property Type", ["Flat", "House", "Bungalow"])
    num_rooms = st.number_input("Number of Rooms", min_value=1, max_value=10, value=1)
    location = st.text_input("Enter Location (e.g., postcode or city)")
    
    if st.button("Search"):
        if location:
            properties = search_properties(property_type, num_rooms, location)
            if properties:
                st.write("### Properties Found:")
                df = pd.DataFrame(properties)
                st.dataframe(df)
            else:
                st.write("No properties found.")
        else:
            st.write("Please enter a location.")

if __name__ == "__main__":
    main()
