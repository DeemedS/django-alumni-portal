document.addEventListener("DOMContentLoaded", function () {
    document.addEventListener('click', function (e) {
        const btn = e.target.closest('.edit-section-btn-me');
        if (!btn) return;

        const sectionId = btn.dataset.id;
        const sectionCode = btn.dataset.code;

        document.getElementById('edit-section-id').value = sectionId;
        document.getElementById('edit-section-code').value = sectionCode;
    });

    const updateSectionBtn = document.querySelector(".update-section-btn");

    if (updateSectionBtn) {
        updateSectionBtn.addEventListener("click", async function () {
            const formData = {
                section_id: document.getElementById("edit-section-id").value.trim(),
                section_code: document.getElementById("edit-section-code").value.trim(),
            };

            const csrfToken = document.querySelector('input[name=csrfmiddlewaretoken]').value;

            if (formData.section_id && formData.section_code) {
                fetch(`/faculty/section-edit`, {
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
                    const editSectionModal = document.getElementById("edit-section-modal");
                    const modalInstance = bootstrap.Modal.getInstance(editSectionModal);
                    if (modalInstance) {
                        modalInstance.hide();
                    }
                    
                    if (data.success) {
                        showToast("Success", "Section updated successfully!", "success");

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
