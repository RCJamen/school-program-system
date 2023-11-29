document.addEventListener("DOMContentLoaded", function () {
    // Fetch data from the server
    fetch('/class-record')
        .then(response => response.json())
        .then(data => {
            // Update the table with the fetched data
            // Implement the logic to update the table using JavaScript
        });
});
