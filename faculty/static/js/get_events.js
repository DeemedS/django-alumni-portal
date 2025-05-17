$(document).ready(function () {
    let page = 1;
    const pageSize = 20;

    function fetchEvents(page) {
        $.ajax({
            url: `/api/filtered-events/?page=${page}&page_size=${pageSize}`,
            type: "GET",
            success: function (response) {
                let eventsTable = $("tbody");
                eventsTable.empty();
            
                response.results.forEach(function (events) {
                    let isActive = events.is_active ? "active" : "inactive";
            
                    let truncatedTitle = events.title.split(" ").slice(0, 5).join(" ");
                    if (events.title.split(" ").length > 5) {
                        truncatedTitle += "...";
                    }
                    let eventDate = new Date(events.date);
                    let formattedDate = eventDate.toLocaleDateString('en-US', {
                        year: 'numeric',
                        month: 'long',
                        day: 'numeric'
                    });
                    let formattedTime = eventDate.toLocaleTimeString('en-US', {
                        hour: 'numeric',
                        minute: 'numeric',
                        hour12: true
                    });
                    let formattedDateTime = `${formattedDate}, ${formattedTime}`;
            
                    let row = `
                        <tr>
                            <td data-label="Event">${events.title}</td>
                            <td data-label="Date">${formattedDateTime}</td>
                            <td data-label="Actions" class="action-icons">
                                <a href="/events/view/${events.slug}/"><i class="fas fa-eye"></i></a>
                                <a href="/faculty/events-edit/${events.slug}"><i class="fas fa-edit"></i></a>
                                <a href="#" class="delete-item" data-id="${events.id}" data-type="event" data-bs-toggle="modal" data-bs-target="#deleteModal"><i class="fas fa-trash"></i></a>
                            </td>
                            <td class="text-center" data-label="Active">
                                <button class="${isActive === 'active' ? 'unpublish-btn' : 'publish-btn'} toggle-status-btn" data-id="${events.id}">
                                    ${isActive === 'active' ? 'Unpublish' : 'Publish'}
                                </button>
                            </td>
                        </tr>
                    `;
                    eventsTable.append(row);
                });
            
                createPagination(page, Math.ceil(response.count / pageSize), 5);
            },
            error: function (error) {
                console.error("Error fetching events:", error);
            }
        });
    }

    $(document).on("click", "#pagination .page-link", function (e) {
        e.preventDefault();
        let newPage = parseInt($(this).data("page"));
        if (!isNaN(newPage)) {
            page = newPage;
            fetchEvents(page);
        }
    });

    // Handle publish/unpublish button click
    $(document).on("click", ".toggle-status-btn", function () {
        const button = $(this);
        const eventId = button.data("id");

        $.ajax({
            url: `/events/toggle_status/${eventId}/`,
            type: "POST",
            headers: {
                'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function () {
                if (button.hasClass("publish-btn")) {
                    button.removeClass("publish-btn").addClass("unpublish-btn").text("Unpublish");
                } else {
                    button.removeClass("unpublish-btn").addClass("publish-btn").text("Publish");
                }

                showToast("Success", "Event status updated successfully!", "success");
            },
            error: function (xhr, status, error) {
                console.error("Error toggling event status:", error);
            }
        });
    });

    fetchEvents(page);
});
