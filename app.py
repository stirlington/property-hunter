from flask import Flask, request, jsonify

app = Flask(__name__)

# Fetch current properties (Placeholder logic)
def fetch_current_properties(location, min_price, max_price, bedrooms):
    return [
        {"title": "Current Property 1", "description": "Spacious 2-bed flat", "price": 300000, "rental_income": 12000},
        {"title": "Current Property 2", "description": "3-bed house with garden", "price": 250000, "rental_income": 15000},
    ]

# Fetch sold prices (Placeholder logic)
def fetch_sold_prices(location, min_price, max_price, bedrooms):
    return [
        {"title": "Sold Property 1", "description": "Recently sold 2-bed flat", "price": 280000},
        {"title": "Sold Property 2", "description": "Recently sold 3-bed house", "price": 240000},
    ]

# Calculate gross yield
def calculate_yield(price, rental_income):
    return round((rental_income / price) * 100, 2)

@app.route('/search-properties', methods=['GET'])
def search_properties():
    location = request.args.get('location')
    min_price = int(request.args.get('min_price', 0))
    max_price = int(request.args.get('max_price', 1000000))
    bedrooms = request.args.get('bedrooms')

    # Fetch properties
    current_properties = fetch_current_properties(location, min_price, max_price, bedrooms)
    sold_prices = fetch_sold_prices(location, min_price, max_price, bedrooms)

    # Add yield calculation for current properties
    for property in current_properties:
        property['yield'] = calculate_yield(property['price'], property['rental_income'])

    # Combine results
    results = {
        "current_properties": current_properties,
        "sold_prices": sold_prices,
    }
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
