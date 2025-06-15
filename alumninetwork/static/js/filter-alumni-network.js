$(document).ready(function () {
    $(document).on('click', '.page-link', function (e) {
        e.preventDefault();
        const page = $(this).data('page');
        updateAlumniCards(page);
    });

    async function updateAlumniCards(page = 1) {
        const course_code = $('#course_code').val().trim() || "";
        const year_graduated = $('#year_graduated').val() || "";
        const section_code = $('#section').val()?.trim() || "";

        const pageSize = window.innerWidth <= 640 ? 5 : (window.innerWidth <= 1024 ? 10 : 20);

        $('#searching-message').removeClass('d-none').show();

        const data = {
            page,
            page_size: pageSize,
            is_active: true,
            course_code,
            year_graduated,
            section_code
        };

        $('#alumni-cards-container').fadeOut(400, async function () {
            try {
                const response = await fetchAlumniData(data);

                $('#searching-message').addClass('d-none').hide();
                $('#alumni-cards-container').empty();

                if (response.results.length > 0) {
                    response.results.forEach(alumni => {
                        const cardHtml = `
                        <div class="network-card p-0 mb-3 mt-3 mx-2">
                            <div class="network-card-background red-background"></div>
                            <div class="network-card-body">
                                <img src="${alumni.profile_image?.url || '/static/images/default_image.png'}" alt="Alumnus photo" class="alumni-image">
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
                    $('#alumni-cards-container').append(
                        '<div class="col-12 text-center"><p>No alumni found for the selected filters.</p></div>'
                    );
                }

                $('#pagination').empty();
                createPagination(page, Math.ceil(response.count / pageSize), 5);
                $('#alumni-cards-container').fadeIn(400);
            } catch (error) {
                console.error('Error fetching alumni:', error);
                $('#alumni-cards-container').fadeIn(400);
                $('#searching-message').addClass('d-none').hide();
            }
        });
    }

    async function fetchAlumniData(data) {
        return new Promise((resolve, reject) => {
            $.ajax({
                url: '/api/filtered-alumni/',
                type: 'GET',
                data,
                success: resolve,
                error: reject
            });
        });
    }

    $("#search-button").on("click", function () {
        const query = $("#search-input").val();
        updateAlumniCards(1, query);
    });

    updateAlumniCards();
});
