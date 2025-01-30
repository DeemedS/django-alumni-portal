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
        const jobDetailsList = await Promise.all(jobs.jobs.map(job => fetchJobDetails(job.id)));
    
        jobDetailsList.forEach(jobDetails => {
            if (jobDetails) {
                const jobCard = document.createElement("div");
                jobCard.className = "card mb-3";
                jobCard.innerHTML = `
                    <div class="card-body">
                        <h5 class="card-title">${jobDetails.title}</h5>
                        <p class="card-text">${jobDetails.company}</p>
                        <a href="/careers/${jobDetails.id}" class="btn btn-primary">View Job</a>
                    </div>
                `;
                jobsContainer.appendChild(jobCard);
            }
        });
    }

    const savedJobs = await fetchSavedJobs();
    await renderJobs(savedJobs);
});
