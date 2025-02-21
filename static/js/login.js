document.getElementById("loginForm").addEventListener("submit", async function (e) {
    e.preventDefault(); // Prevent default form submission

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
        console.log("🔹 Login Response:", result); // ✅ Debugging

        if (response.ok) {
            alert(result.message); // Success message

            // ✅ Store user role & ID in sessionStorage
            sessionStorage.setItem("user_role", result.role);
            sessionStorage.setItem("user_id", result.user_id);

            console.log("✅ Stored in sessionStorage:", {
                role: sessionStorage.getItem("user_role"),
                user_id: sessionStorage.getItem("user_id")
            });

            // Redirect to the correct page based on role
            window.location.href = result.redirect || "/";  // ✅ Default redirect to home
            
        } else {
            alert(result.error); // Show error message
        }
    } catch (err) {
        console.error("❌ Login error:", err);
        alert("An error occurred. Please try again.");
    }
});
