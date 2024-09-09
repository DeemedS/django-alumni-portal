
function validateEmail(email) {

    const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    return pattern.test(email);
}

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('email').addEventListener('input', function() {
        const email = this.value;
        const isValid = validateEmail(email);
        
        if (email != '') {

            if (isValid === false) {
                document.getElementById('email').classList.add('is-invalid');
                document.getElementById('form-submit').disabled = true;
                document.getElementById('form-submit').style.cursor = 'not-allowed';
            } else {
                document.getElementById('email').classList.remove('is-invalid');
                document.getElementById('form-submit').disabled = false;
                document.getElementById('form-submit').style.cursor = 'pointer';
            }
        }

        else {
            document.getElementById('email').classList.remove('is-invalid');
            document.getElementById('form-submit').disabled = false;
        }

    });
});
