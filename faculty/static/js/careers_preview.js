document.addEventListener('DOMContentLoaded', function () {

    const createdAtSpan = document.querySelector('.created-at-text');

    if (createdAtSpan) {
        const today = new Date();
        const options = { year: 'numeric', month: 'long', day: 'numeric' };
        const formattedDate = today.toLocaleDateString(undefined, options);

        if (createdAtSpan.textContent.trim() === '') {
            createdAtSpan.textContent = formattedDate;
        }
    }

    // Form fields
    const titleInput = document.getElementById('title');
    const companyInput = document.getElementById('company');
    const companyEmailInput = document.getElementById('company_email');
    const companyContactInput = document.getElementById('company_contact');
    const salaryInput = document.getElementById('salary');
    const locationInput = document.getElementById('location');
    const jobTypeSelect = document.getElementById('job-type');
    const descriptionInput = document.getElementById('description');
    const responsibilitiesInput = document.getElementById('responsibilities');
    const qualificationsInput = document.getElementById('qualifications');
    const benefitsInput = document.getElementById('benefits');

    function updatePreview() {
        // Helper function to toggle content visibility
    function toggleSection(value, elementSelector, wrapperSelector = null) {
        const element = document.querySelector(elementSelector);
        const wrapper = wrapperSelector ? document.querySelector(wrapperSelector) : null;

        if (!element) return; // Prevent error if element not found

        if (value.trim()) {
            element.textContent = value;
            if (wrapper) wrapper.style.display = '';
        } else {
            element.textContent = '';
            if (wrapper) wrapper.style.display = 'none';
        }
    }
    
        toggleSection(titleInput.value, '.preview-title');
        toggleSection(companyInput.value, '.company-text', '.preview-company');
        toggleSection(companyEmailInput.value, '.company-email-text', '.preview-company-email');
        toggleSection(companyContactInput.value, '.company-contact-text', '.preview-contact');
        toggleSection(locationInput.value, '.location-text', '.preview-location');
        toggleSection(salaryInput.value, '.salary-text', '.preview-salary');
        toggleSection(jobTypeSelect.value, '.job-type-text', '.preview-job-type');
        toggleSection(descriptionInput.value, '.description-text', '.preview-description');
        toggleSection(responsibilitiesInput.value, '.responsibilities-text', '.preview-responsibilities');
        toggleSection(qualificationsInput.value, '.qualifications-text', '.preview-qualifications');
        toggleSection(benefitsInput.value, '.benefits-text', '.preview-benefits');
    }

    // Add input listeners
    [
        titleInput,
        companyInput,
        companyEmailInput,
        companyContactInput,
        salaryInput,
        locationInput,
        jobTypeSelect,
        descriptionInput,
        responsibilitiesInput,
        qualificationsInput,
        benefitsInput
    ].forEach(el => {
        el.addEventListener('input', updatePreview);
        el.addEventListener('change', updatePreview);
    });

    updatePreview(); // Initial fill on load (optional)
});