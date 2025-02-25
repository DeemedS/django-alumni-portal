$(document).ready(function () {
    let page = 1;
    const pageSize = 20;

    function fetchAlumni(page) {
        $.ajax({
            url: `/api/alumni-list/?page=${page}&page_size=${pageSize}`,
            type: "GET",
            success: function (response) {
                let alumniTable = $("tbody");
                alumniTable.empty();

                response.results.forEach(function (alumni) {
                    let isActive = alumni.is_active ? "active" : "inactive";

                    let row = `
                        <tr>
                            <td class="center-dot" data-label="Active">
                                <div class="status-indicator ${isActive}"></div>
                            </td>
                            <td data-label="Name">${alumni.first_name}</td>
                            <td data-label="Email">${alumni.email}</td>
                            <td data-label="Phone">${alumni.mobile || "N/A"}</td>
                            <td data-label="Course">${alumni.course || "N/A"}</td>
                            <td data-label="Date Created">${new Date(alumni.date_created).toLocaleDateString()}</td>
                            <td data-label="Actions" class="action-icons">
                                <a href="/faculty/alumni-view/${alumni.id}"><i class="fas fa-eye"></i></a>
                                <a href="/faculty/alumni-edit/${alumni.id}"><i class="fas fa-edit"></i></a>
                                <a href="#" class="delete-alumni" data-id="${alumni.id}"><i class="fas fa-trash"></i></a>
                            </td>
                        </tr>
                    `;
                    alumniTable.append(row);
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
            fetchAlumni(page);
        }
    });

    fetchAlumni(page);
});
