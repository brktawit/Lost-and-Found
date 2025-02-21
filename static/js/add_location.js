// Ensure script runs only after the DOM is fully loaded
document.addEventListener("DOMContentLoaded", function () {
    console.log("✅ add_location.js loaded successfully!");

    // Ensure the map container exists
    let mapContainer = document.getElementById("map");
    if (!mapContainer) {
        console.error("❌ Error: Map container not found!");
        return;
    }

    // Initialize the map (Default: Lisbon, Portugal)
    let map = L.map("map").setView([38.7169, -9.1399], 6);

    // Add OpenStreetMap tiles
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: "&copy; OpenStreetMap contributors"
    }).addTo(map);

    console.log("✅ Map initialized successfully!");

    // Initialize marker
    let marker = null;

    // Function to update marker position
    function updateMarker(lat, lng) {
        if (marker) {
            marker.setLatLng([lat, lng]);
        } else {
            marker = L.marker([lat, lng]).addTo(map);
        }

        console.log(`📍 Marker updated to: Lat ${lat}, Lon ${lng}`);

        // Update hidden form fields
        let latInput = document.getElementById("latitude");
        let lonInput = document.getElementById("longitude");

        if (latInput && lonInput) {
            latInput.value = lat;
            lonInput.value = lng;
        } else {
            console.error("❌ Error: Latitude or Longitude input field not found!");
        }
    }

    // Handle map clicks (User selects a location)
    map.on("click", function (e) {
        updateMarker(e.latlng.lat, e.latlng.lng);
    });

    console.log("✅ Click event added to the map!");

    // Ensure the search input exists
    let searchInput = document.getElementById("searchInput");
    if (!searchInput) {
        console.error("❌ Error: Search input field not found!");
        return;
    }

    console.log("✅ Search input found!");

    // Handle location search using OpenStreetMap's Nominatim API
    searchInput.addEventListener("input", function () {
        let query = this.value.trim();
        if (query.length < 3) return; // Waits until user types at least 3 characters

        fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${query}`)
            .then(response => response.json())
            .then(data => {
                if (data.length > 0) {
                    let lat = parseFloat(data[0].lat);
                    let lon = parseFloat(data[0].lon);

                    console.log(`📍 Moving map to: Lat ${lat}, Lon ${lon}`);

                    // Ensure map is initialized before calling setView()
                    if (typeof map !== "undefined" && map !== null) {
                        map.setView([lat, lon], 12);
                        updateMarker(lat, lon);
                    } else {
                        console.error("❌ Error: Map object not initialized!");
                    }
                } else {
                    console.warn("⚠️ No location found");
                }
            })
            .catch(error => console.error("❌ Error fetching location:", error));
    });

    console.log("✅ Search functionality initialized!");
});
