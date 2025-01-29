$(document).on("click", ".save-event-btn", function() {
    const eventId = $(this).data("id");

    $.ajax({
        url: `/events/save_event/${eventId}/`,
        method: "POST",
        headers: {
            "X-CSRFToken": getcsrftoken()
        },

        success: function(response, status, xhr) {
            let message = "";
            if (xhr.status === 201) {
                showToast('success','Event saved successfully!', "success");
            } else if (xhr.status === 200){
                message = `<p class="text-info">.</p>`;
                showToast('success','Event already saved', 'success');
            }

            $("#save-event-message").html(message); 
            
        },
        error: function(xhr) {
            if (xhr.status === 401) {
                showToast('No User Found', 'You need to log in to save Events.', 'warning');  
            } else if (xhr.status === 403) {
                showToast('No User Found', 'Please try logging in again.', 'warning');  
            } else if (xhr.status === 404) {
                showToast('Job not found', 'event not found.', 'danger');  
            } else if (xhr.status === 500) {
                showToast('ServerError', 'Server error. Please try again later.', 'danger');  
            }

            $("#save-event-message").html(message);
        }
    });

});

function getcsrftoken() {
    const cookieValue = document.cookie
        .split("; ")
        .find((row) => row.startsWith("csrftoken"))
        ?.split("=")[1];
    return cookieValue || "";
}
