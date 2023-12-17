
$(document).ready(function () {
    $('.delete-faculty').click(function (event) {
        event.preventDefault();
        var facultyID = $(this).data('faculty-id');
        var facultyName = $(this).data('faculty-name');
        var csrfToken = $('meta[name=csrf-token]').attr('content');

        // Update modal content with faculty details
        $('#askDelete .delete-modal-body').html(`<p>Do you want to delete the following faculty?</p><strong>ID:</strong> <em>${facultyID}</em><br><strong>Name:</strong> <em>${facultyName}</em>`);

        // Show the modal
        $('#askDelete').modal('show');

        // Handle "Yes" button click in the modal
        $('#askDelete .delete-button').off('click').on('click', function () {
            // Send an AJAX request to delete faculty
            $.ajax({
                type: 'DELETE',
                url: `/faculty/delete/${facultyID}`,
                headers: {
                    'X-CSRFToken': csrfToken
                },
                success: function (response) {
                    if (response.success) {
                        // Handle success, e.g., refresh the page or update UI
                        $(event.target).closest('tr').remove();
                        console.log('Faculty deleted successfully:', response);
                        // Add a flash message for successful deletion
                        flashMessage('success', `Faculty deleted successfully`);
                    } else {
                        // Handle failure, e.g., display an error message
                        console.error('Error deleting faculty:', response.error);
                        // Add a flash message for failed deletion
                        flashMessage('danger', 'Failed to delete faculty');
                    }
                },
                error: function (error) {
                    // Handle error, e.g., display an error message
                    console.error('Error deleting faculty:', error);
                    // Add a flash message for failed deletion
                    flashMessage('danger', 'Failed to delete faculty');
                }
            });

            // Hide the modal after the "Yes" button is clicked
            $('#askDelete').modal('hide');
        });
    });

    function flashMessage(type, message) {
        // Create flash message HTML
        var flashMessageHTML = `
            <div class="alert alert-${type} alert-dismissible fade show" role="alert">
                <div class="d-flex justify-content-between align-items-center">
                    <span>${message}</span>
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
            </div>
        `;

        // Append flash message HTML to a container (adjust the selector accordingly)
        $('#message').append(flashMessageHTML);
    }


});



var csrfToken = $('meta[name=csrf-token]').attr('content');  // Move it outside the click event handler

$(".edit-faculty").click(function () {
    console.log("Update Faculty button clicked");
    var facultyID = $(this).data("faculty-edit-id");
    var facultyfirstName = $(this).data("faculty-edit-firstname");
    var facultylastName = $(this).data("faculty-edit-lastname");
    var facultyEmail = $(this).data("faculty-edit-email");
    var facultyRole = $(this).data("faculty-edit-role");

    console.log('Clicked Edit Faculty. ID:', facultyID, 'FirstName:', facultyfirstName, 'LastName:', facultylastName, 'Email:', facultyEmail, 'Role:', facultyRole);

    $("#editFacultyIDInput").val(facultyID);
    $("#editFacultyfirstName").val(facultyfirstName);
    $("#editFacultylastName").val(facultylastName);
    $("#editFacultyEmail").val(facultyEmail);
    $("#editFacultyRole").val(facultyRole);
});



$("#editFacultyForm").submit(function (e) {
    e.preventDefault();

    var facultyID = $("#editFacultyIDInput").val();  // Retrieve the ID from the form
    var facultyfirstName = $("#editFacultyfirstName").val();
    var facultylastName = $("#editFacultylastName").val();
    var facultyEmail = $("#editFacultyEmail").val();
    var facultyRole = $("#editFacultyRole").val();

    $.ajax({
        type: 'POST',
        url: `/faculty/edit/${facultyID}`,
        data: {
            editFacultyIDInput: facultyID,  // Include the ID in the data
            editFacultyfirstName: facultyfirstName,
            editFacultylastName: facultylastName,
            editFacultyEmail: facultyEmail,
            editFacultyRole: facultyRole,
        },
        headers: {
            'X-CSRFToken': csrfToken
        },
        success: function (response) {
            console.log('Faculty Updated successfully:', response);
            editFlashMessage('success', `Faculty updated successfully - ID: <strong>${facultyID}</strong>`);
            const row = document.querySelector(`#faculty-row-${facultyID}`)
            console.log(row)
            row.querySelector("#faculty-firstname").textContent = facultyfirstName
            row.querySelector("#faculty-lastname").textContent = facultylastName
            row.querySelector("#faculty-email").textContent = facultyEmail
            row.querySelector("#faculty-role").textContent = facultyRole
        },
        error: function (error) {
            // Handle error, e.g., display an error message
            console.error('Error Updating faculty:', error);
        },
    });

    function editFlashMessage(type, message) {
        // Create flash message HTML
        var flashMessageHTML = `
            <div class="alert alert-${type} alert-dismissible fade show" role="alert">
                <div class="d-flex justify-content-between align-items-center">
                    <span>${message}</span>
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
            </div>
        `;

        // Append flash message HTML to a container (adjust the selector accordingly)
        $('#message').append(flashMessageHTML);
    }

});

function editRedirect() {
    function redirectToFaculty() {
        window.location.href = '/faculty';
    }

    // Trigger the flash message after the redirection
    redirectToFaculty();
}


const editFacultyBtn = document.querySelectorAll('.edit-faculty');
editFacultyBtn.forEach(button => {
    button.addEventListener("click", () => {
        const edit_faculty_id = button.getAttribute('data-faculty-edit-id');
        const edit_faculty_firstname = button.getAttribute("data-faculty-edit-firstname");
        const edit_faculty_lastname = button.getAttribute("data-faculty-edit-lastname");
        const edit_faculty_email = button.getAttribute("data-faculty-edit-email");
        const edit_faculty_role = button.getAttribute("data-faculty-edit-role");

        const id_input = document.getElementById("editFacultyIDInput");
        id_input.value = edit_faculty_id;

        const firstname_input = document.getElementById("editFacultyfirstName");
        firstname_input.value = edit_faculty_firstname;

        const lastname_input = document.getElementById("editFacultylastName");
        lastname_input.value = edit_faculty_lastname;

        const email_input = document.getElementById("editFacultyEmail");
        email_input.value = edit_faculty_email;

        const role_input = document.getElementById("editFacultyRole");
        role_input.value = edit_faculty_role;
    });
});

function goBack() {
    // You can use window.location.href to navigate to the /faculty route
    window.location.href = '/faculty';
}




function showAcademicLoad(button) {
    currentFacultyID = button.getAttribute('data-facultyid-academic');
    facultyName = button.getAttribute('data-academic-name');
    $("#academic-faculty-name").html(facultyName);
    $("#academic-faculty-id").text(currentFacultyID);

    console.log('Faculty ID:', currentFacultyID);
    console.log('Faculty Name:', facultyName);

    $.ajax({
        url: "/faculty_data",
        method: "GET",
        data: { faculty_id: currentFacultyID },
        success: function (data) {
            console.log(data);
            var tbody = $('#academic-table-body');
            tbody.empty();

            var totalCredits = 0;

            for (var i = 0; i < data.length; i++) {
                var subject = data[i];
                var row = '<tr>' +
                    '<th scope="row">' + subject['Subject Code'] + '</th>' +
                    '<td>' + subject['Section ID'] + '</td>' +
                    '<td>' + subject['Description'] + '</td>' +
                    '<td>' + subject['Credits'] + '</td>' +
                    '</tr>';

                totalCredits += parseInt(subject['Credits']);
                tbody.append(row);
            }

            // Add a row for the total credits
            var totalRow = '<tr>' +
                '<th scope="row"><strong>Total Credits:</strong></th>' +
                '<td></td>' +
                '<td></td>' +
                '<td><strong>' + totalCredits + '</strong></td>' +
                '</tr>';

            tbody.append(totalRow);

            $('#academic-load').modal('show');
        },
        error: function (error) {
            console.error("Error fetching data:", error);
        }
    });
}


