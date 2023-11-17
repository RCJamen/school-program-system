// $(document).ready(function() {
//     $('.delete-faculty').click(function(event) {
//         event.preventDefault();
//         var facultyID = $(this).data('faculty-id');
//         var name = $(this).data('faculty-name')
//         var csrfToken = $('meta[name=csrf-token]').attr('content');

//         // Update modal content with faculty details
//         $('#askDelete .modal-body').html('<p>Do you want to delete the following faculty?</p>'+facultyID+name);

//         // Fetch faculty details using an AJAX request
//         $.ajax({
//             type: 'GET',
//             url: '/faculty/' + facultyID,  // Adjust the URL to your Flask route for fetching a single faculty
//             success: function(faculty) {

//                 $('#askDelete').modal('show');
//             },
//             error: function(error) {
//                 console.error('Error fetching faculty details:', error);
//             }
//         });

//         // Handle "Yes" button click in the modal
//         $('#askDelete .delete-button').off('click').on('click', function() {
//             // Send an AJAX request to delete faculty
//             $.ajax({
//                 type: 'DELETE',
//                 url: '/faculty/delete/' + facultyID,
//                 headers: {
//                     'X-CSRFToken': csrfToken
//                 },
//                 success: function(response) {
//                     // Handle success, e.g., refresh the page or update UI
//                     console.log('Faculty deleted successfully:', response);
//                 },
//                 error: function(error) {
//                     // Handle error, e.g., display an error message
//                     console.error('Error deleting faculty:', error);
//                 }
//             });

//             // Hide the modal after the "Yes" button is clicked
//             $('#askDelete').modal('hide');
//         });
//     });
// });

$(document).ready(function() {
    $('.delete-faculty').click(function(event) {
        event.preventDefault();
        var facultyID = $(this).data('faculty-id');
        var facultyName = $(this).data('faculty-name');
        var csrfToken = $('meta[name=csrf-token]').attr('content');

        // Update modal content with faculty details
        $('#askDelete .delete-modal-body').html(`<p>Do you want to delete the following faculty?</p><strong>ID:</strong> ${facultyID}<br><strong>Name:</strong> ${facultyName}`);

        // Show the modal
        $('#askDelete').modal('show');

        // Handle "Yes" button click in the modal
        $('#askDelete .delete-button').off('click').on('click', function() {
            // Send an AJAX request to delete faculty
            $.ajax({
                type: 'DELETE',
                url: `/faculty/delete/${facultyID}`,
                headers: {
                    'X-CSRFToken': csrfToken
                },
                success: function(response) {
                    if (response.success) {
                        // Handle success, e.g., refresh the page or update UI
                        $(event.target).closest('tr').remove();
                        console.log('Faculty deleted successfully:', response);
                        // Add a flash message for successful deletion
                        flashMessage('success', `Faculty deleted successfully - ID: <strong>${facultyID}</strong>, Name: <strong>${facultyName}</strong>`);
                    } else {
                        // Handle failure, e.g., display an error message
                        console.error('Error deleting faculty:', response.error);
                        // Add a flash message for failed deletion
                        flashMessage('danger', 'Failed to delete faculty');
                    }
                },
                error: function(error) {
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
        $('#flash-messages-container').append(flashMessageHTML);
    }

    
});


var csrfToken = $('meta[name=csrf-token]').attr('content');  // Move it outside the click event handler

$(".edit-faculty").click(function() {
    console.log("Update Faculty button clicked");
    var facultyID = $(this).data("faculty-edit-id");
    var facultyfirstName = $(this).data("faculty-edit-firstname");
    var facultylastName = $(this).data("faculty-edit-lastname");
    var facultyEmail = $(this).data("faculty-edit-email");

    console.log('Clicked Edit Faculty. ID:', facultyID, 'FirstName:', facultyfirstName, 'LastName:', facultylastName, 'Email:', facultyEmail);
    
    $("#editFacultyIDInput").val(facultyID);
    $("#editFacultyfirstName").val(facultyfirstName);
    $("#editFacultylastName").val(facultylastName);
    $("#editFacultyEmail").val(facultyEmail);
});

$("#editFacultyForm").submit(function(e) {
    e.preventDefault();

    var facultyID = $("#editFacultyIDInput").val();  // Retrieve the ID from the form
    var facultyfirstName = $("#editFacultyfirstName").val();
    var facultylastName = $("#editFacultylastName").val();
    var facultyEmail = $("#editFacultyEmail").val();

    $.ajax({
        type: 'POST',
        url: `/faculty/edit/${facultyID}`,
        data: {
            editFacultyIDInput: facultyID,  // Include the ID in the data
            editFacultyfirstName: facultyfirstName,
            editFacultylastName: facultylastName,
            editFacultyEmail: facultyEmail,
        },
        headers: {
            'X-CSRFToken': csrfToken
        },
        success: function(response) {
            console.log('Faculty Updated successfully:', response);
            editFlashMessage('success', `Faculty updated successfully - ID: <strong>${facultyID}</strong>`);
            
            // After the flash message is shown, redirect to the faculty page
            setTimeout(function() {
                editRedirect();
            }, 3000); // Adjust the timeout duration as needed
        },
        error: function(error) {
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
        $('#flash-messages-container').append(flashMessageHTML);
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
    button.addEventListener("click", ()=>{
        const edit_faculty_id = button.getAttribute('data-faculty-edit-id');
        const edit_faculty_firstname = button.getAttribute("data-faculty-edit-firstname");
        const edit_faculty_lastname = button.getAttribute("data-faculty-edit-lastname");
        const edit_faculty_email = button.getAttribute("data-faculty-edit-email");

        const id_input = document.getElementById("editFacultyIDInput");
        id_input.value = edit_faculty_id;

        const firstname_input = document.getElementById("editFacultyfirstName");
        firstname_input.value = edit_faculty_firstname;

        const lastname_input = document.getElementById("editFacultylastName");
        lastname_input.value = edit_faculty_lastname;

        const email_input = document.getElementById("editFacultyEmail");
        email_input.value = edit_faculty_email;
    });
});