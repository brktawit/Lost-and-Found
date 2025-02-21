function deleteItem(itemId) {
    if (!confirm("Are you sure you want to delete this item?")) {
        return; // Stop if user cancels deletion
    }

    fetch(`/items/${itemId}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (!response.ok) {
            return response.text().then(text => {
                console.error("Server Response:", text);
                throw new Error("Failed to delete item.");
            });
        }
        return response.json();
    })
    .then(data => {
        alert(data.message);
        let row = document.querySelector(`tr[data-item-id='${itemId}']`);
        if (row) row.remove(); // Remove the row without reloading
    })
    .catch(error => {
        console.error('Error:', error);
        alert(`Failed to delete item: ${error.message}`);
    });
}
