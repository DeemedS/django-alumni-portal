document.addEventListener("DOMContentLoaded", function () {

    document.body.addEventListener("click", function (event) {
        if (event.target.matches("#addEducation")) {
            addEducationEntry();
        } else if (event.target.matches("#addLicense")) {
            addLicenseEntry();
        } else if (event.target.matches("#addWork")) {
            addWorkEntry();
        } else if (event.target.matches(".remove-btn")) {
            event.target.closest(".entry").remove();
        }
    });

    // Function to add a new education entry
    function addEducationEntry() {
        let educationContainer = document.createElement("div");
        educationContainer.classList.add("row", "g-3", "mt-3", "entry");
        educationContainer.innerHTML = `
            <div class="col-md-3">
                <label class="form-label">School Graduated</label>
                <input type="text" class="form-control school" placeholder="School Graduated">
            </div>
            <div class="col-md-3">
                <label class="form-label">Degree/Course</label>
                <input type="text" class="form-control degree" placeholder="Degree/Course">
            </div>
            <div class="col-md-3">
                <label class="form-label">Year Graduated</label>
                <select class="form-select yearGraduated">${generateYearOptions()}</select>
            </div>
            <div class="col-md-3 d-flex align-items-end">
                <button type="button" class="btn btn-danger remove-btn">Remove</button>
            </div>
        `;
        document.querySelector("#educationSection").appendChild(educationContainer);
    }

    // Function to add a new license entry
    function addLicenseEntry() {
        let licenseContainer = document.createElement("div");
        licenseContainer.classList.add("row", "g-3", "mt-3", "entry");
        licenseContainer.innerHTML = `
            <div class="col-md-3">
                <label class="form-label">License or Certification Name</label>
                <input type="text" class="form-control license" placeholder="License or Certification Name">
            </div>
            <div class="col-md-3">
                <label class="form-label">Issuing Organization</label>
                <input type="text" class="form-control org" placeholder="Issuing Organization">
            </div>
            <div class="col-md-2">
                <label class="form-label">Issue Date</label>
                <input type="date" class="form-control issueDate">
            </div>
            <div class="col-md-2">
                <label class="form-label">Expiration Date</label>
                <input type="date" class="form-control expirationDate">
            </div>
            <div class="col-md-2 d-flex align-items-end">
                <button type="button" class="btn btn-danger remove-btn">Remove</button>
            </div>
        `;
        document.querySelector("#licenseSection").appendChild(licenseContainer);
    }

    // Function to add a new work experience entry
    function addWorkEntry() {
        let workContainer = document.createElement("div");
        workContainer.classList.add("row", "g-3", "mt-3", "entry");
        workContainer.innerHTML = `
            <div class="col-md-3">
                <label class="form-label">Company Name</label>
                <input type="text" class="form-control company" placeholder="Company Name (e.g., Google, Microsoft)">
            </div>
            <div class="col-md-3">
                <label class="form-label">Position</label>
                <input type="text" class="form-control position" placeholder="(e.g., Software Engineer)">
            </div>
            <div class="col-md-2">
                <label class="form-label">Start Date</label>
                <input type="date" class="form-control startDate">
            </div>
            <div class="col-md-2">
                <label class="form-label">End Date</label>
                <input type="date" class="form-control endDate">
            </div>
            <div class="col-md-1 d-flex align-items-end">
                <button type="button" class="btn btn-danger remove-btn">Remove</button>
            </div>
        `;
        document.querySelector("#workSection").appendChild(workContainer);
    }
});
