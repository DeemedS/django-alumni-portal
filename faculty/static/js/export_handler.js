document.getElementById("export-btn").addEventListener("click", function () {
    const exportBtn = this;
    const exportingText = document.getElementById("exporting-text");
    const downloadBtn = document.getElementById("download-export-btn");

    // Disable export button and show exporting text
    exportBtn.disabled = true;
    exportingText.style.display = "inline";
    downloadBtn.style.display = "none";

    const selectedFields = [];
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]')?.value;

    if (document.getElementById("check_name").checked) selectedFields.push("name");
    if (document.getElementById("check_birthdate").checked) selectedFields.push("birthday");
    if (document.getElementById("check_address").checked) selectedFields.push("address");
    if (document.getElementById("check_telephone").checked) selectedFields.push("telephone");
    if (document.getElementById("check_mobile").checked) selectedFields.push("mobile");
    if (document.getElementById("check_email").checked) selectedFields.push("email");
    if (document.getElementById("check_civil_status").checked) selectedFields.push("civil_status");
    if (document.getElementById("check_sex").checked) selectedFields.push("sex");
    if (document.getElementById("check_school_year").checked) selectedFields.push("school_year");
    if (document.getElementById("check_course").checked) selectedFields.push("course");
    if (document.getElementById("check_employment").checked) selectedFields.push("employment");

    const schoolYear = document.getElementById("school_year_1").value;
    const course = document.getElementById("selectedCourse").value;

    const formData = new FormData();
    formData.append("data", JSON.stringify({
        fields: selectedFields,
        school_year: schoolYear !== "School Year" ? schoolYear : null,
        course: course || null
    }));

    fetch('/faculty/alumni-export', {
        method: "POST",
        body: formData,
        headers: {
            "X-CSRFToken": csrfToken
        }
    })
        .then(response => {
            if (response.ok) return response.blob();
            return response.json().then(err => { throw err; });
        })
        .then(blob => {
            const url = window.URL.createObjectURL(blob);

            // Setup and show the download button
            downloadBtn.href = url;
            downloadBtn.download = "alumni_export.csv";
            downloadBtn.style.display = "inline-block";

        })
        .catch(error => {
            alert(error.message || "Failed to export.");
        })
        .finally(() => {
            // Hide exporting text and enable export button again
            exportingText.style.display = "none";
            exportBtn.disabled = false;
        });
});
