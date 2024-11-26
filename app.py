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

# Function to calculate gross rental yield
def calculate_yield(current_price, sold_price):
    try:
        current_price = float(current_price.replace("£", "").replace(",", ""))
        sold_price = float(sold_price.replace("£", "").replace(",", ""))
        yield_percentage = ((current_price - sold_price) / sold_price) * 100
        return round(yield_percentage, 2)
    except ValueError:
        return None

# Streamlit app layout
st.set_page_config(page_title="Property Yield Calculator", layout="wide")
st.title("🏠 Property Yield Calculator")

# Input fields for search criteria
with st.sidebar:
    st.header("Search Criteria")
    location = st.text_input("Location (e.g., RH1 for Redhill)", value="RH1")
    min_price = st.number_input("Min Price (£)", min_value=0, value=100000, step=5000)
    max_price = st.number_input("Max Price (£)", min_value=0, value=500000, step=5000)
    bedrooms = st.selectbox("Bedrooms", options=["Any", "1", "2", "3", "4", "5+"])

# Example data for demonstration purposes (replace with live data fetching logic)
current_properties = [
    {"title": "2-Bed Flat", "price": "£300,000", "url": "https://example.com/property1"},
    {"title": "3-Bed House", "price": "£250,000", "url": "https://example.com/property2"},
]
sold_properties = [
    {"title": "Sold 2-Bed Flat", "price": "£200,000"},
    {"title": "Sold 3-Bed House", "price": "£180,000"},
]

# Search button functionality
if st.button("Search"):
    with st.spinner("Generating results..."):
        # Generate URLs
        for_sale_url = generate_for_sale_url(location, min_price, max_price, bedrooms)
        sold_prices_url = generate_sold_prices_url(location)

        # Display generated URLs
        st.subheader("Generated Search Links")
        st.markdown(f"### [View Properties For Sale](<{for_sale_url}>)")
        st.markdown(f"### [View Sold House Prices](<{sold_prices_url}>)")

        # Calculate yields based on example data
        st.subheader("Investment Opportunities")
        opportunities = []
        for current in current_properties:
            for sold in sold_properties:
                yield_percentage = calculate_yield(current["price"], sold["price"])
                if yield_percentage is not None:
                    opportunities.append({
                        "title": current["title"],
                        "current_price": current["price"],
                        "sold_price": sold["price"],
                        "yield": yield_percentage,
                        "url": current["url"]
                    })

        # Sort opportunities by yield (highest first)
        opportunities.sort(key=lambda x: x["yield"], reverse=True)

        # Display opportunities
        if opportunities:
            for opp in opportunities:
                st.markdown(f"### [{opp['title']}]({opp['url']})")
                st.write(f"**Current Price**: {opp['current_price']}")
                st.write(f"**Sold Price**: {opp['sold_price']}")
                st.write(f"**Yield**: {opp['yield']}%")
                st.write("---")
        else:
            st.write("No investment opportunities found.")
