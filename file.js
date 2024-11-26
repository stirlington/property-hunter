function searchProperties(event) {
    event.preventDefault(); // Prevent form submission

    const location = document.getElementById('search-location').value;
    const minPrice = document.getElementById('min-price').value;
    const maxPrice = document.getElementById('max-price').value;
    const bedrooms = document.getElementById('bedrooms').value;

    // Fetch properties based on all criteria
    const currentProperties = fetchCurrentProperties(location, minPrice, maxPrice, bedrooms);
    const soldPrices = fetchSoldPrices(location, minPrice, maxPrice, bedrooms);

    // Combine results
    const results = [...currentProperties, ...soldPrices];

    // Display results
    displayResults(results);
}

// New function to display results
function displayResults(results) {
    const resultsContainer = document.querySelector('.results-container');
    resultsContainer.innerHTML = ''; // Clear previous results

    results.forEach(property => {
        const propertyElement = document.createElement('div');
        propertyElement.className = 'property-item';
        propertyElement.innerHTML = `
            <h2>${property.title}</h2>
            <p>${property.description}</p>
            <p>Price: ${property.price}</p>
        `;
        resultsContainer.appendChild(propertyElement);
    });
}

function fetchCurrentProperties(location, minPrice, maxPrice, bedrooms) {
    // Implement your logic to fetch current properties based on the criteria
    // This is a placeholder for demonstration
    return [
        { title: "Current Property 1", description: "Description 1", price: "£300,000" },
        // Add more properties as needed
    ];
}

function fetchSoldPrices(location, minPrice, maxPrice, bedrooms) {
    // Implement your logic to fetch sold prices based on the criteria
    // This is a placeholder for demonstration
    return [
        { title: "Sold Property 1", description: "Description 2", price: "£250,000" },
        // Add more properties as needed
    ];
}

document.getElementById('property-search-form').addEventListener('submit', searchProperties);
