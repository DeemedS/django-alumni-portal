$(document).ready(function() {
    // Initial load of events
    updateEventCards();

    // Update event cards on filter change
    $('#event-filter, #month-filter, #year-filter').change(function() {
        updateEventCards();
    });

    function updateEventCards() {
        var eventFilter = $('#event-filter').val();
        var monthFilter = $('#month-filter').val();
        var yearFilter = $('#year-filter').val();

        $.ajax({
            url: '/api/filtered-events/',
            type: 'GET',
            data: {
                event_filter: eventFilter,
                month: monthFilter,
                year: yearFilter
            },
            success: function(response) {
                // Update event cards container with new data
                $('#event-cards-container').empty();
                $.each(response, function(index, event) {
                    var cardHtml = '<div class="card col-md-4 mb-4">';
                    cardHtml += '<img src="' + (event.thumbnail || '/static/images/default_image.png') + '" class="card-img-top" alt="' + event.title + '">';
                    cardHtml += '<div class="card-body">';
                    cardHtml += '<h5 class="card-title">' + event.title + '</h5>';

                    var truncatedBody = event.body.length > 100 ? event.body.substring(0, 100) + '...' : event.body;
                    
                    cardHtml += '<p class="card-text">' + truncatedBody + '</p>';

                    cardHtml += '<a href="/events/view/' + event.slug + '" class="btn btn-primary">View Details</a>';
                    cardHtml += '<a href="#" class="btn btn-danger">Register</a>';
                    cardHtml += '</div></div>';
                    $('#event-cards-container').append(cardHtml);
                });
            },
            error: function(xhr, status, error) {
                console.error('Error fetching events:', error);
            }
        });
    }
});