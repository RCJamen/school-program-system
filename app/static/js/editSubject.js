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