const backgroundClasses = [
    "blue-background",
    "pastel-wine-background",
    "pastel-ochre-background",
    "pastel-powder-blue-background",
    "pastel-indigo-background",
];

let splide;

function fetchRelatedAlumni(courseCode = null, pageSize = 10) {
    $.ajax({
        url: "/api/related-alumni",
        type: "GET",
        data: {
        page_size: pageSize,
        course_code: courseCode,
    },
    success: function (response) {
        const alumniList = response.results || [];

        // Clear existing slides manually
        const $splideList = $(".splide__list");
        $splideList.empty();

        if (alumniList.length === 0) {
            splide.add(`<li class="splide__slide"><div class="alumni-card">No alumni found.</div></li>`);
        } else {
            alumniList.forEach((alumnus, index) => {
            const backgroundClass = backgroundClasses[index % backgroundClasses.length];
            const position = alumnus.work_experience?.position || '';
            const slide = `
            <li class="splide__slide">
                <div class="alumni-card">
                    <div class="alumni-card-background ${backgroundClass}"></div>
                        <div class="alumni-card-body">
                        <img src="${alumnus.profile_image || '/static/images/default_user.jpg'}" alt="Alumnus photo" class="alumni-image">
                        <h6 class="mt-3 mb-1 alumni-name">${alumnus.first_name || 'First Name'} ${alumnus.last_name || 'Last Name'}</h6>
                        <p class="mb-3">${position || 'No Work Info'}</p>
                        <div class="alumni-details">
                            <p>${alumnus.course_code || 'BSPUP'}</p>
                            <p>SY ${alumnus.school_year || '0000-0000'}</p>
                        </div>
                    </div>
                </div>
            </li>
            `;

            splide.add(slide);
            });
        }

        // Refresh after modifying slides
        splide.refresh();
    },
    error: function (xhr, status, error) {
        console.error("Error fetching alumni:", error);
    },
    });
}