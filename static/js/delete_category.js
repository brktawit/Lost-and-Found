function deleteCategory(categoryId) {
    if (!confirm("Are you sure you want to delete this category?")) {
        return; // Stop if the user cancels the confirmation
    }

    fetch(`/categories/${categoryId}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (response.ok) {
            alert("Category deleted successfully");
            location.reload(); // Reload the page to update the category list
        } else {
            response.json().then(data => alert(data.error));
        }
    })
    .catch(error => console.error('Error:', error));
}
