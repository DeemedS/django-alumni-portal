$(document).ready(function () {
    $('#contactForm').on('submit', function (e) {
        e.preventDefault();

        const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]')?.value;
        let formData = new FormData(this);
        const btnspinner = document.getElementById('btn-spinner');
        const spinner = document.getElementById('spinner-hide');
        btnspinner.classList.remove('d-none');
        spinner.classList.add('d-none');

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
                btnspinner.classList.add('d-none');
                spinner.classList.remove('d-none');

                $('#contactForm')[0].reset();
            },
            error: function (xhr, status, error) {
                let errorMsg = "An error occurred.";
                if (xhr.responseJSON && xhr.responseJSON.error) {
                    errorMsg = xhr.responseJSON.error;
                } else if (error) {
                    errorMsg = error;
                }
                showToast("Error", errorMsg, "danger");
                btnspinner.classList.add('d-none');
                spinner.classList.remove('d-none');
            }
        });
    });
});
