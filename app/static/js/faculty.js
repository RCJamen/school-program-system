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

function goBack() {
    // You can use window.location.href to navigate to the /faculty route
    window.location.href = '/faculty';
}

var currentFacultyID = null;
var facultyName = null;
var isEditState = false;

function toggleFunctions(button) {
    if (isEditState) {
        showAcademicLoad(button);
    } else {
        editAcademicLoad(button);
    }
    isEditState = !isEditState;
}

function showAcademicLoad(button) {
    currentFacultyID = button.getAttribute('data-facultyid-academic');
    facultyName = button.getAttribute('data-academic-name');
    $("#academic-faculty-name").html("<strong>" + facultyName + "</strong>");
    $("#academic-faculty-id").text(currentFacultyID); // You can modify this part accordingly

    console.log('Faculty ID:', currentFacultyID);
    console.log('Faculty Name:', facultyName);

    $.ajax({
        url: "/faculty_data",
        method: "GET",
        data: { faculty_id: currentFacultyID },
        success: function (data) {
            var tbody = $('#academic-table-body');
            tbody.empty();

            for (var i = 0; i < data.length; i++) {
                var subject = data[i];
                var row = '<tr>' +
                    '<th scope="row">' + subject['Subject Code'] + '</th>' +
                    '<td>' + subject['Section ID'] + '</td>' +
                    '<td>' + subject['Description'] + '</td>' +
                    '<td>' + subject['Schedule'] + '</td>' +
                    '<td>' + subject['Credits'] + '</td>' +
                    '<td>' +
                    '<button type="button" class="btn btn-info classRecordBtn" style="color: white;">Class Record</button>' +
                    '</td>' +
                    '</tr>';

                tbody.append(row);
            }

            $('#academic-load').modal('show');
        },
        error: function (error) {
            console.error("Error fetching data:", error);
            console.log(data);
        }
    });
}

$('.academicEditBtn').on('click', function () {
    var button = $(this);
    toggleFunctions(button[0]);
    // Hide the button after the first click
    button.hide();
});

function editAcademicLoad(button) {
    console.log('Faculty ID:', currentFacultyID);

    $.ajax({
        url: "/faculty_data",
        method: "GET",
        data: { faculty_id: currentFacultyID },
        success: function (data) {
            var tbody = $('#academic-table-body');
            tbody.empty();

            for (var i = 0; i < data.length; i++) {
                var subject = data[i];
                var row = `
                    <tr>
                        <th scope="row">${subject['Subject Code']}</th>
                        <td>${subject['Section ID']}</td>
                        <td>${subject['Description']}</td>
                        <td>${subject['Schedule']}</td>
                        <td>${subject['Credits']}</td>
                        <td>
                            <button type="button" class="btn btn-warning editSchedule">
                                <i class="fa-solid fa-pen-to-square" style="color: #ffffff;"></i>
                            </button>
                            <button type="button" class="btn btn-danger addSchedule"
                                data-subject-code="${subject['Subject Code']}"
                                data-section-id="${subject['Section ID']}"
                                onclick="openSecondModal(this)">
                                <i class="fa-solid fa-calendar-plus" style="color: #ffffff;"></i>
                            </button>
                        </td>
                    </tr>
                `;
            
                tbody.append(row);
            }
            

            $('#academic-load').modal('show');
        },
        error: function (error) {
            console.error("Error fetching data:", error);
            console.log(data);
        }
    });
}

function openSecondModal(button) {
    // Create a new instance of the Bootstrap Modal for the second modal
    var secondModal = new bootstrap.Modal(document.getElementById('secondModal'), { backdrop: 'static' });
    var subjectCode = $(button).data('subject-code');
    var sectionID = $(button).data('section-id');

    // Use subjectCode and sectionID as needed in your function
    console.log('Subject Code:', subjectCode);
    console.log('Section ID:', sectionID);

    $("#subject-id").val(subjectCode);
    $("#section-id").val(sectionID);
    // Show the second modal
    secondModal.show();
    
}


$("#addScheduleForm").submit(function (e) {
    e.preventDefault();

    var subjectID = $("#subject-id").val();
    var sectionID = $("#section-id").val();
    var day = $("#day").val();
    var timeStart = $("#time-start").val();
    var timeEnd = $("#time-end").val();

    $.ajax({
        type: 'POST',
        url: '/faculty/add-schedule',
        data: {
            'subject-id': subjectID,
            'section-id': sectionID,
            'day': day,
            'time-start': timeStart,
            'time-end': timeEnd,
        },
        headers: {
            'X-CSRFToken': csrfToken
        },
        success: function (response) {
            console.log('Schedule added successfully:', response);
            // Handle success, e.g., display a success message
        },
        error: function (error) {
            // Handle error, e.g., display an error message
            console.error('Error adding schedule:', error);
        },
    });
});
