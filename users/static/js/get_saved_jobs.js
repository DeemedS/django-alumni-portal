document.addEventListener("DOMContentLoaded", async function () {
    const jobsContainer = document.getElementById("jobs-container");

    async function fetchSavedJobs() {
        try {
            const response = await fetch("/careers/userjobs/");
            if (!response.ok) {
                throw new Error("Failed to fetch saved jobs.");
            }
            return await response.json();
        } catch (error) {
            console.error("Error fetching saved jobs:", error);
            return [];
        }
    }

    async function fetchJobDetails(jobId) {
        try {
            const response = await fetch(`/api/job-details/${jobId}/`);
            if (!response.ok) {
                throw new Error(`Failed to fetch job details for ID: ${jobId}`);
            }
            return await response.json();
        } catch (error) {
            console.error("Error fetching job details:", error);
            return null;
        }
    }

    async function renderJobs(jobs) {
        jobsContainer.innerHTML = "";
    
        if (!jobs.jobs || jobs.jobs.length === 0) {
            jobsContainer.innerHTML = `<p class="text-muted">No saved jobs found.</p>`;
            return;
        }
        // Mapping of job type abbreviations to full forms
        const jobTypeMapping = {
            FT: "Full-Time",
            PT: "Part-Time",
            CT: "Contract",
            IN: "Internship",
            // Add more mappings as needed
        };

        const jobDetailsList = await Promise.all(jobs.jobs.map(job => fetchJobDetails(job.id)));
    
        jobDetailsList.forEach(jobDetails => {
            if (jobDetails) {
                const jobCard = document.createElement("div");
                jobCard.className = "col-md-4 mb-4";
                jobCard.innerHTML = `
                    <div class="card h-100 border-0 shadow-sm position-relative p-3">
                        <h5 class="card-title fw-bold">${jobDetails.title}</h5>
                        <p class="mb-1"><strong>Company:</strong> ${jobDetails.company}</p>
                        <p class="mb-1"><strong>Job Type:</strong> ${jobTypeMapping[jobDetails.job_type] || jobDetails.job_type}</p>
                        <p class="mb-1"><strong>Location:</strong> ${jobDetails.location}</p>
                        ${jobDetails.salary ? `<p class="mb-3"><strong>Salary:</strong> ${jobDetails.salary} PHP</p>` : ""}
                        <div class="mt-auto mb-2 pt-2">
                            <a href="/careers/${jobDetails.id}" class="job-card-btn">View More</a>
                        </div>
                    </div>
                `;
                jobsContainer.appendChild(jobCard);
            }
        });
    }

    const savedJobs = await fetchSavedJobs();
    await renderJobs(savedJobs);
});
