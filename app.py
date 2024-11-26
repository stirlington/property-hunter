import requests
from bs4 import BeautifulSoup

# Function to fetch properties for sale
def fetch_properties_for_sale(location):
    url = f"https://www.rightmove.co.uk/property-for-sale/{location}.html"
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to fetch properties for sale.")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    properties = []

    # Parse property listings (adjust selectors based on Rightmove's HTML structure)
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
    url = f"https://www.rightmove.co.uk/house-prices/{location}.html"
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to fetch sold house prices.")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    sold_prices = []

    # Parse sold property listings (adjust selectors based on Rightmove's HTML structure)
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

# Example usage
location = "Redhill"  # Replace with your desired location
properties_for_sale = fetch_properties_for_sale(location)
sold_prices = fetch_sold_prices(location)

# Display results
print("Properties for Sale:")
for property in properties_for_sale:
    print(f"{property['title']} - {property['price']}")
    print(f"Description: {property['description']}")
    print(f"Link: {property['link']}\n")

print("\nSold House Prices:")
for sold_property in sold_prices:
    print(f"{sold_property['title']} - {sold_property['price']}")
    print(f"Description: {sold_property['description']}")
    print(f"Link: {sold_property['link']}\n")
