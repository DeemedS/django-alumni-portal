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
            is_active: true
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
                            <h5 class="card-title pup-red"">${job.title}</h5>
                            
                            <!-- Company Name -->
                            <p class="card-text">
                                <i class="bi bi-building"></i>${job.company}
                            </p>

                                                        <p class="card-text">
                                <i class="bi bi-building"></i>${job.description}
                            </p>

                            <!-- Job Location -->
                            <p class="card-text text-muted mb-1">
                                <i class="bi bi-geo-alt-fill"></i>${job.location}
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
        const threshold = 10; // pixels from bottom
        if (
          scrollableContainer.scrollTop + scrollableContainer.clientHeight >=
          scrollableContainer.scrollHeight - threshold
        ) {
          loadJobs();
        }
      });

    document.addEventListener("DOMContentLoaded", loadJobs);
});


$(document).on("click", ".job-card", function (e) {
    e.preventDefault();

    const jobId = $(this).attr("data");

    if ($(window).width() <= 576) {
        window.location.href = `/careers/${jobId}`;
        return;
    }

    // Fetch saved jobs first
    $.ajax({
        url: "/careers/userjobs/",
        method: "GET",
        success: function (savedJobsData) {
            const savedJobIds = savedJobsData.jobs.map(job => job.id); 

            // Now fetch job details after getting saved jobs
            $.ajax({
                url: `/api/job-details/${jobId}/`,
                method: "GET",
                success: function (data) {
                    const date = new Date(data.created_at);
                    data.created_at = date.toDateString();

                    // Format salary or salary range
                    let formattedSalary = "";
                    if (typeof data.salary === "string" && data.salary.includes("-")) {
                        // Handle range
                        const [min, max] = data.salary.split("-").map(s => s.trim());
                        if (!isNaN(min) && !isNaN(max)) {
                            const formattedMin = new Intl.NumberFormat('en-PH', { minimumFractionDigits: 0 }).format(Number(min));
                            const formattedMax = new Intl.NumberFormat('en-PH', { minimumFractionDigits: 0 }).format(Number(max));
                            formattedSalary = `${formattedMin} - ${formattedMax}`;
                        } else {
                            formattedSalary = data.salary; // fallback if not numbers
                        }
                    } else if (data.salary && !isNaN(data.salary)) {
                        // Handle single value
                        formattedSalary = new Intl.NumberFormat('en-PH', { minimumFractionDigits: 0 }).format(Number(data.salary));
                    }

                    // Map job type abbreviations to full meanings
                    const jobTypeMap = {
                        "FT": "Full-Time",
                        "PT": "Part-Time",
                        "IN": "Internship",
                        "CT": "Contract",
                        // Add more as needed
                    };
                    const jobTypeFull = jobTypeMap[data.job_type] || data.job_type;


                    // Check if the job is saved
                    const isSaved = savedJobIds.includes(data.id);
                    const saveButtonText = isSaved ? "Unsave Job" : "Save Job";
                    const saveButtonClass = isSaved ? "btn-danger unsave-job-btn" : "btn-outline-danger save-job-btn";

                    $(".job-description").html(`
                        <div class="card mb-4">
                            <div class="card-body">
                                <h3 class="card-title fw-bold mb-4 pup-red">${data.title}</h3>
                                
                                <div class="row mb-4">
                                    <div class="col-md-6">
                                        <p class="mb-0 text-muted"><strong>Posted:</strong> ${data.created_at}</p>
                                    </div>
                                </div>

                                <div class="row mb-4">
                                    <div class="col-md-6">
                                        <p class="mb-0 text-muted"><strong>Company:</strong> ${data.company}</p>
                                    </div>
                                </div>

                                <div class="row mb-4">
                                    <div class="col-md-6">
                                        <p class="mb-0 text-muted"><strong>Email:</strong> ${data.company_email}</p>
                                    </div>
                                </div>
                                <div class="row mb-4">
                                    <div class="col-md-6">
                                        ${data.company_contact ? `<p class="mb-0 text-muted"><strong>Contact:</strong> ${data.company_contact}</p>` : ''}
                                    </div>
                                </div>

                                <div class="row mb-4">
                                    <div class="col-md-4 mb-3 mb-md-0 d-flex align-items-center">
                                        <span><strong>Location:</strong> ${data.location}</span>
                                    </div>
                                    <div class="col-md-4 mb-3 mb-md-0 d-flex align-items-center">
                                        ${formattedSalary
                                            ? `<span><strong>Salary:</strong> <span class="text-success">₱${formattedSalary}</span></span>`
                                            : `<span><strong>Salary:</strong> <span class="text-muted">Not specified</span></span>`
                                        }
                                    </div>
                                    <div class="col-md-4 d-flex align-items-center">
                                        <span><strong>Job Type:</strong> ${jobTypeFull}</span>
                                    </div>
                                </div>

                                <hr>

                                <div class="row mb-4">
                                    <h4 class="fw-semibold">Job Description</h4>
                                    <pre class="text-secondary">${data.description}</pre>
                                </div>

                                ${data.responsibilities ? `
                                <div class="row mb-4">
                                    <h4 class="fw-semibold">Job Responsibilities</h4>
                                    <pre class="text-secondary">${data.responsibilities}</pre>
                                </div>
                                ` : ''}

                                ${data.qualifications ? `
                                <div class="row mb-4">
                                    <h4 class="fw-semibold">Job Qualifications</h4>
                                    <pre class="text-secondary">${data.qualifications}</pre>
                                </div>
                                ` : ''}

                                ${data.benefits ? `
                                <div class="row mb-4">
                                    <h4 class="fw-semibold">Job Benefits</h4>
                                    <pre class="text-secondary">${data.benefits}</pre>
                                </div>
                                ` : ''}

                                <div class="d-flex justify-content-start gap-3">
                                    <a href="/careers/${data.id}" class="btn red-careers-btn">View</a>
                                    <button class="btn ${saveButtonClass}" data-id="${data.id}">${saveButtonText}</button>
                                </div>
                            </div>
                        </div>
                    `);
                },
                error: function () {
                    $(".job-description").html("<p>Failed to load job details. Please try again.</p>");
                },
            });
        },
        error: function () {
            console.error("Failed to load saved jobs.");
        }
    });
});


// Handle Save Job Button Click
$(document).on("click", ".save-job-btn", function () {
    const jobId = $(this).attr("data-id");
    const button = $(this);
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]')?.value;

    $.ajax({
        url: `/careers/save_job/${jobId}/`,
        method: "POST",
        headers: {
            "X-CSRFToken": csrfToken
        },
        success: function (response, status, xhr) {
            if (xhr.status === 201) {
                showToast('Success', 'Job saved successfully!', 'success');
                button.text("Unsave Job").removeClass("btn-outline-danger save-job-btn").addClass("btn-danger unsave-job-btn");
            } else if (xhr.status === 200) {
                message = `<p class="text-info">.</p>`;
                showToast('Success', 'Job is already saved', 'success');  
            }
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
        }
    });
});



$(document).on("click", ".unsave-job-btn", function () {
    const jobId = $(this).attr("data-id");
    const button = $(this);
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]')?.value;

    $.ajax({
        url: `/careers/unsave_job/${jobId}/`,
        method: "POST",
        headers: {
            "X-CSRFToken": csrfToken
        },
        success: function (response, status, xhr) {
            if (xhr.status === 200) { 
                showToast('Success', 'Job removed successfully!', 'success');
                button.text("Save Job").removeClass("btn-danger unsave-job-btn").addClass("btn-outline-danger save-job-btn");
            } 
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
        }
    });
});
