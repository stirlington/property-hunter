import streamlit as st
import requests
from bs4 import BeautifulSoup

# Function to fetch properties for sale
def fetch_properties_for_sale(location, min_price, max_price, bedrooms):
    # Construct the URL (replace POSTCODE with location if needed)
    url = f"https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=POSTCODE&minPrice={min_price}&maxPrice={max_price}&minBedrooms={bedrooms}&radius=0.5"
    
    # Send GET request
    response = requests.get(url)
    if response.status_code != 200:
        return []
    
    # Parse HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    properties = []
    
    # Extract property details
    for listing in soup.find_all('div', class_='propertyCard'):
        try:
            title = listing.find('h2', class_='propertyCard-title').text.strip()
            description = listing.find('span', class_='propertyCard-description').text.strip()
            price = listing.find('div', class_='propertyCard-priceValue').text.strip()
            link = "https://www.rightmove.co.uk" + listing.find('a', class_='propertyCard-link')['href']
            properties.append({
                'title': title,
                'description': description,
                'price': price,
                'link': link
            })
        except AttributeError:
            continue
    
    return properties

# Function to fetch sold house prices
def fetch_sold_prices(location):
    # Construct the URL (replace POSTCODE with location if needed)
    url = f"https://www.rightmove.co.uk/house-prices/{location}.html"
    
    # Send GET request
    response = requests.get(url)
    if response.status_code != 200:
        return []
    
    # Parse HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    sold_prices = []
    
    # Extract sold property details
    for listing in soup.find_all('div', class_='soldPropertyCard'):
        try:
            title = listing.find('h2', class_='soldPropertyCard-title').text.strip()
            description = listing.find('span', class_='soldPropertyCard-description').text.strip()
            price = listing.find('div', class_='soldPropertyCard-priceValue').text.strip()
            link = "https://www.rightmove.co.uk" + listing.find('a', class_='soldPropertyCard-link')['href']
            sold_prices.append({
                'title': title,
                'description': description,
                'price': price,
                'link': link
            })
        except AttributeError:
            continue
    
    return sold_prices

# Streamlit app layout
st.set_page_config(page_title="Property Search", layout="wide")
st.title("🏠 Property Search")

# Input fields for search criteria
with st.sidebar:
    st.header("Search Criteria")
    location = st.text_input("Location (e.g., RH1 for Redhill)", value="RH1")
    min_price = st.number_input("Min Price (£)", min_value=0, value=100000, step=5000)
    max_price = st.number_input("Max Price (£)", min_value=0, value=500000, step=5000)
    bedrooms = st.selectbox("Bedrooms", options=["Any", "1", "2", "3", "4", "5+"])

# Search button functionality
if st.button("Search"):
    with st.spinner("Fetching properties..."):
        # Fetch properties for sale and sold prices
        properties_for_sale = fetch_properties_for_sale(location, min_price, max_price, bedrooms)
        sold_prices = fetch_sold_prices(location)

        # Display results
        st.subheader("Properties For Sale")
        if properties_for_sale:
            for property in properties_for_sale:
                st.markdown(f"### [{property['title']}]({property['link']})")
                st.write(f"**Description**: {property['description']}")
                st.write(f"**Price**: {property['price']}")
                st.write("---")
        else:
            st.write("No properties found.")

        st.subheader("Sold Prices")
        if sold_prices:
            for sold_property in sold_prices:
                st.markdown(f"### [{sold_property['title']}]({sold_property['link']})")
                st.write(f"**Description**: {sold_property['description']}")
                st.write(f"**Sold Price**: {sold_property['price']}")
                st.write("---")
        else:
            st.write("No sold prices found.")
