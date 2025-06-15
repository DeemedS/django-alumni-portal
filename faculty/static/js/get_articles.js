$(document).ready(function () {
    let page = 1;
    const pageSize = 20;

    // Fetch articles with optional search query and page number
    function fetchArticles(page) {
        let query = $('#search-input').val().trim();

        // Hide table and pagination
        $('table').hide();
        $('.pagination-controls').hide();

        // Show the searching message
        $('#searching-message').removeClass('d-none').show();

        let url = `/api/filtered-articles/?page=${page}&page_size=${pageSize}`;
        if (query) {
            url += `&q=${encodeURIComponent(query)}`;
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
                let articlesTable = $('tbody');
                articlesTable.empty();

                if (response.results.length === 0) {
                    articlesTable.append(`<tr><td colspan="5" class="text-center">No articles found.</td></tr>`);
                } else {
                    response.results.forEach(function (articles) {
                        let isActive = articles.is_active ? "active" : "inactive";

                        let truncatedTitle = articles.title.split(" ").slice(0, 5).join(" ");
                        if (articles.title.split(" ").length > 5) {
                            truncatedTitle += "...";
                        }

                        let articleDate = new Date(articles.date);
                        let formattedDate = articleDate.toLocaleDateString('en-US', {
                            year: 'numeric',
                            month: 'long',
                            day: 'numeric'
                        });
                        let formattedTime = articleDate.toLocaleTimeString('en-US', {
                            hour: 'numeric',
                            minute: 'numeric',
                            hour12: true
                        });
                        let formattedDateTime = `${formattedDate}, ${formattedTime}`;

                        let row = `
                        <tr>
                            <td data-label="Title">${truncatedTitle}</td>
                            <td data-label="Date">${formattedDateTime}</td>
                            <td data-label="Category">${articles.category}</td>
                            <td data-label="Actions" class="action-icons text-nowrap">
                                <a href="/faculty/articles-view/${articles.slug}/"><i class="fas fa-eye"></i></a>
                                <a href="/faculty/articles/${articles.slug}/edit"><i class="fas fa-edit"></i></a>
                                <a href="#" class="delete-item" data-id="${articles.id}" data-type="article" data-bs-toggle="modal" data-bs-target="#deleteModal"><i class="fas fa-trash"></i></a>
                            </td>
                            <td class="text-center" data-label="Active">
                                <button class="${isActive === 'active' ? 'unpublish-btn' : 'publish-btn'} toggle-status-btn" data-id="${articles.id}">
                                    ${isActive === 'active' ? 'Unpublish' : 'Publish'}
                                </button>
                            </td>
                        </tr>
                    `;
                        articlesTable.append(row);
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
            fetchArticles(page);
        }
    });

    // Publish/unpublish button click event
    $(document).on("click", ".toggle-status-btn", function () {
        const button = $(this);
        const articleId = button.data("id");

        $.ajax({
            url: `/article/toggle_status/${articleId}/`,
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

                showToast("Success", "Article status updated successfully!", "success");
            },
            error: function (xhr, status, error) {
                console.error("Error toggling article status:", error);
            }
        });
    });

    // Search button click event — resets page to 1 and fetches articles with query
    $('#search-button').on('click', function () {
        page = 1;
        fetchArticles(page);
    });

    // Optional: Pressing Enter inside search input triggers search too
    $('#search-input').on('keypress', function (e) {
        if (e.which === 13) { // Enter key
            e.preventDefault();
            page = 1;
            fetchArticles(page);
        }
    });

    // Initial fetch
    fetchArticles(page);
});
