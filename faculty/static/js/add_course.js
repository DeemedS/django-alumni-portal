$(document).ready(function () {
    $("#careerForm").submit(function (event) {
        event.preventDefault();

        let formData = {
            title: $("#title").val(),
            company: $("#company").val(),
            company_email: $("#company_email").val(),
        };

        $.ajax({
            url: "/faculty/career-add",
            type: "POST",
            data: JSON.stringify(formData),
            contentType: "application/json",
            headers: { 'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val() },
            success: function (response) {

                // Redirect to the career edit page
                if (response.redirect_url) {
                    window.location.href = response.redirect_url;
                }
            },
            error: function (xhr, status, error) {
                console.error("Error:", error);
                showToast("Error", "Error submitting the form!", "danger");
            }
        });
    });
});
