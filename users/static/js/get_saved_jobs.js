document.addEventListener("DOMContentLoaded", async function () {
    const jobsContainer = document.getElementById("jobs-container");
    const paginationContainer = document.getElementById("pagination-container"); // Make sure you have this in HTML

    const jobTypeMapping = {
        FT: "Full-Time",
        PT: "Part-Time",
        CT: "Contract",
        IN: "Internship"
    };

    async function fetchSavedJobs(page = 1) {
        try {
            const response = await fetch(`/api/careers/userjobs/?page=${page}`);
            if (!response.ok) {
                throw new Error("Failed to fetch saved jobs.");
            }
            return await response.json();
        } catch (error) {
            console.error("Error fetching saved jobs:", error);
            return null;
        }
    }

    function renderPagination(next, previous, currentPage) {
        paginationContainer.innerHTML = "";

        if (previous) {
            const prevBtn = document.createElement("button");
            prevBtn.textContent = "Previous";
            prevBtn.className = "btn btn-secondary me-2";
            prevBtn.addEventListener("click", () => loadJobs(currentPage - 1));
            paginationContainer.appendChild(prevBtn);
        }

        if (next) {
            const nextBtn = document.createElement("button");
            nextBtn.textContent = "Next";
            nextBtn.className = "btn btn-secondary";
            nextBtn.addEventListener("click", () => loadJobs(currentPage + 1));
            paginationContainer.appendChild(nextBtn);
        }
    }

    async function renderJobs(data, page) {
        jobsContainer.innerHTML = "";

        if (!data || !data.results || data.results.length === 0) {
            jobsContainer.innerHTML = `<p class="text-muted">No saved jobs found.</p>`;
            return;
        }

        data.results.forEach(job => {
            const jobCard = document.createElement("div");
            jobCard.className = "save-job-card";
            jobCard.innerHTML = `
                <div class="save-job-card-inner">
                    <h5 class="save-job-title">${job.title}</h5>
                    <p class="save-job-meta"><strong>Company:</strong> ${job.company}</p>
                    <p class="save-job-meta"><strong>Job Type:</strong> ${jobTypeMapping[job.job_type] || job.job_type}</p>
                    <p class="save-job-meta"><strong>Location:</strong> ${job.location}</p>
                    ${job.salary ? `<p class="save-job-meta"><strong>Salary:</strong> ${job.salary} PHP</p>` : ""}
                    <div class="save-job-card-footer">
                        <a href="/careers/${job.id}" class="save-job-card-btn">
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
        });

        renderPagination(data.next, data.previous, page);
    }

    async function loadJobs(page = 1) {
        const savedJobs = await fetchSavedJobs(page);
        await renderJobs(savedJobs, page);
    }

    await loadJobs(); // Initial load
});
