$(document).ready(function () {
    $('#contactForm').on('submit', function (e) {
        e.preventDefault();

        const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]')?.value;
        let formData = new FormData(this);

        $.ajax({
            url: '/help-email/',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            headers: {
                'X-CSRFToken': csrfToken
            },
            success: function (response) {
                showToast("Success", "Message sent successfully!", "success");
                $('#contactForm')[0].reset();
            },
            error: function (xhr, status, error) {

                showToast("Error", error, "error");
            }
        });
    });
});