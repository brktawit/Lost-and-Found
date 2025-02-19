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
        if (response.ok) {
            alert("item deleted successfully");
            location.reload(); // Reload the page to update the item list
        } else {
            response.json().then(data => alert(data.error));
        }
    })
    .catch(error => console.error('Error:', error));
}


