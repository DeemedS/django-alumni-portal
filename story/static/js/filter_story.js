$(document).ready(function() {

    updateStoryCards();

    $(document).on('click', '.page-link', function(e) {
        e.preventDefault();
        var page = $(this).data('page');
        updateStoryCards(page);
    });

    function updateStoryCards(page = 1) {

        var pageSize = window.innerWidth <= 640 ? 3 : (window.innerWidth <= 1024 ? 3 : 3);

        var data = {
            page: page,
            page_size: pageSize,
            is_active: true
        };

        $('#story-cards-container').fadeOut(400, function() {
            $.ajax({
                url: '/api/filtered-stories/',
                type: 'GET',
                data: data,
                success: function(response) {

                    $('#story-cards-container').empty();
                    if (response.results.length > 0) {
                        $.each(response.results, function(index, story) {
                        var cardHtml = `
                        <div class="col-md-4 mb-4">
                        <div class="story-card">
                            <img
                            src="${story.thumbnail || '/static/images/default_image.png'}"
                            alt="${story.title}"
                            class="img-fluid story-img"
                            onerror="this.onerror=null; this.src='/static/images/default_image.png';"
                            />
                            <h3 class="story-title">${story.title}</h3>
                            <p class="story-description">
                            ${story.body}
                            </p>
                            <a href="/stories/view/${story.id}" class="story-readmore">Read More</a>
                        </div>
                        </div>`;
                            $('#story-cards-container').append(cardHtml);
                        });
                    } else {
                        var noStoryHtml = '<div class="col-12 text-center"><p>No storys found for the selected filters.</p></div>';
                        $('#story-cards-container').append(noStoryHtml);
                    }

                    // Pagination with ellipses
                    $('#pagination').empty();
                    createPagination(page, Math.ceil(response.count / pageSize), 5);

                    $('#story-cards-container').fadeIn(400);
                },
                error: function(xhr, status, error) {
                    console.error('Error fetching storys:', error);
                    $('#story-cards-container').fadeIn(400);
                }
            });
        });
    }

});
