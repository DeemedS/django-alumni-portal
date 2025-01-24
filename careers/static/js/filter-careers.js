$(document).ready(function () {
    updateJobs();

    // Handle pagination
    $(document).on("click", ".page-link", function (e) {
        e.preventDefault();
        const page = $(this).data("page");
        updateJobs(page);
    });

    jobs = [];
    let currentIndex = 0;
    const jobsPerPage = 7;

    function updateJobs(page = 1) {
        const pageSize = 10;
        const data = {
            page: page,
            page_size: pageSize,
        };

        $.ajax({
            url: '/api/filtered-jobposts/',
            type: 'GET',
            data: data,
            success: function (response) {

                $('#jobs-container').empty();
                currentIndex = 0;

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
                    <h5>${job.title}</h5>
                    <p>${job.location}</p>
                `;
    
                jobContainer.appendChild(jobCard);
    
                currentIndex++;
            }
        }, 1000);
    }
    
    

    const scrollableContainer = document.getElementById("jobs-container");

    scrollableContainer.addEventListener("scroll", () => {
        const isAtBottom =
            scrollableContainer.scrollTop + scrollableContainer.clientHeight >=
            scrollableContainer.scrollHeight - 1; // Use a small margin for precision errors
    
        if (isAtBottom && currentIndex < maxJobs) {
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
                        <h3 class="card-title fw-bold mb-3">${data.title}</h3>
                        
                        <!-- Company and Posted Date -->
                        <div class="row mb-3">
                            <div class="col-md-6">
                                <p class="mb-0 text-muted"><strong>Company:</strong> ${data.company}</p>
                            </div>
                            <div class="col-md-6 text-md-end">
                                <p class="mb-0 text-muted"><strong>Posted:</strong> ${data.created_at}</p>
                            </div>
                        </div>

                        <!-- Job Details -->
                        <div class="row mb-4">
                            <div class="col-md-4 mb-2">
                                <p class="mb-0"><i class="bi bi-geo-alt"></i> <strong>Location:</strong> ${data.location}</p>
                            </div>
                            <div class="col-md-4 mb-2">
                                <p class="mb-0"><strong>Salary:</strong> <span>${formattedSalary}</span> PHP</p>
                            </div>
                            <div class="col-md-4 mb-2">
                                <p class="mb-0"><i class="bi bi-briefcase"></i> <strong>Job Type:</strong> ${data.job_type}</p>
                            </div>
                        </div>

                        <hr>
                        
                        <!-- Job Description -->
                        <div class="row mb-4 w-100">
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
                            
                            <a href="" class="btn btn-primary">Apply Now</a>
                            <a href="" class="btn btn-primary">Save Job</a>
                        



                    </div>
                </div>


            `);
        },
        error: function () {
            $(".job-description").html("<p>Failed to load job details. Please try again.</p>");
        },
    });
});