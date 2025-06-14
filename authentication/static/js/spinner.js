document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    const submitBtn = document.getElementById('form-submit');
    const spinner = document.getElementById('btn-spinner');

    if (form) {
        form.addEventListener('submit', function () {
            spinner.classList.remove('d-none');
            submitBtn.disabled = true;
        });
    }
});