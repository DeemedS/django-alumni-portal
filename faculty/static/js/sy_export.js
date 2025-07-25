document.addEventListener("DOMContentLoaded", function () {
    const schoolYearSelect = document.getElementById("year_graduated_1");

    // Ensure year_graduated select exists
    if (!schoolYearSelect) {
        console.warn("Element with ID 'year_graduated' not found.");
        return;
    }

    const currentYear = new Date().getFullYear();
    for (let year = currentYear; year >= 1980; year--) {
        const option = document.createElement("option");
        option.value = `${year}`;
        option.textContent = `${year}`;
        schoolYearSelect.appendChild(option);
    }

    // Get selected school year dynamically (Replace this part in Django or another backend)
    const selectedSchoolYear = schoolYearSelect.getAttribute("data-selected-year");
    
    if (selectedSchoolYear) {
        schoolYearSelect.value = selectedSchoolYear;
    }
});
