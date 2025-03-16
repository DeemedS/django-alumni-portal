function generateYearOptions() {
    let currentYear = new Date().getFullYear();
    let options = '<option value="" selected disabled>Select year</option>';
    for (let year = 1980; year <= currentYear; year++) {
        options += `<option value="${year}">${year}</option>`;
    }
    return options;
}