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

        var data = {
            event_filter: eventFilter,
            page: page,
            page_size: pageSize
        };

        if (monthFilter !== "0") {
            data.month = monthFilter;
        }

        if (yearFilter) {
            data.year = yearFilter;
        }



        $('#event-cards-container').fadeOut(400, function() {
            $.ajax({
                url: '/api/filtered-events/',
                type: 'GET',
                data: data,
                success: function(response) {

                    $('#event-cards-container').empty();
                    if (response.results.length > 0) {
                        $.each(response.results, function(index, event) {
                            var eventDate = new Date(event.date).toDateString();
                            var badgeClass = event.status === "Upcoming Event" ? "text-bg-success" : "text-bg-secondary";
                            var cardHtml = `<div class="card col-md-4 mb-4">
                                                <div class="position-relative">
                                                    <img src="${event.thumbnail || '/static/images/default_image.png'}" class="card-img-top" alt="${event.title}">
                                                    <div class="overlay">
                                                        <div class="badge text-bg-warning">${eventDate}</div>
                                                        <span class="badge ${badgeClass}">${event.status}</span>
                                                    </div>
                                                </div>
                                                <div class="card-body">
                                                    <h5 class="card-title">${event.title}</h5>
                                                    <p class="card-text">${event.body}</p>
                                                    <a href="/events/view/${event.slug}" class="btn btn-primary">Learn More</a>
                                                </div>
                                            </div>`;
                            $('#event-cards-container').append(cardHtml);
                        });
                    } else {
                        var noEventsHtml = '<div class="col-12 text-center"><p>No events found for the selected filters.</p></div>';
                        $('#event-cards-container').append(noEventsHtml);
                    }


                    // Pagination with ellipses
                    $('#pagination').empty();
                    createPagination(page, Math.ceil(response.count / pageSize), 5);

                    $('#event-cards-container').fadeIn(400);
                },
                error: function(xhr, status, error) {
                    console.error('Error fetching events:', error);
                    $('#event-cards-container').fadeIn(400);
                }
            });
        });
    }

});
