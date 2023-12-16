$(document).ready(function() {
    $('.delete-student').click(function(event) {
        event.preventDefault();
        var studentID = $(this).data('studentid');
        var firstname = $(this).data('firstname');
        var lastname = $(this).data('lastname');
        var csrfToken = $('meta[name=csrf-token]').attr('content');

        console.log(studentID)
        console.log(firstname)
        console.log(lastname)
        console.log(csrfToken)

        $('#askDelete .delete-modal-body').html(
            `<p>Do you want to delete the following Student?</p><strong>Student ID:</strong> ${studentID}
            <br><strong>Full name:</strong> ${firstname} ${lastname}`);

        $('#askDelete').modal('show');

        $('#askDelete .delete-button').off('click').on('click', function () {
            $.ajax({
                type: 'POST',
                url: `/class_record/delete_student/${studentID}`,
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
        var assessmentid = $(this).data('assessmentid');
        var name = $(this).data('name');
        var csrfToken = $('meta[name=csrf-token]').attr('content');

        console.log(assessmentid)
        console.log(name)
        $('#askDeleteAssessment .delete-modal-body').html(
            `<p>Do you want to delete the following Assessment?</p><strong>Assessment Name:</strong> ${name}`);

        $('#askDeleteAssessment').modal('show');

        $('#askDeleteAssessment .delete-button').off('click').on('click', function () {
            $.ajax({
                type: 'POST',
                url: `/grade_distribution/delete_assessment/${assessmentid}/${name}`,
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