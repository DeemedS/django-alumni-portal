$(document).ready(function() {

    updateEventCards();


    $('#event-filter, #month-filter, #year-filter').change(function() {
        updateEventCards();
    });


    $(document).on('click', '.page-link', function(e) {
        e.preventDefault();
        var page = $(this).data('page');
        updateEventCards(page);
    });

    function updateEventCards(page = 1) {
        var eventFilter = $('#event-filter').val();
        var monthFilter = $('#month-filter').val();
        var yearFilter = $('#year-filter').val();

        var pageSize = window.innerWidth <= 640 ? 2 : (window.innerWidth <= 1024 ? 4 : 8);



        $('#event-cards-container').fadeOut(400, function() {
            $.ajax({
                url: '/api/filtered-events/',
                type: 'GET',
                data: {
                    event_filter: eventFilter,
                    month: monthFilter,
                    year: yearFilter,
                    page: page,
                    page_size: pageSize
                },
                success: function(response) {

                    $('#event-cards-container').empty();
                    if (response.results.length > 0) {
                        $.each(response.results, function(index, event) {
                            var cardHtml = '<div class="card col-md-4 mb-4">';
                            cardHtml += '<img src="' + (event.thumbnail || '/static/images/default_image.png') + '" class="card-img-top" alt="' + event.title + '">';
                            cardHtml += '<div class="card-body">';
                            cardHtml += '<h5 class="card-title">' + event.title + '</h5>';
                            cardHtml += '<p class="card-text">' + truncateWords(event.body, 20) + '</p>';
                            cardHtml += '<a href="/events/view/' + event.slug + '" class="btn btn-primary">Learn More</a>';
                            cardHtml += '</div></div>';
                            $('#event-cards-container').append(cardHtml);
                        });
                    } else {
                        var noEventsHtml = '<div class="col-12 text-center"><p>No events found for the selected filters.</p></div>';
                        $('#event-cards-container').append(noEventsHtml);
                    }


                    $('#pagination').empty();
                    for (var i = 1; i <= Math.ceil(response.count / pageSize); i++) {
                        var activeClass = (i === page) ? ' active' : '';
                        var pageLink = '<li class="page-item' + activeClass + '"><a class="page-link" href="#" data-page="' + i + '">' + i + '</a></li>';
                        $('#pagination').append(pageLink);
                    }

                    $('#event-cards-container').fadeIn(400);
                },
                error: function(xhr, status, error) {
                    console.error('Error fetching events:', error);
                    $('#event-cards-container').fadeIn(400);
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
