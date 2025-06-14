$(document).ready(function () {
    $("#courseForm").submit(function (event) {
        event.preventDefault();

        let formData = {
            course_code: $("#course-code").val(),
            course_name: $("#course-name").val(),
        };

        $.ajax({
            url: "/faculty/course-add",
            type: "POST",
            data: JSON.stringify(formData),
            contentType: "application/json",
            headers: { 'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val() },
            success: function (response) {
                showToast("Success", "Course added successfully!", "success");

                $("#course-code").val("");
                $("#course-name").val("");

                setTimeout(() => {
                    const addCourseModal = document.getElementById("add-course-modal");
                    const modalInstance = bootstrap.Modal.getInstance(addCourseModal);
                    if (modalInstance) {
                        modalInstance.hide();
                    }
                }, 1000);
            },
            error: function (xhr, status, err) {
                

                let errorMessage = "An unexpected error occurred.";

                if (xhr.responseJSON && xhr.responseJSON.error) {
                    errorMessage = xhr.responseJSON.error;
                }

                console.error("Error:", err);
                console.error("Error:", errorMessage);

                showToast("Error", errorMessage, "danger");
            }
        });
    });
});
