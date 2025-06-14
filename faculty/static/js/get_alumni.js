$(document).ready(function () {
    let page = 1;
    const pageSize = 20;

    function fetchAlumni(page) {
        // Get the latest values from inputs
        let query = $('#search-input').val().trim();
        let course_code = $('#course-code-input').val().trim();
        let year_graduated = $('#year_graduated').val() || "";
        let verification = $('#verification-status').val().trim();

        // Hide table and pagination
        $('table').hide();
        $('.pagination-controls').hide();

        // Show the searching message
        $('#searching-message').removeClass('d-none').show();

        $.ajax({
            url: `/api/alumni-list/`,
            type: "GET",
            data: {
                page: page,
                page_size: pageSize,
                search: query,
                course_code: course_code,
                year_graduated: year_graduated,
                verification: verification
            },
            success: function (response) {

                // Hide the searching message
                $('#searching-message').addClass('d-none').hide();

                // Show table and pagination again
                $('table').show();
                $('.pagination-controls').show();

                // Clear and populate table with results
                let alumniTable = $("tbody");
                alumniTable.empty();
                if (response.results.length === 0) {
                    alumnisTable.append(`<tr><td colspan="5" class="text-center">No alumnis found.</td></tr>`);
                } else {
                    response.results.forEach(function (alumni) {
                        let isActive = alumni.is_active ? "active" : "inactive";

                        let row = `
                        <tr>
                            <td class="center-dot" data-label="Active">
                                <div class="status-indicator ${isActive}"></div>
                            </td>
                            <td data-label="Name">${alumni.last_name} ${alumni.first_name}</td>
                            <td data-label="Email">${alumni.email}</td>
                            <td data-label="Phone">${alumni.mobile || "N/A"}</td>
                            <td data-label="Course">${alumni.course_code || "N/A"}</td>
                            <td data-label="Section">${alumni.section_code || "N/A"}</td>
                            <td data-label="Batch">${alumni.year_graduated || "N/A"}</td>
                            <td data-label="Actions" class="action-icons text-nowrap">
                                <a href="/faculty/alumni-view/${alumni.id}"><i class="fas fa-eye"></i></a>
                                <a href="/faculty/alumni-edit/${alumni.id}"><i class="fas fa-edit"></i></a>
                                <a href="#" class="delete-item" data-id="${alumni.id}" data-type="alumni" data-bs-toggle="modal" data-bs-target="#deleteModal"><i class="fas fa-trash"></i></a>
                            </td>
                            <td class="text-center" data-label="Status">
                                <button class="${isActive === 'active' ? 'verified-btn' : 'unverified-btn'} toggle-status-btn" data-id="${alumni.id}">
                                    ${isActive === 'active' ? 'Verified' : 'Verify'}
                                </button>
                            </td>
                        </tr>
                    `;
                        alumniTable.append(row);
                    });
                }

                createPagination(page, Math.ceil(response.count / pageSize), 5);
            },
            error: function (xhr, status, error) {
                $('#searching-message').addClass('d-none').hide();
                $('table').show();
                $('.pagination-controls').show();
                console.error("Error fetching article:", error);
            }
        });
    }

    $(document).on("click", ".toggle-status-btn", function () {
        const button = $(this);
        const alumniId = button.data("id");

        $.ajax({
            url: `/user/toggle_status/${alumniId}/`,
            type: "POST",
            headers: {
                'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function () {
                if (button.hasClass("verified-btn")) {
                    button.removeClass("verified-btn").addClass("unverified-btn").text("Unverified");
                } else {
                    button.removeClass("unverified-btn").addClass("verified-btn").text("Verified");
                }

                showToast("Success", "Alumni status updated successfully!", "success");
            },
            error: function (xhr, status, error) {
                console.error("Error toggling alumni status:", error);
            }
        });
    });

    $(document).on("click", "#pagination .page-link", function (e) {
        e.preventDefault();
        let newPage = parseInt($(this).data("page"));
        if (!isNaN(newPage)) {
            page = newPage;
            fetchAlumni(page);
        }
    });

    // Search/filter button
    $('#search-btn').on('click', function () {
        page = 1;
        fetchAlumni(page);
    });

    // Optionally, auto-fetch when filter inputs change
    $('#course-code-input, #search-input, #year_graduated, #verification-status').on('change', function () {
        page = 1;
        fetchAlumni(page);
    });

    fetchAlumni(page);
});
