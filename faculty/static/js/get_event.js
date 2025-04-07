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
                                <a href="#" data-id="${events.id}" data-bs-toggle="modal" data-bs-target="#deleteModal"><i class="fas fa-trash"></i></a>
                            </td>
                            <td class="text-center" data-label="Active">
                                <button class="${isActive === 'active' ? 'unpublish-btn' : 'publish-btn'}">
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

    fetchEvents(page);
});
