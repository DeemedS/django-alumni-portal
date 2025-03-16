document.addEventListener("DOMContentLoaded", function () {
    function getEducationData() {
        let educationEntries = document.querySelectorAll("#educationSection .entry");
        let educationData = [];

        educationEntries.forEach(entry => {
            let school = entry.querySelector(".school").value.trim();
            let degree = entry.querySelector(".degree").value.trim();
            let year = entry.querySelector(".yearGraduated").value;
            
            if (school && degree && year) {
                educationData.push({ school, degree, year });
            }
        });

        return educationData;
    }

    function getLicenseData() {
        let licenseEntries = document.querySelectorAll("#licenseSection .entry");
        let licenseData = [];

        licenseEntries.forEach(entry => {
            let name = entry.querySelector(".license").value.trim();
            let org = entry.querySelector(".org").value.trim();
            let issueDate = entry.querySelector(".issueDate").value;
            let expirationDate = entry.querySelector(".expirationDate").value;

            if (name && org && issueDate) {
                licenseData.push({ name, org, issueDate, expirationDate });
            }
        });

        return licenseData;
    }

    function getWorkData() {
        let workEntries = document.querySelectorAll("#workSection .entry");
        let workData = [];

        workEntries.forEach(entry => {
            let company = entry.querySelector(".company").value.trim();
            let position = entry.querySelector(".position").value.trim();
            let startDate = entry.querySelector(".startDate").value;
            let endDate = entry.querySelector(".endDate").value;

            if (company && position && startDate) {
                workData.push({ company, position, startDate, endDate });
            }
        });

        return workData;
    }

    // Handle form submission
    document.querySelector("#alumniForm").addEventListener("submit", function (event) {
        event.preventDefault(); // Prevent actual form submission

        let formData = {
            basicInfo: {
                lastName: document.querySelector("#lastName").value,
                firstName: document.querySelector("#firstName").value,
                middleName: document.querySelector("#middleName").value,
                suffix: document.querySelector("#suffix").value,
                birthday: document.querySelector("#birthday").value,
                address: document.querySelector("#address").value,
                email: document.querySelector("#email").value,
                telephone: document.querySelector("#telephone").value,
                mobile: document.querySelector("#mobile").value,
                civilStatus: document.querySelector("#civilStatus").value,
                sex: document.querySelector("#sex").value,
                course: document.querySelector("#selectedCourse").value,
                section: document.querySelector("#section").value,
                schoolYear: document.querySelector("#school_year").value
            },
            education: getEducationData(),
            licenses: getLicenseData(),
            workExperience: getWorkData()
        };

        console.log(formData)

        // Optionally: Send data to server via AJAX
        // fetch('/submit', { method: 'POST', body: JSON.stringify({ education, licenses, work }), headers: { 'Content-Type': 'application/json' } });

        alert("Form submitted! Check the console for data.");
    });
});
