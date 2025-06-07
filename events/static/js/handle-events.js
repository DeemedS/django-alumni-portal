$(document).on("click", ".save-event-btn", function() {
    const eventId = $(this).data("id");
    const button = $(this);
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]')?.value;

    $.ajax({
        url: `/events/save_event/${eventId}/`,
        method: "POST",
        headers: {
            "X-CSRFToken": csrfToken
        },

        success: function(response, status, xhr) {
            if (xhr.status === 201) {
                showToast('success','Event saved successfully!', "success");
                button.text("Unsave Event").removeClass("btn-outline-danger save-event-btn").addClass("btn-danger unsave-event-btn");
            } else if (xhr.status === 200){
                message = `<p class="text-info">.</p>`;
                showToast('success','Event already saved', 'success');
                button.text("Unsave Event").removeClass("btn-outline-danger save-event-btn").addClass("btn-danger unsave-event-btn");
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

$(document).on("click", ".unsave-event-btn", function () {
    const eventId = $(this).attr("data-id");
    const button = $(this);
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]')?.value;

    $.ajax({
        url: `/events/unsave_event/${eventId}/`,
        method: "POST",
        headers: {
            "X-CSRFToken": csrfToken
        },
        success: function (response, status, xhr) {
            if (xhr.status === 200) { 
                showToast('Success', 'Job removed successfully!', 'success');
                button.text("Save Event").removeClass("btn-danger unsave-event-btn").addClass("btn-outline-danger save-event-btn");
            } 
        },
        error: function (xhr) {
            if (xhr.status === 401) {
                showToast('No User Found', 'You need to log in to save event.', 'warning');  
            } else if (xhr.status === 403) {
                showToast('No User Found', 'Please try logging in again.', 'warning');  
            } else if (xhr.status === 404) {
                showToast('Job not found', 'Job not found.', 'danger');  
            } else if (xhr.status === 500) {
                showToast('ServerError', 'Server error. Please try again later.', 'danger');  
            }
        }
    });
});


