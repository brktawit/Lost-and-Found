function updateItem(itemId) {
    const itemName = prompt("Enter the new item name:");
    const description = prompt("Enter the new description:");
    

    if (!itemName || !description) {
        alert("All fields are required.");
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
        if (!response.ok) {
            return response.text().then(text => {
                console.error("Server Response:", text);
                throw new Error("Failed to update item.");
            });
        }
        return response.json();
    })
    .then(data => {
        alert("Item updated successfully!");
        
        // Update row in table without reloading
        let row = document.querySelector(`tr[data-item-id='${itemId}']`);
        row.cells[0].innerText = itemName;
        row.cells[1].innerText = description;

    })
    .catch(error => {
        console.error("Error:", error);
        alert(`Failed to update item: ${error.message}`);
    });
}
