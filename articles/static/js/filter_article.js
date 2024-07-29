$(document).ready(function() {

    updateArticleCards();


    $('#article-filter, #month-filter, #year-filter').change(function() {
        updateArticleCards();
    });


    $(document).on('click', '.page-link', function(e) {
        e.preventDefault();
        var page = $(this).data('page');
        updateArticleCards(page);
    });

    function updateArticleCards(page = 1) {
        var articleFilter = $('#article-filter').val();
        var monthFilter = $('#month-filter').val();
        var yearFilter = $('#year-filter').val();

        var pageSize = window.innerWidth <= 640 ? 2 : (window.innerWidth <= 1024 ? 4 : 8);

        var data = {
            article_filter: articleFilter,
            page: page,
            page_size: pageSize
        };

        if (monthFilter !== "0") {
            data.month = monthFilter;
        }

        if (yearFilter) {
            data.year = yearFilter;
        }



        $('#article-cards-container').fadeOut(400, function() {
            $.ajax({
                url: '/api/filtered-articles/',
                type: 'GET',
                data: data,
                success: function(response) {

                    $('#article-cards-container').empty();
                    if (response.results.length > 0) {
                        $.each(response.results, function(index, article) {
                            var articleDate = new Date(article.date).toDateString();
                            var cardHtml = `<div class="card col-md-8 mb-4">
                                                <div class="position-relative">
                                                    <img src="${article.thumbnail || '/static/images/default_image.png'}" class="card-img-top" alt="${article.title}">
                                                    <div class="overlay">
                                                        <div class="badge text-bg-warning">${articleDate}</div>
                                                    </div>
                                                </div>
                                                <div class="card-body">
                                                    <h5 class="card-title">${article.title}</h5>
                                                    <p class="card-text">${truncateWords(article.body, 20)}</p>
                                                    <a href="/articles/view/${article.slug}" class="btn btn-primary">Learn More</a>
                                                </div>
                                            </div>`;
                            $('#article-cards-container').append(cardHtml);
                        });
                    } else {
                        var noArticleHtml = '<div class="col-12 text-center"><p>No articles found for the selected filters.</p></div>';
                        $('#article-cards-container').append(noArticleHtml);
                    }


                    $('#pagination').empty();
                    for (var i = 1; i <= Math.ceil(response.count / pageSize); i++) {
                        var activeClass = (i === page) ? ' active' : '';
                        var pageLink = '<li class="page-item' + activeClass + '"><a class="page-link" href="#latest-articles" data-page="' + i + '">' + i + '</a></li>';
                        $('#pagination').append(pageLink);
                    }

                    $('#article-cards-container').fadeIn(400);
                },
                error: function(xhr, status, error) {
                    console.error('Error fetching articles:', error);
                    $('#article-cards-container').fadeIn(400);
                }
            });
        });
    }

    function truncateWords(str, num) {
        if (!str) return '';
        var words = str.split(" ");
        if (words.length <= num) {
            return str;
        }
        return words.slice(0, num).join(" ") + "...";
    }
});
