$(document).ready(function () {
    updateJobs();

    // Handle pagination
    $(document).on("click", ".page-link", function (e) {
        e.preventDefault();
        const page = $(this).data("page");
        updateJobs(page);
    });
    // Handle form submission
    $("#job-search-form").on("submit", function (e) {
        e.preventDefault();
        updateJobs(1);
    });


    jobs = [];
    let currentIndex = 0;
    const jobsPerPage = 7;

    function updateJobs(page = 1) {
        const pageSize = 10;

        //get form data
        const keyword = $("#keyword").val();
        const location = $("#location").val();
        const jobType = $("#job_type").val();

        const data = {
            page: page,
            page_size: pageSize,
            keyword: keyword,
            location: location,
            job_type: jobType,
        };

        $.ajax({
            url: '/api/filtered-jobposts/',
            type: 'GET',
            data: data,
            success: function (response) {

                $('#jobs-container').empty();
                currentIndex = 0;

                // Check if there are any job posts in the response
                if (response.results.length === 0) {
                    $('#jobs-container').html(`
                        <div class="alert alert-warning" role="alert">
                            No job posts found matching your criteria.
                        </div>
                    `);
                    return; // Exit early, as there are no results to display
                }

                jobs = response.results;
                loadJobs();

                $('#pagination').empty();
                createPagination(page, Math.ceil(response.count / pageSize), 5);

            },
            error: function (xhr, status, error) {
                console.log("Error fetching jobs:", error);
            }
        });
    }

    function loadJobs() {

        const jobContainer = document.getElementById("jobs-container");
        const loader = document.getElementById("loader");
        const pagination = document.getElementById("pagination-controls");


        maxJobs = jobs.length;
    
        loader.style.display = "block";
        pagination.style.display = "none";
    
        setTimeout(() => {

            loader.style.display = "none";

            for (let i = 0; i < jobsPerPage; i++) {

                if (currentIndex >= jobs.length) {
                    pagination.style.display = "flex";
                }
    
                const job = jobs[currentIndex];
                const jobCard = document.createElement("div");
                jobCard.className = "job-card";
                jobCard.setAttribute("data", job.id);
                jobCard.innerHTML = `
                    <div class="card mb-3 shadow-sm">
                        <div class="card-body">
                            <!-- Job Title -->
                            <h5 class="card-title" style="color: #800000;">${job.title}</h5>
                            
                            <!-- Company Name -->
                            <p class="card-text">
                                <i class="bi bi-building me-2"></i>${job.company}
                            </p>

                            <!-- Job Location -->
                            <p class="card-text text-muted mb-1">
                                <i class="bi bi-geo-alt-fill me-2"></i>${job.location}
                            </p>
                        </div>
                    </div>

                `;
    
                jobContainer.appendChild(jobCard);
    
                currentIndex++;
            }
        }, 1000);
    }
    
    

    const scrollableContainer = document.getElementById("jobs-container");
    scrollableContainer.addEventListener("scroll", () => {


        if (
            scrollableContainer.scrollTop + scrollableContainer.clientHeight >=
            scrollableContainer.scrollHeight && currentIndex < maxJobs
        ) {
            loadJobs();
        }
    });

    document.addEventListener("DOMContentLoaded", loadJobs);
});


$(document).on("click", ".job-card", function (e) {
    e.preventDefault(); 

    const jobId = $(this).attr("data");

    $.ajax({
        url: `/api/job-details/${jobId}/`, // API endpoint to fetch job details
        method: "GET",
        success: function (data) {
            const date = new Date(data.created_at);
            data.created_at = date.toDateString();

            const salary = data.salary; // Example: 50000

            // Format the salary with commas
            const formattedSalary = new Intl.NumberFormat('en-US', {
                minimumFractionDigits: 0, // Optional: no decimal places
            }).format(salary);
            
            $(".job-description").html(` <!-- Inject job details into the .job-description div -->
                
                <div class="card border-0 shadow-sm mb-4">
                    <div class="card-body">
                        <!-- Job Title -->
                        <h3 class="card-title fw-bold mb-4" style="color: #800000;">${data.title}</h3>

                        <!-- Company and Posted Date -->
                        <div class="row mb-4">
                            <div class="col-md-6">
                                <p class="mb-0 text-muted"><strong>Company:</strong> ${data.company}</p>
                            </div>
                            <div class="col-md-6 text-md-end">
                                <p class="mb-0 text-muted"><strong>Posted:</strong> ${data.created_at}</p>
                            </div>
                        </div>

                        <!-- Job Details -->
                        <div class="row mb-4">
                            <div class="col-md-4 mb-3 mb-md-0">
                                <p class="mb-0"><i class="bi bi-geo-alt"></i> <strong>Location:</strong> ${data.location}</p>
                            </div>
                            <div class="col-md-4 mb-3 mb-md-0">
                                <p class="mb-0"><strong>Salary:</strong> <span>${formattedSalary}</span> PHP</p>
                            </div>
                            <div class="col-md-4">
                                <p class="mb-0"><i class="bi bi-briefcase"></i> <strong>Job Type:</strong> ${data.job_type}</p>
                            </div>
                        </div>

                        <hr>

                        <!-- Job Description -->
                        <div class="row mb-4">
                            <h4 class="fw-semibold">Job Description</h4>
                            <pre class="text-secondary">${data.description}</pre>
                        </div>

                        <!-- Job Responsibilities -->
                        ${data.responsibilities ? `
                        <div class="row mb-4">
                            <h4 class="fw-semibold">Job Responsibilities</h4>
                            <pre class="text-secondary">${data.responsibilities}</pre>
                        </div>
                        ` : ''}

                        <!-- Job Qualifications -->
                        ${data.qualifications ? `
                        <div class="row mb-4">
                            <h4 class="fw-semibold">Job Qualifications</h4>
                            <pre class="text-secondary">${data.qualifications}</pre>
                        </div>
                        ` : ''}

                        <!-- Job Benefits -->
                        ${data.benefits ? `
                        <div class="row mb-4">
                            <h4 class="fw-semibold">Job Benefits</h4>
                            <pre class="text-secondary">${data.benefits}</pre>
                        </div>
                        ` : ''}

                        <!-- Action Buttons -->
                        <div class="d-flex justify-content-start gap-3">
                            <a href="/careers/${data.id}" class="btn" style="background-color: #800000; color: white;">Apply Now</a>
                            <button class="btn btn-outline-danger save-job-btn" data-id="${data.id}">Save Job</button>
                        </div>
                    </div>
                </div>


            `);
        },
        error: function () {
            $(".job-description").html("<p>Failed to load job details. Please try again.</p>");
        },
    });
});

// Handle Save Job Button Click
$(document).on("click", ".save-job-btn", function () {
    const jobId = $(this).attr("data-id");

    $.ajax({
        url: `/careers/save_job/${jobId}/`,
        method: "POST",
        headers: {
            "X-CSRFToken": getCsrfToken()
        },
        success: function (response, status, xhr) {
            let message = "";
            if (xhr.status === 201) {
                showToast('Success', 'Job saved successfully!', 'success');  
            } else if (xhr.status === 200) {
                message = `<p class="text-info">.</p>`;
                showToast('Success', 'Job is already saved', 'success');  
            }

            $("#save-job-message").html(message);
        },
        error: function (xhr) {
            if (xhr.status === 401) {
                showToast('No User Found', 'You need to log in to save jobs.', 'warning');  
            } else if (xhr.status === 403) {
                showToast('No User Found', 'Please try logging in again.', 'warning');  
            } else if (xhr.status === 404) {
                showToast('Job not found', 'Job not found.', 'danger');  
            } else if (xhr.status === 500) {
                showToast('ServerError', 'Server error. Please try again later.', 'danger');  
            }

            $("#save-job-message").html(message);
        }
    });
});

function getCsrfToken() {
    const cookieValue = document.cookie
        .split("; ")
        .find(row => row.startsWith("csrftoken="))
        ?.split("=")[1];
    return cookieValue || "";
}

