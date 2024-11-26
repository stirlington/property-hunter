document.getElementById('property-search-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const location = document.getElementById('search-location').value;
    const minPrice = document.getElementById('min-price').value;
    const maxPrice = document.getElementById('max-price').value;
    const bedrooms = document.getElementById('bedrooms').value;

    // Fetch data from backend
    const response = await fetch(`/search-properties?location=${location}&min_price=${minPrice}&max_price=${maxPrice}&bedrooms=${bedrooms}`);
    const data = await response.json();

    displayResults(data);
});

function displayResults(data) {
    const resultsContainer = document.querySelector('.results-container');
    resultsContainer.innerHTML = '';

    // Display current properties
    if (data.current_properties.length > 0) {
        const currentHeader = document.createElement('h2');
        currentHeader.textContent = 'Current Properties';
        resultsContainer.appendChild(currentHeader);

        data.current_properties.forEach(property => {
            const propertyElement = document.createElement('div');
            propertyElement.className = 'property-item';
            propertyElement.innerHTML = `
                <h3>${property.title}</h3>
                <p>${property.description}</p>
                <p>Price: £${property.price.toLocaleString()}</p>
                <p>Rental Income: £${property.rental_income.toLocaleString()}/year</p>
                <p>Yield: ${property.yield}%</p>`;
            resultsContainer.appendChild(propertyElement);
        });
    }

    // Display sold prices
    if (data.sold_prices.length > 0) {
        const soldHeader = document.createElement('h2');
        soldHeader.textContent = 'Sold Prices';
        resultsContainer.appendChild(soldHeader);

        data.sold_prices.forEach(property => {
            const propertyElement = document.createElement('div');
            propertyElement.className = 'property-item';
            propertyElement.innerHTML = `
                <h3>${property.title}</h3>
                <p>${property.description}</p>
                <p>Sold Price: £${property.price.toLocaleString()}</p>`;
            resultsContainer.appendChild(propertyElement);
        });
    }
}
