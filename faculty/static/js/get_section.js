$(document).ready(function () {
    let page = 1;
    const pageSize = 20;

    function fetchSection(page) {
        let section_code = $('#search-section-code-input').val().trim();
        let course_name = $('#search-course-name-input').val().trim();
        let course_code = $('#search-course-code-input').val().trim();


        $('table').hide();
        $('.pagination-controls').hide();
        $('#searching-message').removeClass('d-none').show();

        let url = `/api/filtered-course-section/?page=${page}&page_size=${pageSize}`;

        if (section_code) {
            url += `&section_code=${encodeURIComponent(section_code)}`;
        }

        if (course_name) {
            url += `&course_name=${encodeURIComponent(course_name)}`;
        }

        if (course_code) {
            url += `&course_code=${encodeURIComponent(course_code)}`;
        }

        $.ajax({
            url: url,
            type: "GET",
            success: function (response) {
                // Hide the searching message
                $('#searching-message').addClass('d-none').hide();

                // Show table and pagination again
                $('table').show();
                $('.pagination-controls').show();

                // Clear and populate table with results
                let sectionTable = $('tbody');
                sectionTable.empty();

                if (response.results.length === 0) {
                    sectionTable.append(`<tr><td colspan="5" class="text-center">No Sections found.</td></tr>`);
                } else {
                    response.results.forEach(function (section) {
                        let row = `
                        <tr>
                            <td data-label="Course Name">${section.course_name}</td>
                            <td data-label="Course Code">${section.course_code}</td>
                            <td data-label="Section Code">${section.section_code}</td>
                            <td data-label="Actions" class="action-icons text-nowrap">
                                <a href="/faculty/course/${section.course_id}/edit"><i class="fas fa-edit"></i></a>
                                <a href="#" class="delete-item" data-id="${section.course_id}" data-type="article" data-bs-toggle="modal" data-bs-target="#deleteModal"><i class="fas fa-trash"></i></a>
                            </td>
                        </tr>
                    `;
                        sectionTable.append(row);
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

    $(document).on("click", "#pagination .page-link", function (e) {
        e.preventDefault();
        let newPage = parseInt($(this).data("page"));
        if (!isNaN(newPage)) {
            page = newPage;
            fetchSection(page);
        }
    });

    $('#search-btn').on('click', function () {
        page = 1;
        fetchSection(page);
    });

    $('#search-course-name-input, #search-course-code-input').on('keypress', function (e) {
        if (e.which === 13) { // Enter key
            e.preventDefault();
            page = 1;
            fetchSection(page);
        }
    });

    fetchSection(page);
});
