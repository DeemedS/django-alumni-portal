$(document).ready(function () {
    let page = 1;
    const pageSize = 20;

    function fetchArticles(page) {
        $.ajax({
            url: `/api/filtered-articles/?page=${page}&page_size=${pageSize}`,
            type: "GET",
            success: function (response) {
                let articlesTable = $("tbody");
                articlesTable.empty();

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
                                <a href="/articles/view/${articles.slug}/"><i class="fas fa-eye"></i></a>
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
                 
                createPagination(page, Math.ceil(response.count / pageSize), 5);
            },
            error: function (xhr, status, error) {
                console.error("Error fetching articles:", error);
            }
        });
    }

    $(document).on("click", "#pagination .page-link", function (e) {
        e.preventDefault();
        let newPage = parseInt($(this).data("page"));
        if (!isNaN(newPage)) {
            page = newPage;
            fetchArticles(page);
        }
    });

    // Handle publish/unpublish button click
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

    fetchArticles(page);

    });