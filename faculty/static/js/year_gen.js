function generateYearOptions() {
    let currentYear = new Date().getFullYear();
    let options = '<option value="" selected disabled>Select Year</option>';
    for (let year = 1980; year <= currentYear; year++) {
        options += `<option value="${year}">${year}</option>`;
    }
    return options;
}

document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".yearGraduated").forEach(select => {
        select.innerHTML = generateYearOptions();
        let selectedYear = select.getAttribute("data-selected-year"); // Get pre-selected value
        if (selectedYear) {
            select.value = selectedYear; // Set the pre-selected value
        }
    });
});