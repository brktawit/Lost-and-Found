function updateCategory(categoryId) {
    const newCategoryName = document.getElementById(`update-category-${categoryId}`).value;

    if (!newCategoryName) {
        alert("Category name cannot be empty!");
        return;
    }

    fetch(`/categories/${categoryId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ category_name: newCategoryName }),
    })
    .then(response => {
        if (response.ok) {
            alert("Category updated successfully!");
            location.reload(); // Reload the page to reflect changes
        } else {
            response.json().then(data => alert(data.error));
        }
    })
    .catch(error => console.error('Error:', error));
}
