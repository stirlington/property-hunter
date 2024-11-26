import streamlit as st

# Function to construct Rightmove search URL for cheapest properties
def generate_for_sale_url(location, min_price, max_price, bedrooms):
    base_url = "https://www.rightmove.co.uk/property-for-sale/find.html"
    location_param = f"locationIdentifier=OUTCODE%5E{location}"
    min_price_param = f"minPrice={min_price}"
    max_price_param = f"maxPrice={max_price}"
    bedrooms_param = f"minBedrooms={bedrooms}" if bedrooms != "Any" else ""
    sort_order = "sortType=1"  # Sort by lowest price
    radius_param = "radius=0.5"

    # Combine parameters into a valid URL
    params = "&".join(filter(None, [location_param, min_price_param, max_price_param, bedrooms_param, sort_order, radius_param]))
    return f"{base_url}?{params}"

# Function to calculate After Repair Value (ARV)
def calculate_arv(current_price, renovation_cost, market_increase_percent):
    try:
        current_price = float(current_price.replace("£", "").replace(",", ""))
        arv = current_price + renovation_cost + (current_price * market_increase_percent / 100)
        return round(arv, 2)
    except ValueError:
        return None

# Function to estimate profit margin
def calculate_profit(arv, current_price, renovation_cost):
    try:
        current_price = float(current_price.replace("£", "").replace(",", ""))
        profit = arv - (current_price + renovation_cost)
        return round(profit, 2)
    except ValueError:
        return None

# Streamlit app layout
st.set_page_config(page_title="Property Investment Analyzer", layout="wide")
st.title("🏠 Property Investment Analyzer")

# Input fields for search criteria
with st.sidebar:
    st.header("Search Criteria")
    location = st.text_input("Location (e.g., RH1 for Redhill)", value="RH1")
    min_price = st.number_input("Min Price (£)", min_value=0, value=100000, step=5000)
    max_price = st.number_input("Max Price (£)", min_value=0, value=500000, step=5000)
    bedrooms = st.selectbox("Bedrooms", options=["Any", "1", "2", "3", "4", "5+"])
    renovation_cost = st.number_input("Estimated Renovation Cost (£)", min_value=0, value=20000)
    market_increase_percent = st.slider("Expected Market Increase (%)", min_value=0.0, max_value=50.0, value=10.0)

# Search button functionality
if st.button("Search"):
    with st.spinner("Generating results..."):
        # Generate Rightmove URL for cheapest properties
        for_sale_url = generate_for_sale_url(location, min_price, max_price, bedrooms)

        # Display generated URL
        st.subheader("Search Link")
        st.markdown(f"### [View Cheapest Properties on Rightmove](<{for_sale_url}>)")

        # Example data for demonstration purposes (replace with live data fetching logic)
        properties_for_sale = [
            {"title": "2-Bed Flat", "price": "£300,000", "url": f"{for_sale_url}&propertyId=12345"},
            {"title": "3-Bed House", "price": "£250,000", "url": f"{for_sale_url}&propertyId=67890"},
            {"title": "Studio Apartment", "price": "£150,000", "url": f"{for_sale_url}&propertyId=54321"},
        ]

        # Calculate ARV and profit margins
        investment_opportunities = []
        for property in properties_for_sale:
            arv = calculate_arv(property["price"], renovation_cost, market_increase_percent)
            profit = calculate_profit(arv, property["price"], renovation_cost)
            investment_opportunities.append({
                "title": property["title"],
                "current_price": property["price"],
                "arv": f"£{arv:,}" if arv else "N/A",
                "profit": f"£{profit:,}" if profit else "N/A",
                "url": property["url"]
            })

        # Display investment opportunities
        st.subheader("Investment Opportunities")
        if investment_opportunities:
            for opp in investment_opportunities:
                st.markdown(f"### [{opp['title']}]({opp['url']})")
                st.write(f"**Current Price**: {opp['current_price']}")
                st.write(f"**After Repair Value (ARV)**: {opp['arv']}")
                st.write(f"**Estimated Profit**: {opp['profit']}")
                st.write("---")
        else:
            st.write("No investment opportunities found.")
