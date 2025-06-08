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
                credentials: 'include'
            });
            const result = await response.json();

            if (response.ok && result.image_url) {
                showToast("Success", "Profile photo updated successfully.", "success");
                setTimeout(() => location.reload(), 1500);
            } else {
                showToast("Error", result.error || "Failed to update photo.", "error");
            }
        } catch (error) {
            showToast("Error", "Error uploading photo.", "error");
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
                credentials: 'include'
            });
            const result = await response.json();

            if (response.ok) {
                showToast("Success", "Profile photo removed successfully.", "success");
                setTimeout(() => location.reload(), 1500);
            } else {
                showToast("Error", result.error || "Failed to remove photo.", "error");
            }
        } catch (error) {
            showToast("Error", "Error removing photo.", "error");
            console.error(error);
        }
    });
});
