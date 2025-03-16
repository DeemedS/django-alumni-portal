$(document).ready(function () {
    let page = 1;
    const pageSize = 20;

    function fetchCareers(page) {
        $.ajax({
            url: `/api/careers-list/?page=${page}&page_size=${pageSize}`,
            type: "GET",
            success: function (response) {
                let careersTable = $("tbody");
                careersTable.empty();

                response.results.forEach(function (careers) {
                    let isActive = careers.is_active ? "active" : "inactive";

                    let truncatedTitle = careers.title.split(" ").slice(0, 5).join(" ");
                    if (careers.title.split(" ").length > 5) {
                        truncatedTitle += "...";
                    }

                    let row = `
                        <tr>
                            <td class="center-dot" data-label="Active">
                                <div class="status-indicator ${isActive}"></div>
                            </td>
                            <td data-label="Title">${truncatedTitle}</td>
                            <td data-label="Company">${careers.company}</td>
                            <td data-label="Location">${careers.location}</td>
                            <td data-label="Job Type">${careers.job_type}</td>
                            <td data-label="Actions" class="action-icons">
                                <a href="/faculty/careers-view/${careers.id}"><i class="fas fa-eye"></i></a>
                                <a href="/faculty/careers-edit/${careers.id}"><i class="fas fa-edit"></i></a>
                                <a href="#" class="delete-career" data-id="${careers.id}"><i class="fas fa-trash"></i></a>
                            </td>
                        </tr>
                    `;
                    careersTable.append(row);
                });

                createPagination(page, Math.ceil(response.count / pageSize), 5);
            },
            error: function (xhr, status, error) {
                console.error("Error fetching alumni:", error);
            }
        });
    }

    $(document).on("click", "#pagination .page-link", function (e) {
        e.preventDefault();
        let newPage = parseInt($(this).data("page"));
        if (!isNaN(newPage)) {
            page = newPage;
            fetchCareers(page);
        }
    });

    fetchCareers(page);
});
