   // Sample data for demonstration
   var studentsData = [
    { id: 1, studentId: '2019-2093', name: 'Jamen, Ramel Cary' },
    // Add more student data as needed
];

// Function to populate the table with dynamic data
function populateTable() {
    var tableBody = document.getElementById('dynamic-table').getElementsByTagName('tbody')[0];

    // Clear existing table rows
    tableBody.innerHTML = '';

    // Loop through the data and create table rows
    studentsData.forEach(function(student, index) {
        var row = tableBody.insertRow(index);

        var cell1 = row.insertCell(0);
        cell1.textContent = index + 1;

        var cell2 = row.insertCell(1);
        cell2.textContent = student.studentId;

        var cell3 = row.insertCell(2);
        cell3.textContent = student.name;

        // Add more cells/columns as needed
    });
}

// Call the function to initially populate the table
populateTable();