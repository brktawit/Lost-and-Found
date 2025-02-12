// DELETE ITEM FUNCTION
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
            return response.json().then(data => {
                throw new Error(data.error || "Unknown error occurred");
            });
        }
        return response.json();
    })
    .then(data => {
        alert(data.message);
        document.querySelector(`tr[data-item-id='${itemId}']`).remove(); // Remove the row without reloading
    })
    .catch(error => {
        console.error('Error:', error);
        alert(`Failed to delete item: ${error.message}`);
    });
}