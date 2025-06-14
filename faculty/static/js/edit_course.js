document.addEventListener("DOMContentLoaded", function () {
    document.addEventListener('click', function (e) {
        const btn = e.target.closest('.edit-course-btn-me');
        if (!btn) return;

        const courseId = btn.dataset.id;
        const courseName = btn.dataset.name;
        const courseCode = btn.dataset.code;

        document.getElementById('edit-course-id').value = courseId;
        document.getElementById('edit-course-name').value = courseName;
        document.getElementById('edit-course-code').value = courseCode;
    });

    const updateCourseBtn = document.querySelector(".update-course-btn");

    if (updateCourseBtn) {
        updateCourseBtn.addEventListener("click", async function () {
            const formData = {
                course_id: document.getElementById("edit-course-id").value.trim(),
                course_code: document.getElementById("edit-course-code").value.trim(),
                course_name: document.getElementById("edit-course-name").value.trim(),
            };

            const csrfToken = document.querySelector('input[name=csrfmiddlewaretoken]').value;

            if (formData.course_id && formData.course_code && formData.course_name) {
                fetch(`/faculty/course-edit`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": csrfToken,
                    },
                    body: JSON.stringify(formData),
                    credentials: "same-origin"
                })
                .then(response => response.json())
                .then(data => {
                    const editCourseModal = document.getElementById("edit-course-modal");
                    const modalInstance = bootstrap.Modal.getInstance(editCourseModal);
                    if (modalInstance) {
                        modalInstance.hide();
                    }
                    
                    if (data.success) {
                        showToast("Success", "Course updated successfully!", "success");

                        setTimeout(() => {
                            location.reload();
                        }, 1000);
                    } else {
                        showToast("Update Failed", data.message || "Something went wrong.", "danger");
                    }
                })
                .catch(error => {
                    console.error("Error:", error);
                    showToast("Error", "Something went wrong.", "danger");
                });
            } else {
                showToast("Validation Error", "All fields are required.", "warning");
            }
        });
    }
});
