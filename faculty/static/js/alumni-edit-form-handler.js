$(document).ready(function () {
    let alumniId = $("#alumniForm").data("alumni-id");

    $("#alumniForm").submit(function (event) {
        event.preventDefault();

        let formData = {
            basicInfo: {
                id: alumniId,
                lastName: $("#lastName").val().trim(),
                firstName: $("#firstName").val().trim(),
                middleName: $("#middleName").val().trim(),
                suffix: $("#suffix").val().trim(),
                birthday: $("#birthday").val(),
                address: $("#address").val().trim(),
                email: $("#email").val().trim(),
                telephone: $("#telephone").val().trim(),
                mobile: $("#mobile").val().trim(),
                civilStatus: $("#civilStatus").val(),
                sex: $("#sex").val(),
                course: $("#selectedCourse").val(),
                section: $("#section").val(),
                year_graduated: $("#year_graduated").val()
            },
            education: getEducationData(),
            licenses: getLicenseData(),
            workExperience: getWorkData()
        };

        $.ajax({
            url: `/faculty/alumni-edit/${alumniId}/`,
            type: "POST",
            data: JSON.stringify(formData),
            contentType: "application/json",
            headers: { "X-CSRFToken": getCSRFToken() },
            success: function (response) {
                showToast("Success", "Successfully Edited Alumni.", "success");
            },
            error: function (xhr, status, error) {
                console.error("Error:", error);
                showToast("Error", "Error submitting the form!", "danger");
            }
        });
    });

    function getEducationData() {
        let educationData = [];
        $("#educationSection .entry").each(function () {
            let school = $(this).find(".school").val().trim();
            let degree = $(this).find(".degree").val().trim();
            let year = $(this).find(".yearGraduated").val();

            if (school && degree && year) {
                educationData.push({ school, degree, year });
            }
        });
        return educationData;
    }

    function getLicenseData() {
        let licenseData = [];
        $("#licenseSection .entry").each(function () {
            let name = $(this).find(".license").val().trim();
            let org = $(this).find(".org").val().trim();
            let issueDate = $(this).find(".issueDate").val();
            let expirationDate = $(this).find(".expirationDate").val();

            if (name && org && issueDate) {
                licenseData.push({ name, org, issueDate, expirationDate });
            }
        });
        return licenseData;
    }

    function getWorkData() {
        let workData = [];
        $("#workSection .entry").each(function () {
            let company = $(this).find(".company").val().trim();
            let position = $(this).find(".position").val().trim();
            let startDate = $(this).find(".startDate").val();
            let endDate = $(this).find(".endDate").val();

            if (company && position && startDate) {
                workData.push({ company, position, startDate, endDate });
            }
        });
        return workData;
    }

    function getCSRFToken() {
        return $("input[name=csrfmiddlewaretoken]").val();
    }
});
