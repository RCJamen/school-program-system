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
        $('#askDelete .modal-body').html(`<p>Do you want to delete the following faculty?</p><strong>ID:</strong> ${facultyID}<br><strong>Name:</strong> ${facultyName}`);

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
