// Function to fetch data from the backend and populate the table
async function fetchDataAndPopulateTable() {
    try {
        const response = await fetch('/api/students');  // Assuming Flask route for getting students data
        const studentsData = await response.json();

        var tableBody = document.getElementById('dynamic-table').getElementsByTagName('tbody')[0];
        tableBody.innerHTML = '';  // Clear existing table rows

        studentsData.forEach(function(student, index) {
            var row = tableBody.insertRow(index);

            var cell1 = row.insertCell(0);
            cell1.textContent = index + 1;

            var cell2 = row.insertCell(1);
            cell2.textContent = student.studentId;

            var cell3 = row.insertCell(2);
            cell3.textContent = student.lastname;

            var cell4 = row.insertCell(3);
            cell4.textContent = student.firstname;

            // Add more cells/columns as needed
        });
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

// Call the function to fetch data and populate the table
fetchDataAndPopulateTable();
