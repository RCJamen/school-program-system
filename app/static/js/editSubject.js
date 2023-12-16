$(document).ready(function () {
    $('.edit-subject').click(function () {
        var subjectCode = $(this).data('subject-code');
        var section = $(this).data('section');
        var description = $(this).data('description');
        var credits = $(this).data('credits');
        var handler = $(this).data('handler');

        $('#editCodeInput').val(subjectCode);
        $('#editCodeInputHidden').val(subjectCode);
        $('#editSectionInput').val(section);
        $('#editSectionInputHidden').val(section);
        $('#editDescriptionInput').val(description);
        $('#editCreditsInput').val(credits);
        $('#editHandlerInput').val(handler);

    });
});

document.getElementById('downloadTemplateSubject').addEventListener('click', function () {
    // Replace '/download/subject' with the route that serves the file in your Flask app
    var downloadRoute = '/download/subject';

    // Create an anchor element
    var anchor = document.createElement('a');
    anchor.href = downloadRoute;

    // Set the download attribute with the desired file name
    anchor.download = 'subject.csv';

    // Append the anchor to the body
    document.body.appendChild(anchor);

    // Trigger a click event on the anchor
    anchor.click();

    // Remove the anchor from the body
    document.body.removeChild(anchor);
});