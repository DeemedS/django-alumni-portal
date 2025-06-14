$(document).ready(function () {
    let page = 1;
    const pageSize = 20;

    function fetchCourse(page) {
        let course_code = $('#search-course-code-input').val().trim();
        let course_name = $('#search-course-name-input').val().trim();


        $('table').hide();
        $('.pagination-controls').hide();
        $('#searching-message').removeClass('d-none').show();

        let url = `/api/filtered-course-section/?page=${page}&page_size=${pageSize}`;

        if (course_code) {
            url += `&course_code=${encodeURIComponent(course_code)}`;
        }

        if (course_name) {
            url += `&course_name=${encodeURIComponent(course_name)}`;
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
                let courseTable = $('tbody');
                courseTable.empty();

                if (response.results.length === 0) {
                    courseTable.append(`<tr><td colspan="5" class="text-center">No Course found.</td></tr>`);
                } else {
                    response.results.forEach(function (course) {
                        let row = `
                        <tr>
                            <td data-label="Course Name">${course.course_name}</td>
                            <td data-label="Course Code">${course.course_code}</td>
                            <td data-label="Actions" class="action-icons text-nowrap">
                                <a href="#"
                                class="edit-course-btn-me"                                 
                                data-id="${course.id}" 
                                data-name="${course.course_name}" 
                                data-code="${course.course_code}"
                                data-bs-toggle="modal" 
                                data-bs-target="#edit-course-modal"><i class="fas fa-edit"></i></a>
                                <a href="#" class="delete-item" data-id="${course.id}" data-type="course" data-bs-toggle="modal" data-bs-target="#deleteModal"><i class="fas fa-trash"></i></a>
                            </td>
                        </tr>
                    `;
                        courseTable.append(row);
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

    // Pagination click event
    $(document).on("click", "#pagination .page-link", function (e) {
        e.preventDefault();
        let newPage = parseInt($(this).data("page"));
        if (!isNaN(newPage)) {
            page = newPage;
            fetchCourse(page);
        }
    });

    // Search button click event — resets page to 1 and fetches course with query
    $('#search-btn').on('click', function () {
        page = 1;
        fetchCourse(page);
    });

    // Optional: Pressing Enter inside search input triggers search too
    $('#search-course-name-input, #search-course-code-input').on('keypress', function (e) {
        if (e.which === 13) { // Enter key
            e.preventDefault();
            page = 1;
            fetchCourse(page);
        }
    });

    // Initial fetch
    fetchCourse(page);
});
