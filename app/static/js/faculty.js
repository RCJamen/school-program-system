
$(document).ready(function() {
    $('.delete-faculty').click(function(event) {
        event.preventDefault();
        var facultyID = $(this).data('faculty-id');
        var facultyName = $(this).data('faculty-name');
        var csrfToken = $('meta[name=csrf-token]').attr('content');

        // Update modal content with faculty details
        $('#askDelete .delete-modal-body').html(`<p>Do you want to delete the following faculty?</p><strong>ID:</strong> <em>${facultyID}</em><br><strong>Name:</strong> <em>${facultyName}</em>`);

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
    $("#academic-faculty-id").text(currentFacultyID);

    console.log('Faculty ID:', currentFacultyID);
    console.log('Faculty Name:', facultyName);

    $.ajax({
        url: "/faculty_data",
        method: "GET",
        data: { faculty_id: currentFacultyID },
        success: function (data) {
            console.log(data);
            var groupedSchedules = groupSchedules(data);

            var tbody = $('#academic-table-body');
            tbody.empty();

            for (var i = 0; i < groupedSchedules.length; i++) {
                var subject = groupedSchedules[i];
                var row = '<tr>' +
                    '<th scope="row">' + subject['Subject Code'] + '</th>' +
                    '<td>' + subject['Section ID'] + '</td>' +
                    '<td>' + subject['Description'] + '</td>' +
                    '<td>';

                // Iterate through the schedules for the current subject
                for (var j = 0; j < subject['Schedules'].length; j++) {
                    var schedule = subject['Schedules'][j];

                    if (schedule['Day'] === 'None') {
                        // Show "None" if the day is None
                        row += 'None<br>';
                    } else {
                        row += `${schedule['Day']} ${schedule['Time Start']} - ${schedule['Time End']}<br>`;
                    }
                }

                row += '</td>' +
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
        }
    });
}

// Helper function to group schedules by subject code and section ID
function groupSchedules(data) {
    var groupedSchedules = [];

    for (var i = 0; i < data.length; i++) {
        var schedule = data[i];
        var existingSubject = groupedSchedules.find(subject => subject['Subject Code'] === schedule['Subject Code'] && subject['Section ID'] === schedule['Section ID']);

        if (existingSubject) {
            // Subject already exists in the groupedSchedules array, add the schedule to its 'Schedules' array
            existingSubject['Schedules'].push({
                'Day': schedule['Schedule'].split(' ')[0], // Extract the day from the 'Schedule' field
                'Time Start': schedule['Schedule'].split(' ')[1],
                'Time End': schedule['Schedule'].split(' - ')[1]
            });
        } else {
            // Subject does not exist in the groupedSchedules array, create a new entry
            groupedSchedules.push({
                'Subject Code': schedule['Subject Code'],
                'Section ID': schedule['Section ID'],
                'Description': schedule['Description'],
                'Schedules': [{
                    'Day': schedule['Schedule'].split(' ')[0], // Extract the day from the 'Schedule' field
                    'Time Start': schedule['Schedule'].split(' ')[1],
                    'Time End': schedule['Schedule'].split(' - ')[1]
                }],
                'Credits': schedule['Credits']
            });
        }
    }

    return groupedSchedules;
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
                            <button type="button" class="btn btn-warning delete-schedule" data-schedule-id = "${subject['Schedule ID']}"
                            data-schedule = "${subject['Schedule']}" data-schedule-subject = "${subject['Subject Code']} ${subject['Section ID']}" onclick="openDeleteModal()" >
                                <i class="fa-solid fa-trash" style="color: #ffffff;"></i>
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

function formatTime(time) {
    // Check if time is defined
    if (time) {
        // Assuming time is in HH:mm:ss format
        const [hours, minutes] = time.split(':');
        return `${hours}:${minutes}`;
    } else {
        // Return a default value or handle it based on your requirements
        return 'N/A';
    }
}
// Assuming #academic-table-body is a static parent element



$(document).on('click', '#classSchedule-tab', function () {
    console.log(currentFacultyID);
    console.log("clicked");

    // Check if currentFacultyID is defined
    if (typeof currentFacultyID !== 'undefined') {
        $.ajax({
            url: "/faculty_schedule",
            method: "GET",
            data: { faculty_id: currentFacultyID },
            success: function (response) {
                if (response.success) {
                    var data = response.data;
                    console.log(data);

                    // Iterate through the days
                    var days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
                    days.forEach(function (day) {
                        var eventsGroup = $(`.events-group.${day}`);
                        
                        // Clear existing content inside the ul element
                        eventsGroup.find(`#schedule-${day.toLowerCase()}`).empty();

                        // Check if the schedule data for the current day is available
                        if (data[`${day.toLowerCase()}_schedule`]) {
                            // Iterate through the data for the current day and create list items
                            for (var i = 0; i < data[`${day.toLowerCase()}_schedule`].length; i++) {
                                var schedule = data[`${day.toLowerCase()}_schedule`][i];
                                var formattedStartTime = formatTime(schedule.time_start);
                                var formattedEndTime = formatTime(schedule.time_end);

                                var listItem = `
                                    <li class="single-event" data-start="${formattedStartTime}" data-end="${formattedEndTime}" data-event="event-${(i % 4) + 1}">
                                        <a href="#0">
                                            <em class="event-name">${schedule.subjectID} ${schedule.sectionID}</em>
                                        </a>
                                    </li>`;

                                // Append the new list item to the ul element
                                eventsGroup.find(`#schedule-${day.toLowerCase()}`).append(listItem);

                                console.log(formattedStartTime, formattedEndTime, schedule.subjectID, schedule.sectionID);
                            }
                        }
                    });

                    // After updating the schedule data, reinitialize the schedule events
                    // and recalculate their placements by calling the appropriate functions
                    $.getScript("../static/js/schedule.js", function () {
                        console.log("schedule.js loaded");
                    });

                } else {
                    console.error("Error fetching data:", response.error);
                }
            },
            error: function (error) {
                console.error("Error fetching data:", error);
            }
        });
    } else {
        console.error("currentFacultyID is not defined");
    }
});



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

function openDeleteModal() {
    var deleteModal = new bootstrap.Modal(document.getElementById('deleteSchedule'), { backdrop: 'static' });
    deleteModal.show();
    console.log("clicked");
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
            if (response.success) {
                console.log('Schedule added successfully:', response);
                editAcademicLoad({ getAttribute: function () { return currentFacultyID; } });
                scheduleFlashMessage("success", `Schedule Added Successfully: ${subjectID} - ${sectionID} <strong>(${day} ${timeStart} - ${timeEnd})</strong>`);
            } else {
                scheduleFlashMessage("danger", "Failed to add schedule: it already exists");
            }
        },
        error: function (error) {
            // Handle error, e.g., display an error message
            console.error('Error adding schedule:', error);
        },
    });
    function scheduleFlashMessage(type, message) {
        // Create flash message HTML
        var flashMessageAcademic = `
            <div class="alert alert-${type} alert-dismissible fade show" role="alert">
                <div class="d-flex justify-content-between align-items-center">
                    <span>${message}</span>
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
            </div>
        `;

        // Append flash message HTML to a container (adjust the selector accordingly)
        $('#academic-flash-container').append(flashMessageAcademic);
    }
});


$('#academic-table-body').on('click', '.delete-schedule', function (event) {
    event.preventDefault();
    var scheduleId = $(this).data('schedule-id');
    var schedule = $(this).data('schedule');
    var classhandled = $(this).data('schedule-subject');
    
    // Perform your delete logic here or trigger another function
    console.log('Delete Schedule ID:', scheduleId);
    console.log('Schedule:', schedule);
    console.log('subject:', classhandled);

    $('#deleteSchedule .delete-schedule-modal-body').html(`<p>Do you want to delete the following Schedule?</p><strong>Class Handled:</strong> <em>${classhandled}</em><br><strong>Schedule:</strong> <em>${schedule}</em>`);

    // // Show the modal
    $('#deleteSchedule').modal('show');

    $('#deleteSchedule .delete-schedule-button').off('click').on('click', function() {
         // Send an AJAX request to delete faculty
         $.ajax({
            type: 'DELETE',
            url: `/faculty/delete-schedule/${scheduleId}`,
            headers: {
                'X-CSRFToken': csrfToken
            },
            success: function(response) {
                console.log('Response:', response);
        
                if (response.success) {
                    editAcademicLoad({ getAttribute: function () { return currentFacultyID; } });
                    console.log('Schedule deleted successfully:', response);
                    deleteScheduleFM("success", `Schedule Deleted Successfully: <strong>Class Handled:</strong> <em>${classhandled}</em><br><strong>Schedule:</strong> <em>${schedule}</em>`);
                } else {
                    // Handle failure
                    console.error('Error Schedule faculty:', response.error);
                    deleteScheduleFM("success", `Schedule Added Successfully: <strong>Class Handled:</strong> <em>${classhandled}</em><br><strong>Schedule:</strong> <em>${schedule}</em>`);
                }
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.error('AJAX Error:', textStatus, errorThrown);
            }
        });
        

        // Hide the modal after the "Yes" button is clicked
        $('#deleteSchedule').modal('hide');
    });

    function deleteScheduleFM(type, message) {
        // Create flash message HTML
        var deleteScheduleFM = `
            <div class="alert alert-${type} alert-dismissible fade show" role="alert">
                <div class="d-flex justify-content-between align-items-center">
                    <span>${message}</span>
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
            </div>
        `;

        // Append flash message HTML to a container (adjust the selector accordingly)
        $('#academic-flash-container').append(deleteScheduleFM);
    }
});

