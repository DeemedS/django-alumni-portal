$('#officials-form').on('submit', function (e) {
    e.preventDefault(); // Prevent default form submission

    const formData = new FormData(this);
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]')?.value;

    $.ajax({
        url: '/faculty/save-officials',
        type: 'POST',
        data: formData,
        processData: false, // Prevent jQuery from converting the FormData object into a query string
        contentType: false, // Let the browser set the correct Content-Type (multipart/form-data)
        headers: {
            'X-CSRFToken': csrfToken
        },
        success: function (response) {
            showToast("Success", `Successfully Updated the Officials.`, "success");
            setTimeout(function () {
                location.reload();
            }, 1000);
        },
        error: function (xhr, status, error) {
            showToast("Update Failed", `An error occurred while submitting the form.`, "danger");
            setTimeout(function () {
                location.reload();
            }, 1000);
            console.error(xhr.responseText);
        }
    });
});
