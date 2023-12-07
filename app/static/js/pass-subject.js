$(document).ready(function () {
    $(".class-record").click(function (event) {
        // Prevent the default behavior of the link
        event.preventDefault();

        // Get the data attributes from the clicked link
        var subjectCode = $(this).data("subject-code");
        var sectionCode = $(this).data("section-code");

        // Make an AJAX request to your Flask route with POST method
        $.ajax({
            url: "/class_record/" + subjectCode + "/" + sectionCode,
            type: "POST",  // Use POST method
            data: {},  // Add any data you want to send in the request body
            success: function (response) {
                // Handle the response, e.g., update the UI
                console.log(response);
            },
            error: function (error) {
                console.log(error);
            }
        });
    });
});