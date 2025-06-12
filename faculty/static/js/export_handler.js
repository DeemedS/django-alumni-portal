document.getElementById("export-btn").addEventListener("click", function () {
    const exportBtn = this;
    const exportingText = document.getElementById("exporting-text");
    const downloadBtn = document.getElementById("download-export-btn");

    exportBtn.disabled = true;
    exportingText.classList.remove("d-none");
    downloadBtn.classList.add("d-none");

    const selectedFields = [];

    if (document.getElementById("check_name").checked) selectedFields.push("name");
    if (document.getElementById("check_birthdate").checked) selectedFields.push("birthday");
    if (document.getElementById("check_address").checked) selectedFields.push("address");
    if (document.getElementById("check_telephone").checked) selectedFields.push("telephone");
    if (document.getElementById("check_mobile").checked) selectedFields.push("mobile");
    if (document.getElementById("check_email").checked) selectedFields.push("email");
    if (document.getElementById("check_civil_status").checked) selectedFields.push("civil_status");
    if (document.getElementById("check_sex").checked) selectedFields.push("sex");
    if (document.getElementById("check_year_graduated").checked) selectedFields.push("year_graduated");
    if (document.getElementById("check_course").checked) selectedFields.push("course");
    if (document.getElementById("check_employment").checked) selectedFields.push("employment");

    const schoolYear = document.getElementById("year_graduated_1").value;
    const course = document.getElementById("selectedCourse").value;
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]')?.value;

    const formData = new FormData();
    formData.append("data", JSON.stringify({
        fields: selectedFields,
        year_graduated: schoolYear || null,
        course: course || null
    }));

    fetch("/faculty/alumni-export", {
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
        downloadBtn.href = url;
        downloadBtn.download = "alumni_export.csv";
        downloadBtn.classList.remove("d-none");
    })
    .catch(error => {
        alert(error.message || "Failed to export.");
    })
    .finally(() => {
        exportingText.classList.add("d-none");
        exportBtn.disabled = false;
    });
});

document.getElementById("cancel-export-btn").addEventListener("click", function () {

    document.querySelectorAll("#export-modal .form-check-input").forEach(input => {
        input.checked = false;
    });

    document.getElementById("year_graduated_1").value = "";
    document.getElementById("courseSearch").value = "";
    document.getElementById("course_name").value = "";
    document.getElementById("selectedCourse").value = "";
    document.getElementById("courseSuggestions").innerHTML = "";

    document.getElementById("exporting-text").style.display = "none";
    document.getElementById("download-export-btn").style.display = "none";
    document.getElementById("export-btn").disabled = false;
});