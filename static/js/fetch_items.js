let currentPage = 1;
const limit = 10; // Number of items per page
let map;
let marker;


// Fetch items with pagination, category filtering & search
function fetchItems(page = 1, searchQuery = "") {
    let selectedCategory = document.getElementById("categoryFilter")?.value || "all"; // Get selected category
    let apiUrl = `/items?page=${page}&limit=${limit}`;

    // ✅ Append category filter if it's not "all"
    if (selectedCategory !== "all") {
        apiUrl += `&category=${encodeURIComponent(selectedCategory)}`;
    }

    // ✅ Append search query if provided
    if (searchQuery.trim() !== "") {
        apiUrl += `&search=${encodeURIComponent(searchQuery)}`;
    }

    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            console.log("API Response:", data);  
            if (!Array.isArray(data.items)) {
                throw new Error("Expected an array but got: " + JSON.stringify(data.items));
            }
            currentPage = data.page;
            displayItems(data.items);
            updatePaginationControls(data.page, data.total_pages);
        })
        .catch(error => console.error("Error fetching items:", error));
}

// Search function to filter items in real-time
function searchItems() {
    let query = document.getElementById("searchInput").value.trim().toLowerCase();
    fetchItems(1, query); // Call fetchItems() with search query
}

// Display items in the table
function displayItems(items) {
    const tableBody = document.getElementById("items-table");
    const noItemsMessage = document.getElementById("no-items-message");

    tableBody.innerHTML = ""; // Clear previous items

    if (!items || items.length === 0) {
        if (noItemsMessage) {
            noItemsMessage.classList.remove("d-none"); // Show the "No items found" message
        }
        return;
    }

    if (noItemsMessage) {
        noItemsMessage.classList.add("d-none"); // Hide message if items exist
    }

    items.forEach(item => {
        const row = document.createElement("tr");
        row.setAttribute("data-item-id", item.item_id);

        let actionButtons = "";
        const userRole = sessionStorage.getItem("user_role"); // Get user role from session
        const userId = sessionStorage.getItem("user_id"); // ✅ Get logged-in user ID

        // ✅ Admins can edit/delete ALL items, including those with source = "admin"
        if (userRole === "admin") {
            actionButtons = `
                <a href="#" onclick="updateItem(${item.item_id})" class="text-warning text-decoration-none mx-2" title="Update">
                    ✏️
                </a>
                 <a href="#" onclick="deleteItem(${item.item_id})" class="text-danger text-decoration-none" title="Delete">
                    🗑️
                </a>
            `;
        }
        // ✅ Regular users can edit/delete only their own items, but NOT items from `source="admin"`
        else if (item.user_id == userId && item.source !== "admin") {
            actionButtons = `
                 <a href="#" onclick="updateItem(${item.item_id})" class="text-warning text-decoration-none mx-2" title="Update">
                    ✏️
                </a>
                 <a href="#" onclick="deleteItem(${item.item_id})" class="text-danger text-decoration-none" title="Delete">
                    🗑️
                </a>
            `;
        }

        row.innerHTML = `
            <td>${item.item_name}</td>
            <td>${item.description}</td>
            <td>${item.category_name}</td>
            <td>${item.place}</td>
            <td>${item.source}</td>
            <td class="text-nowrap">
                <a href="#" onclick="showLocation(${item.latitude}, ${item.longitude}); return false;" class="text-decoration-none">
                    📍 View Location
                </a>
            </td>
            <td class="text-center">
                 ${actionButtons}  <!-- ✅ Show buttons only if allowed -->
            </td>
        `;

        tableBody.appendChild(row);
    });
}

// Initialize Leaflet Map
document.addEventListener("DOMContentLoaded", function() {
    map = L.map("map").setView([38.7169, -9.1399], 6); // Default center (Lisbon, Portugal)
    
    // Add OpenStreetMap tile layer
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    fetchItems(); // Fetch items when page loads
});

// Show map & focus on clicked location
function showLocation(lat, lon) {
    const mapContainer = document.getElementById("map-container");

    // Check if the map container exists
    if (!mapContainer) {
        console.error("❌ Error: Map container not found!");
        return;
    }

    // Make the map visible
    mapContainer.style.display = "block";

       // ✅ Ensure Leaflet refreshes the map
       setTimeout(() => {
        map.invalidateSize();
    }, 100);

    // Scroll to the map smoothly
    mapContainer.scrollIntoView({ behavior: "smooth" });

    // Remove previous marker if exists
    if (marker) {
        map.removeLayer(marker);
    }

 // Add new marker
 marker = L.marker([lat, lon]).addTo(map)
 .bindPopup(`<b>Selected Location</b><br>Latitude: ${lat}<br>Longitude: ${lon}`)
 .openPopup();

// Center map on selected location
map.setView([lat, lon], 12);
}


// Update pagination controls
function updatePaginationControls(current, totalPages) {
    const paginationDiv = document.getElementById("pagination");
    paginationDiv.innerHTML = `
        <button onclick="prevPage()" ${current === 1 ? "disabled" : ""}>Previous</button>
        <span> Page ${current} of ${totalPages} </span>
        <button onclick="nextPage(${totalPages})" ${current === totalPages ? "disabled" : ""}>Next</button>
    `;
}



// Handle previous and next page
function nextPage(totalPages) {
    if (currentPage < totalPages) {
        fetchItems(currentPage + 1);
    }
}

function prevPage() {
    if (currentPage > 1) {
        fetchItems(currentPage - 1);
    }
}


// Location Formatter Script
document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll("tr[data-item-id]").forEach(row => {
        let itemId = row.getAttribute("data-item-id");
        let rawLocation = row.querySelector("td:nth-child(4)").innerText; // Get raw WKT
        let formattedLocation = convertWKTtoLatLon(rawLocation);
        document.getElementById(`location-${itemId}`).innerText = formattedLocation;
    });
});


// Convert WKT location to Lat/Lon
function convertWKTtoLatLon(wkt) {
    if (!wkt || typeof wkt !== "string") {
        return "Unknown"; // Handle null, undefined, or non-string values
    }
    if (!wkt.startsWith("POINT")) {
        return "Invalid Format"; // If it's a string but not WKT
    }
    let coords = wkt.replace("POINT(", "").replace(")", "").split(" ");
    return `Lat: ${parseFloat(coords[1])}, Lon: ${parseFloat(coords[0])}`;
}

// Fetch first page on load
document.addEventListener("DOMContentLoaded", () => fetchItems());

// ✅ Add event listener to fetch filtered items when category changes
document.getElementById("categoryFilter")?.addEventListener("change", () => fetchItems(1)); 



