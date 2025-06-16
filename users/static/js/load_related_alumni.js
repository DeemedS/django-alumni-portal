const backgroundClasses = [
    "blue-background",
    "pastel-wine-background",
    "pastel-ochre-background",
    "pastel-powder-blue-background",
    "pastel-indigo-background",
];

let splide;

window.fetchRelatedAlumni = function(courseCode = null, pageSize = 10) {

    const first_name = document.getElementById("first_name").value;
    const last_name = document.getElementById("last_name").value;

    return new Promise((resolve) => {
        $.ajax({
            url: "/api/related-alumni",
            type: "GET",
            data: {
                page_size: pageSize,
                course_code: courseCode,
                first_name: first_name,
                last_name: last_name,
            },
            success: function (response) {
                const alumniList = response.results || [];
                const $splideList = $(".splide__list");
                $splideList.empty();

                if (alumniList.length === 0) {
                    splide.add(`<li class="splide__slide"><div class="alumni-card">No alumni found.</div></li>`);
                } else {
                    alumniList.forEach((alumnus, index) => {
                        const backgroundClass = backgroundClasses[index % backgroundClasses.length];
                        let position = 'No Work Info';

                        if (Array.isArray(alumnus.work_experience) && alumnus.work_experience.length > 0) {
                            const sortedExperience = alumnus.work_experience.sort((a, b) => new Date(b.startDate) - new Date(a.startDate));
                            position = sortedExperience[0]?.position || 'No Work Info';
                        }

                        const slide = `
                            <li class="splide__slide">
                                <div class="alumni-card">
                                    <div class="alumni-card-background ${backgroundClass}"></div>
                                    <div class="alumni-card-body">
                                        <img src="${alumnus.profile_image || '/static/images/default_user.jpg'}" alt="Alumnus photo" class="alumni-image">
                                        <h6 class="mt-3 mb-1 alumni-name">${alumnus.first_name || 'First Name'} ${alumnus.last_name || 'Last Name'}</h6>
                                        <p class="mb-3">${position}</p>
                                        <div class="alumni-details">
                                            <p>${alumnus.course_code || 'BSPUP'}</p>
                                            <p>BATCH ${alumnus.year_graduated || '0000'}</p>
                                        </div>
                                    </div>
                                </div>
                            </li>
                        `;
                        splide.add(slide);
                    });
                }

                splide.refresh();
                resolve(); // Signal ready
            },
            error: function (xhr, status, error) {
                console.error("Error fetching alumni:", error);
                resolve(); // Resolve to prevent blocking
            },
        });
    });
};

window.alumniDataReady = new Promise((resolve) => {
    splide = new Splide(".splide", {
        type: "loop",
        perPage: 3,
        autoplay: true,
    }).mount();

    window.fetchRelatedAlumni().then(resolve); // Fetch and then resolve
});
