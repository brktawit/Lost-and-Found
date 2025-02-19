function updateItem(itemId) {
    const itemName = prompt("Enter the new item name:");
    const description = prompt("Enter the new description:");

    if (!itemName || !description) {
        alert("Both fields are required.");
        return;
    }

    fetch(`/items/${itemId}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            item_name: itemName,
            description: description
        })
    })
    .then(response => {
        if (response.ok) {
            alert("Item updated successfully!");
            location.reload(); // Refresh the page to show the updated item
        } else {
            return response.json().then(data => alert(data.error));
        }
    })
    .catch(error => console.error("Error:", error));
}
