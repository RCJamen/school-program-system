$(document).ready(function() {
    $('.delete-student').click(function(event) {
        event.preventDefault();
        var studentID = $(this).data('studentid');
        var firstname = $(this).data('firstname');
        var lastname = $(this).data('lastname');
        var classrecordid = $(this).data('classrecordid');
        var csrfToken = $('meta[name=csrf-token]').attr('content');

        $('#askDelete .delete-modal-body').html(
            `<p>Do you want to delete the following Student?</p><strong>Student ID:</strong> ${studentID}
            <br><strong>Full name:</strong> ${firstname} ${lastname}`);

        $('#askDelete').modal('show');

        $('#askDelete .delete-button').off('click').on('click', function () {
            $.ajax({
                type: 'POST',
                url: `/${classrecordid}/delete_student/${studentID}`,
                headers: {
                    'X-CSRFToken': csrfToken
                },
                success: function (response) {
                    if (response.success) {
                        $(event.target).closest('tr').remove();
                        console.log('Student deleted successfully:', response);
                        flashMessage(response.flash_message.type, response.flash_message.message);
                        location.reload();
                    } else {
                        console.error('Error deleting Student:', response.error || 'Unknown error');
                        flashMessage('danger', response.error || 'Failed to delete Student');
                    }
                },
                error: function (error) {
                    console.error('Error deleting Student:', error);
                    flashMessage('danger', 'Failed to delete Student');
                }
            });
            $('#askDelete').modal('hide');
        });
    });

    function flashMessage(type, message) {
        var flashMessageHTML = `
            <div class="alert alert-${type} alert-dismissible fade show" role="alert">
                <div class="d-flex justify-content-between align-items-center">
                    <span>${message}</span>
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
            </div>
        `;
        $('#flash-messages-container').append(flashMessageHTML);
    }
});

$(document).ready(function() {
    $('.delete-assessment').click(function(event) {
        event.preventDefault();
        var assessmentname = $(this).data('assessmentname');
        var classrecordid = $(this).data('classrecordid');
        var csrfToken = $('meta[name=csrf-token]').attr('content');

        console.log(assessmentname)
        console.log(classrecordid)

        $('#askDeleteAssessment .delete-modal-body').html(
            `<p>Do you want to delete the following Assessment?</p><strong>Assessment Name:</strong> ${assessmentname}`);

        $('#askDeleteAssessment').modal('show');

        $('#askDeleteAssessment .delete-button').off('click').on('click', function () {
            $.ajax({
                type: 'POST',
                url: `/${classrecordid}/delete_grade_distribution/${assessmentname}`,
                headers: {
                    'X-CSRFToken': csrfToken
                },
                success: function (response) {
                    if (response.success) {
                        $(event.target).closest('tr').remove();
                        console.log('Assessment deleted successfully:', response);
                        flashMessage(response.flash_message.type, response.flash_message.message);
                        location.reload();
                    } else {
                        console.error('Error deleting Assessment:', response.error || 'Unknown error');
                        flashMessage('danger', response.error || 'Failed to delete Assessment');
                    }
                },
                error: function (error) {
                    console.error('Error deleting Assessment:', error);
                    flashMessage('danger', 'Failed to delete Assessment');
                }
            });
            $('#askDeleteAssessment').modal('hide');
        });
    });

    function flashMessage(type, message) {
        var flashMessageHTML = `
            <div class="alert alert-${type} alert-dismissible fade show" role="alert">
                <div class="d-flex justify-content-between align-items-center">
                    <span>${message}</span>
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
            </div>
        `;
        $('#flash-messages-container').append(flashMessageHTML);
    }
});

const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))

document.getElementById('downloadTemplateCR').addEventListener('click', function () {
    // Replace '/download/subject' with the route that serves the file in your Flask app
    var downloadRoute = '/download/classrecord';

    // Create an anchor element
    var anchor = document.createElement('a');
    anchor.href = downloadRoute;

    // Set the download attribute with the desired file name
    anchor.download = 'class-record.csv';

    // Append the anchor to the body
    document.body.appendChild(anchor);

    // Trigger a click event on the anchor
    anchor.click();

    // Remove the anchor from the body
    document.body.removeChild(anchor);
});

$(document).ready(function () {
    $('.addScore').click(function () {
        var studentID = $(this).data('studentid');
        var classrecordID = $(this).data('classrecordid');

        console.log(studentID);
        console.log(classrecordID);

        $.ajax({
            url: '/get_modal_data/' + classrecordID + '/' + studentID,
            type: 'GET',
            dataType: 'JSON',
            success: function (data) {
                console.log('Response from server:', data);

                $('#Assessment').empty();

                // Populate the Assessment dropdown
                $.each(data, function (index, item) {
                    $('#Assessment').append($('<option>', {
                        value: item[0], // assuming item[0] is the assessmentID
                        text: item[2] // assuming item[2] is the activityName
                    }));
                });

                // Trigger the change event on the Assessment dropdown to populate the initial activity list
                $('#Assessment').change();

                // Add an event listener for the change event on the Assessment dropdown
                $('#Assessment').change(function () {
                    var selectedAssessmentID = $(this).val();

                    // Clear existing activity list
                    $('#activityListPlaceholder').empty();

                    // Filter data based on the selected assessment
                    var filteredData = data.filter(function (item) {
                        return item[0] == selectedAssessmentID;
                    });

                    // Populate the activity list based on the filtered data
                    $.each(filteredData, function (index, item) {
                        var activityListItem = '<div class="row">' +
                            '<div class="col-8">' +
                            '<div class="form-group">' +
                            '<h3 class="form-control"><strong>' + item[2] + '</strong></h3>' +
                            '</div>' +
                            '</div>' +
                            '<div class="col-4">' +
                            '<div class="form-group">' +
                            '<div class="input-group">' +
                            '<input type="text" name="scorelimit" id="score" class="form-control" placeholder="Score" maxlength="3">' +
                            '<span class="input-group-text">/' + item[3] + '</span>' + // assuming item[3] is the scoreLimit
                            '</div>' +
                            '</div>' +
                            '</div>' +
                            '</div>';

                        $('#activityListPlaceholder').append(activityListItem);
                    });
                });
            },
            error: function (error) {
                console.log('Error fetching modal data:', error);
            }
        });
    });
});
