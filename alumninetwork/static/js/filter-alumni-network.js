$(document).ready(function() {

    $(document).on('click', '.page-link', function(e) {
        e.preventDefault();
        var page = $(this).data('page');
        updateAlumniCards(page);
    });

    function updateAlumniCards(page = 1) {

        let course_code = $('#course_code').val().trim() || "";
        let year_graduated = $('#year_graduated').val() || "";
        let section_code = $('#section').val()?.trim() || "";

        var pageSize = window.innerWidth <= 640 ? 5 : (window.innerWidth <= 1024 ? 10 : 20);

        $('#searching-message').removeClass('d-none').show();

        var data = {
            page: page,
            page_size: pageSize,
            is_active: true,
            course_code: course_code,
            year_graduated: year_graduated,
            section_code: section_code
        };

        $('#alumni-cards-container').fadeOut(400, function() {
            $.ajax({
                url: '/api/filtered-alumni/',
                type: 'GET',
                data: data,
                success: function(response) {

                    $('#searching-message').addClass('d-none').hide();

                    $('#alumni-cards-container').empty();
                    if (response.results.length > 0) {
                        $.each(response.results, function(index, alumni) {
                        var cardHtml = `
                        <div class="network-card p-0 mb-3 mt-3 mx-2">
                            <div class="network-card-background red-background"></div>
                            <div class="network-card-body">
                                <img src="${alumni.profile_image.url || '/static/images/default_image.png'}" alt="Alumnus photo" class="alumni-image">
                                <div class="network-details">
                                    <h6 class="mt-3 mb-3 alumni-name">${alumni.first_name} ${alumni.last_name}</h6>
                                   <p class="mb-1">${alumni.course_code || ''}${alumni.section_code ? ` - ${alumni.section_code}` : ''}</p>
                                    <p class="mb-1">BATCH ${alumni.year_graduated || ''}</p>
                                    <p class="mb-3">${alumni.position || ''}</p>
                                </div>
                                <div class="network-icons mb-3">
                                    <a href="${alumni.facebook_link || '#'}"><i class="fa-brands fa-facebook"></i></a>
                                    <a href="${alumni.x_link || '#'}"><i class="fa-brands fa-square-x-twitter"></i></a>
                                    <a href="${alumni.linkedin_link || '#'}"><i class="fa-brands fa-linkedin"></i></a>
                                </div>
                            </div>
                        </div>`;
                            $('#alumni-cards-container').append(cardHtml);
                        });
                    } else {
                        var noAlumniHtml = '<div class="col-12 text-center"><p>No alumni found for the selected filters.</p></div>';
                        $('#alumni-cards-container').append(noAlumniHtml);
                    }

                    // Pagination with ellipses
                    $('#pagination').empty();
                    createPagination(page, Math.ceil(response.count / pageSize), 5);

                    $('#alumni-cards-container').fadeIn(400);
                },
                error: function(xhr, status, error) {
                    console.error('Error fetching alumnis:', error);
                    $('#alumni-cards-container').fadeIn(400);
                    $('#searching-message').addClass('d-none').hide();
                }
            });
        });
    }

        // Search on button click
    $("#search-button").on("click", function () {
        const query = $("#search-input").val();
        page = 1;
        updateAlumniCards(page, query);
    });

    updateAlumniCards();
});
