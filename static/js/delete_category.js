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
        if (!response.ok) {
            return response.json().then(data => {
                throw new Error(data.error || "Unknown error occurred");
            });
        }
        return response.json();
    })
    .then(data => {
        alert(data.message);

        // Correctly selecting the category list item by ID
        const categoryElement = document.getElementById(`category-${categoryId}`);
        if (categoryElement) {
            categoryElement.remove();  // Remove category from the UI
        } else {
            console.warn(`Category ID ${categoryId} not found in the DOM.`);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert(`Failed to delete category: ${error.message}`);
    });
}
