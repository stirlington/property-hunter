import streamlit as st

# Function to construct Rightmove search URL for properties for sale
def generate_for_sale_url(location, min_price, max_price, bedrooms):
    base_url = "https://www.rightmove.co.uk/property-for-sale/find.html"
    location_param = f"locationIdentifier=OUTCODE%5E{location}"
    min_price_param = f"minPrice={min_price}"
    max_price_param = f"maxPrice={max_price}"
    bedrooms_param = f"minBedrooms={bedrooms}" if bedrooms != "Any" else ""
    radius_param = "radius=0.5"

    # Combine parameters into a valid URL
    params = "&".join(filter(None, [location_param, min_price_param, max_price_param, bedrooms_param, radius_param]))
    return f"{base_url}?{params}"

# Function to construct Rightmove search URL for sold house prices
def generate_sold_prices_url(location):
    base_url = "https://www.rightmove.co.uk/house-prices/"
    return f"{base_url}{location}.html"

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
    with st.spinner("Generating search URLs..."):
        # Generate URLs
        for_sale_url = generate_for_sale_url(location, min_price, max_price, bedrooms)
        sold_prices_url = generate_sold_prices_url(location)

        # Display results
        st.subheader("Search Results")
        st.markdown(f"### [View Properties For Sale](<{for_sale_url}>)")
        st.write(f"Search for properties in {location} with the following criteria:")
        st.write(f"- **Min Price**: £{min_price:,}")
        st.write(f"- **Max Price**: £{max_price:,}")
        st.write(f"- **Bedrooms**: {bedrooms}")
        st.write("---")

        st.markdown(f"### [View Sold House Prices](<{sold_prices_url}>)")
        st.write(f"View historical sold house prices in {location}.")
