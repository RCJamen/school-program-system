$(document).ready(function () {
    $('.delete-subject').click(function (event) {
        event.preventDefault();
        var subjectCode = $(this).data('subject-code');
        var section = $(this).data('section');
        var handler = $(this).data('handler');
        var csrfToken = $('meta[name=csrf-token]').attr('content');

        // Update modal content with subject details
        $('#deleteSubjectModal .delete-modal-body').html(
            `<p>Do you want to delete the following Subject?</p><strong>Subject Code:</strong> ${subjectCode}
            <br><strong>Section:</strong> ${section} <br><strong>Handler:</strong> ${handler}`);

        // Show the modal
        $('#deleteSubjectModal').modal('show');

        // Handle "Yes" button click in the modal
        $('#deleteSubjectModal .delete-button').off('click').on('click', function () {
            // Send an AJAX request to delete subject
            $.ajax({
                type: 'POST',
                url: `/subjects/delete/${subjectCode}/${section}`,
                headers: {
                    'X-CSRFToken': csrfToken
                },
                success: function (response) {
                    if (response.success) {
                        // Handle success, e.g., refresh the page or update UI
                        $(event.target).closest('tr').remove();
                        console.log('Subject deleted successfully:', response);
                        // Add a flash message for successful deletion
                        flashMessage('success', `Subject deleted successfully - Subject Code: <strong>${subjectCode}</strong>, Section: <strong>${section}</strong>, Handler: <strong>${handler}</strong>`);
                    } else {
                        // Handle failure, e.g., display an error message
                        console.error('Error deleting subject:', response.message);
                        // Add a flash message for failed deletion
                        flashMessage('danger', response.message);
                    }
                },
                error: function (error) {
                    // Handle error, e.g., display an error message
                    console.error('Error deleting Subject:', error);
                    // Add a flash message for failed deletion
                    flashMessage('danger', 'Failed to delete subject');
                }
            });

            // Hide the modal after the "Yes" button is clicked
            $('#deleteSubjectModal').modal('hide');
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
