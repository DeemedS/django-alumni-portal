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
                            <td data-label="Actions" class="action-icons">
                                <a href="/articles/view/${articles.slug}/"><i class="fas fa-eye"></i></a>
                                <a href="/faculty/articles/${articles.slug}/edit"><i class="fas fa-edit"></i></a>
                                <a href="#" class="delete-article" data-id="${articles.id}" data-bs-toggle="modal" data-bs-target="#deleteModal"><i class="fas fa-trash"></i></a>
                            </td>
                            <td class="text-center" data-label="Active">
                                <button class="${isActive === 'active' ? 'unpublish-btn' : 'publish-btn'}">
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

    fetchArticles(page);

    });