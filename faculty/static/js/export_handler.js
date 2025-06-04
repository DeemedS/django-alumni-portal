document.addEventListener('DOMContentLoaded', () => {

    // 📤 Export Alumni Data
    document.getElementById('export-btn').addEventListener('click', function () {
        const selectedFields = [];
        document.querySelectorAll('#export-modal .form-check-input[type="checkbox"]:checked').forEach(cb => {
            selectedFields.push(cb.id);
        });

        const year = document.getElementById('yearSelect').value;
        const course = document.getElementById('courseSelect').value;

        const payload = {
            fields: selectedFields,
            year: year !== 'Select Year' ? year : null,
            course: course !== 'Select Course' ? course : null
        };

        fetch('/export-alumni', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        })
            .then(res => res.blob())
            .then(blob => {
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'alumni_export.xlsx';
                document.body.appendChild(a);
                a.click();
                a.remove();
                bootstrap.Modal.getInstance(document.getElementById('export-modal')).hide();
            })
            .catch(err => {
                console.error(err);
                alert('An error occurred while exporting the data.');
            });
    });
});