$(document).ready(function () {
    $("#submit-course-btn").on("click", function (event) {
        event.preventDefault();


        let formData = {
            course_code: document.getElementById("course-code").value.trim(),
            course_name: document.getElementById("course-name").value.trim(),
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
                
                location.reload();
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

