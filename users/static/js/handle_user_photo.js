document.addEventListener('DOMContentLoaded', () => {
    const changePhotoBtn = document.getElementById('changePhotoBtn');
    const removePhotoBtn = document.getElementById('removePhotoBtn');
    const photoInput = document.getElementById('photoInput');
    const profileImage = document.getElementById('profileImage');
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]')?.value;

    changePhotoBtn.addEventListener('click', () => photoInput.click());

    photoInput.addEventListener('change', async () => {
        const file = photoInput.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append('photo', file);

        try {
            const response = await fetch("/myaccount/photo/upload/", {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken
                },
                body: formData,
            });
            const result = await response.json();
            if (response.ok && result.image_url) {
                profileImage.src = result.image_url;
                alert('Photo updated successfully!');
            } else {
                alert(result.error || 'Failed to update photo');
            }
        } catch (error) {
            alert('Error uploading photo');
            console.error(error);
        }
    });

    removePhotoBtn.addEventListener('click', async () => {
        if (!confirm('Are you sure you want to remove your profile photo?')) return;

        try {
            const response = await fetch("/myaccount/photo/remove/", {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken
                },
            });
            const result = await response.json();
            if (response.ok) {
                alert('Photo removed successfully!');
            } else {
                alert(result.error || 'Failed to remove photo');
            }
        } catch (error) {
            alert('Error removing photo');
            console.error(error);
        }
    });
});