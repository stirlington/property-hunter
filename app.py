import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# Configure Selenium WebDriver
def configure_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode for Streamlit Cloud compatibility
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = Service("/usr/bin/chromedriver")  # Path to ChromeDriver (adjust if needed)
    return webdriver.Chrome(service=service, options=chrome_options)

# Function to fetch properties for sale
def fetch_properties_for_sale(location, min_price, max_price, bedrooms):
    driver = configure_driver()
    url = f"https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=POSTCODE%5E{location}&minPrice={min_price}&maxPrice={max_price}&minBedrooms={bedrooms}&radius=0.5"
    driver.get(url)
    time.sleep(5)  # Allow time for the page to load

    properties = []
    try:
        listings = driver.find_elements(By.CLASS_NAME, "propertyCard")
        for listing in listings:
            try:
                title = listing.find_element(By.CLASS_NAME, "propertyCard-title").text.strip()
                description = listing.find_element(By.CLASS_NAME, "propertyCard-description").text.strip()
                price = listing.find_element(By.CLASS_NAME, "propertyCard-priceValue").text.strip()
                link = listing.find_element(By.TAG_NAME, "a").get_attribute("href")
                properties.append({
                    'title': title,
                    'description': description,
                    'price': price,
                    'link': link
                })
            except Exception:
                continue
    except Exception as e:
        st.error(f"Error fetching properties: {e}")
    finally:
        driver.quit()

    return properties

# Function to fetch sold house prices
def fetch_sold_prices(location):
    driver = configure_driver()
    url = f"https://www.rightmove.co.uk/house-prices/{location}.html"
    driver.get(url)
    time.sleep(5)  # Allow time for the page to load

    sold_prices = []
    try:
        listings = driver.find_elements(By.CLASS_NAME, "soldPropertyCard")
        for listing in listings:
            try:
                title = listing.find_element(By.CLASS_NAME, "soldPropertyCard-title").text.strip()
                description = listing.find_element(By.CLASS_NAME, "soldPropertyCard-description").text.strip()
                price = listing.find_element(By.CLASS_NAME, "soldPropertyCard-priceValue").text.strip()
                link = listing.find_element(By.TAG_NAME, "a").get_attribute("href")
                sold_prices.append({
                    'title': title,
                    'description': description,
                    'price': price,
                    'link': link
                })
            except Exception:
                continue
    except Exception as e:
        st.error(f"Error fetching sold prices: {e}")
    finally:
        driver.quit()

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
