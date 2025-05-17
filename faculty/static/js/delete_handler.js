document.addEventListener("DOMContentLoaded", function () {
    let deleteItemId = null;
    let deleteItemType = null;

    document.querySelector("table").addEventListener("click", function (event) {
        const button = event.target.closest(".delete-item");
        if (!button) return;

        deleteItemId = button.getAttribute("data-id");
        deleteItemType = button.getAttribute("data-type");

        const deleteModal = document.getElementById("deleteModal");
        if (deleteModal) {
            deleteModal.setAttribute("data-id", deleteItemId);
            deleteModal.setAttribute("data-type", deleteItemType);
        }

        const deleteModalMessage = document.getElementById("deleteModalMessage");
        if (deleteModalMessage) {
            deleteModalMessage.textContent = `You're going to delete this ${deleteItemType}?`;
        }
    });

    const confirmDeleteBtn = document.querySelector(".confirm-delete-btn");
    if (confirmDeleteBtn) {
        confirmDeleteBtn.addEventListener("click", function () {
            const deleteModal = document.getElementById("deleteModal");
            if (deleteModal) {
                deleteItemId = deleteModal.getAttribute("data-id");
                deleteItemType = deleteModal.getAttribute("data-type");
            }

            if (deleteItemId && deleteItemType) {
                fetch(`/faculty/${deleteItemType}-delete/${deleteItemId}/`, {
                    method: "DELETE",
                    headers: {
                        'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()
                    },
                    credentials: "same-origin"
                })
                .then(response => response.json())
                .then(data => {
                    
                    const deleteModal = document.getElementById("deleteModal");
                    const modalInstance = bootstrap.Modal.getInstance(deleteModal);
                    if (modalInstance) {
                        modalInstance.hide();
                    }

                    if (data.success) {
                        const deleteButton = document.querySelector(`.delete-item[data-id="${deleteItemId}"][data-type="${deleteItemType}"]`);
                        const row = deleteButton ? deleteButton.closest("tr") : null;
                
                        console.log("Row to remove:", row);
                
                        if (row) {
                            row.remove();
                            showToast("Success", `Successfully Deleted ${deleteItemType}.`, "success");
                        } else {
                            console.warn(`Row for ID ${deleteItemId} and type ${deleteItemType} not found.`);
                        }
                    } else {
                        showToast("Delete Failed", data.message, "danger");
                    }
                })
                .catch(error => console.error("Error:", error));
            }
        });
    }
});
