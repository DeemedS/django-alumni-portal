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
                jobCard.className = "save-job-card";
                jobCard.innerHTML = `
                    <div class="save-job-card-inner">
                        <h5 class="save-job-title">${jobDetails.title}</h5>
                        <p class="save-job-meta"><strong>Company:</strong> ${jobDetails.company}</p>
                        <p class="save-job-meta"><strong>Job Type:</strong> ${jobTypeMapping[jobDetails.job_type] || jobDetails.job_type}</p>
                        <p class="save-job-meta"><strong>Location:</strong> ${jobDetails.location}</p>
                        ${jobDetails.salary ? `<p class="save-job-meta"><strong>Salary:</strong> ${jobDetails.salary} PHP</p>` : ""}

                        <div class="save-job-card-footer">
                        <a href="/careers/${jobDetails.id}" class="save-job-card-btn">
                            View More
                            <svg viewBox="0 0 16 16" aria-hidden="true">
                            <path d="M6 3l4 5-4 5" fill="none" stroke="currentColor" stroke-width="2"
                                    stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                        </a>
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
