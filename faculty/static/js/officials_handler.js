$('#officials-form').on('submit', function (e) {
    e.preventDefault(); // Prevent the default form submission

    const formData = new FormData(this);
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]')?.value;

    $.ajax({
        url: '/faculty/save-officials',
        type: 'POST',
        data: formData,
        headers: {
            "X-CSRFToken": csrfToken,
        },
        processData: false, // Don't process files
        contentType: false, // Let the browser set this
        success: function (response) {
            alert('Form submitted successfully!');
        },
        error: function (xhr, status, error) {
            alert('An error occurred while submitting the form.');
            console.error(error);
        }
    });
});