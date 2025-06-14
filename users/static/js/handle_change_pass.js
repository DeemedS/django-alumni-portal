document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("changePassForm").addEventListener("submit", async function (e) {
        e.preventDefault();

        const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

        const current_password = document.getElementById("current_password").value;
        const new_password = document.getElementById("new_password").value;
        const confirm_new_password = document.getElementById("confirm_new_password").value;

        let formData = {
            current_password: current_password,
            new_password: new_password,
            confirm_new_password: confirm_new_password,
        }

        $.ajax({
            url: `/myaccount/change-password/`,
            type: "POST",
            data: JSON.stringify(formData),
            contentType: "application/json",
            headers: { "X-CSRFToken": csrfToken },
            success: function (response) {
                showToast("Success", "Successfully Change Password.", "success");
                setTimeout(function () {
                location.reload();
                }, 1000);
            },
            error: function (xhr, status, err) {
                

                let errorMessage = "An unexpected error occurred.";

                if (xhr.responseJSON && xhr.responseJSON.error) {
                    errorMessage = xhr.responseJSON.error;
                }

                $("#btn-spinner").addClass("d-none");
                $("#form-submit").prop("disabled", false);

                console.error("Error:", err);
                console.error("Error:", errorMessage);

                showToast("Error", errorMessage, "danger");
            }
        });

    });
});
