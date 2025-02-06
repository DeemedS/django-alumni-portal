document.addEventListener("DOMContentLoaded", function () {
    let formSelect = document.getElementById("form-select");
    let addFormButton = document.getElementById("add-form-button");
    let formContainer = document.getElementById("form-container");

    let formCounts = {
        bodytext: document.querySelector(`input[name="bodytext-INITIAL_FORMS"]`).value,
        bodyimage: document.querySelector(`input[name="bodyimage-INITIAL_FORMS"]`).value,
        subtitle: document.querySelector(`input[name="subtitle-INITIAL_FORMS"]`).value,
    };

    function updateManagementForm(prefix) {
        const totalFormsInput = document.querySelector(`input[name="${prefix}-TOTAL_FORMS"]`);
        totalFormsInput.value = formCounts[prefix];
    }

    addFormButton.addEventListener("click", function () {
        const selectedValue = formSelect.value;
        
        if (selectedValue) {
        const prefix = selectedValue;
        const formTemplate = document.getElementById(`${prefix}-template`);

            if (formTemplate) {
            formCounts[prefix]++;
            const formHtml = formTemplate.innerHTML.replace(
            /__prefix__/g,
            formCounts[prefix] - 1
            );
            formContainer.insertAdjacentHTML("beforeend", formHtml);
            updateManagementForm(prefix);
        }
        } else {
            showToast("Please Select a Form", "Select a form to add.", "warning");
        }
    });

    formContainer.addEventListener("click", function (event) {
        if (event.target.classList.contains("remove-form-button")) {
        const formGroup = event.target.closest(".formset-row");
        const deleteField = formGroup.querySelector('input[name$="-DELETE"]');

        if (deleteField) {
            console.log(deleteField);
            deleteField.checked = true;
            formGroup.style.display = "none";
        } else {
            formGroup.remove();
            const prefix = event.target
            .closest(".formset-row")
            .querySelector("input")
            .name.split("-")[0];
            formCounts[prefix]--;
            updateManagementForm(prefix);
        }
    }
    });
});
