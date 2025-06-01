document.addEventListener("DOMContentLoaded", function () {
    const schoolYearSelect = document.getElementById("school_year");

    // Ensure school_year select exists
    if (!schoolYearSelect) {
        console.warn("Element with ID 'school_year' not found.");
        return;
    }

    const currentYear = new Date().getFullYear();
    for (let year = currentYear; year >= 1980; year--) {
        const option = document.createElement("option");
        option.value = `${year}-${year + 1}`;
        option.textContent = `${year}-${year + 1}`;
        schoolYearSelect.appendChild(option);
    }

    // Get selected school year dynamically (Replace this part in Django or another backend)
    const selectedSchoolYear = schoolYearSelect.getAttribute("data-selected-year");
    
    if (selectedSchoolYear) {
        schoolYearSelect.value = selectedSchoolYear;
    }
});
