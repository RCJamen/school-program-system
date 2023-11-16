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


        // Fetch faculty details using an AJAX request (optional)
        // You can include this part if you need to fetch additional details from the server

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
                    // Handle success, e.g., refresh the page or update UI
                    $(event.target).closest('tr').remove();
                    console.log('Faculty deleted successfully:', response);
                },
                error: function(error) {
                    // Handle error, e.g., display an error message
                    console.error('Error deleting faculty:', error);
                }
            });

            // Hide the modal after the "Yes" button is clicked
            $('#askDelete').modal('hide');
        });
    });
});

var csrfToken = $('meta[name=csrf-token]').attr('content');  // Move it outside the click event handler

$(".edit-faculty").click(function() {
    console.log("Update Faculty button clicked");
    var facultyID = $(this).data("faculty-edit-id");
    var facultyfirstName = $(this).data("faculty-edit-firstname");
    var facultylastName = $(this).data("faculty-edit-lastname");
    var facultyEmail = $(this).data("faculty-edit-email");

    console.log('Clicked Edit Faculty. ID:', facultyID, 'FirstName:', facultyfirstName, 'LastName:', facultylastName, 'Email:', facultyEmail);
    
    // Set the form fields with the retrieved data
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

    // Perform your own custom validation if needed

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
            // Handle success, e.g., refresh the page or update UI
            window.location.reload();
            console.log('Faculty Updated successfully:', response);
        },
        error: function(error) {
            // Handle error, e.g., display an error message
            console.error('Error Updating faculty:', error);
        },
    });
});


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