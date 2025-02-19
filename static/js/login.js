document.getElementById("loginForm").addEventListener("submit", async function (e) {
    e.preventDefault(); // Prevent the default form submission

    // Gather form data
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    // Send POST request to the backend
    try {
        const response = await fetch("/login/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ username, password }),
        });

        const result = await response.json();

        if (response.ok) {
            alert(result.message); // Success message
            window.location.href = "/"; // Redirect to home page
        } else {
            alert(result.error); // Show error message
        }
    } catch (err) {
        console.error("Error:", err);
        alert("An error occurred. Please try again.");
    }
});
