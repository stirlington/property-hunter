import streamlit as st
import requests
from bs4 import BeautifulSoup

# Function to fetch current properties
def fetch_current_properties(location, min_price, max_price, bedrooms):
    # Placeholder logic for demonstration
    return [
        {"title": "Current Property 1", "description": "Spacious 2-bed flat", "price": 300000, "rental_income": 12000},
        {"title": "Current Property 2", "description": "3-bed house with garden", "price": 250000, "rental_income": 15000},
    ]

# Function to fetch sold prices
def fetch_sold_prices(location, min_price, max_price, bedrooms):
    # Placeholder logic for demonstration
    return [
        {"title": "Sold Property 1", "description": "Recently sold 2-bed flat", "price": 280000},
        {"title": "Sold Property 2", "description": "Recently sold 3-bed house", "price": 240000},
    ]

# Function to calculate gross yield
def calculate_yield(price, rental_income):
    return round((rental_income / price) * 100, 2)

# Streamlit app layout
st.title("Property Search")

# Input fields for search criteria
location = st.text_input("Location")
min_price = st.number_input("Min Price (£)", min_value=0, value=0)
max_price = st.number_input("Max Price (£)", min_value=0, value=1000000)
bedrooms = st.selectbox("Bedrooms", options=["Any", "1", "2", "3", "4", "5+"])

# Search button functionality
if st.button("Search"):
    # Fetch properties based on the criteria
    current_properties = fetch_current_properties(location, min_price, max_price, bedrooms)
    sold_prices = fetch_sold_prices(location, min_price, max_price, bedrooms)

    # Add yield calculation for current properties
    for property in current_properties:
        property['yield'] = calculate_yield(property['price'], property['rental_income'])

    # Display results
    st.subheader("Current Properties")
    if current_properties:
        for property in current_properties:
            st.write(f"**{property['title']}**")
            st.write(f"{property['description']}")
            st.write(f"Price: £{property['price']:,}")
            st.write(f"Rental Income: £{property['rental_income']:,}/year")
            st.write(f"Yield: {property['yield']}%")
            st.write("---")
    else:
        st.write("No current properties found.")

    st.subheader("Sold Prices")
    if sold_prices:
        for property in sold_prices:
            st.write(f"**{property['title']}**")
            st.write(f"{property['description']}")
            st.write(f"Sold Price: £{property['price']:,}")
            st.write("---")
    else:
        st.write("No sold prices found.")
