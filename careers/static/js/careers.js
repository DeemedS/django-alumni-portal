    
    
    const jobs = [
        { id: 1, title: "Software Engineer", description: "Develop and maintain software." },
        { id: 2, title: "Data Analyst", description: "Analyze data trends." },
        { id: 3, title: "Web Developer", description: "Create and maintain websites." },
        { id: 4, title: "Product Manager", description: "Oversee product lifecycle." },
        { id: 5, title: "Graphic Designer", description: "Design visual assets." },
        { id: 6, title: "Network Engineer", description: "Manage network infrastructure." },
        { id: 7, title: "UX Designer", description: "Design user experiences." },
        { id: 8, title: "QA Tester", description: "Test and ensure software quality." },
        { id: 9, title: "IT Support", description: "Provide technical assistance." },
        { id: 10, title: "Database Administrator", description: "Manage databases." }
    ];

    let currentIndex = 0;
    const jobsPerPage = 7;

    function loadJobs() {
        const jobContainer = document.getElementById("job-container");
        const loader = document.getElementById("loader");

        loader.style.display = "block";

        setTimeout(() => {
            for (let i = 0; i < jobsPerPage; i++) {
                if (currentIndex >= jobs.length) {
                    loader.style.display = "none";
                    return;
                }

                const job = jobs[currentIndex];
                const jobCard = document.createElement("div");
                jobCard.className = "job-card";
                jobCard.dataset.id = job.id; // Store job id for details display
                jobCard.innerHTML = `
                    <h5>${job.title}</h5>
                    <p>${job.description}</p>
                `;
                jobCard.addEventListener("click", () => displayJobDetails(job)); // Add click event
                jobContainer.insertBefore(jobCard, loader);

                currentIndex++;
            }

            loader.style.display = "none";
        }, 1000);
    }

    function displayJobDetails(job) {
        const jobDetails = document.querySelector(".job-description");
        jobDetails.innerHTML = `
            <h2>${job.title}</h2>
            <p>Description: ${job.description}</p>
            <p>More details will go here...</p>
        `;
    }

    const scrollableContainer = document.getElementById("job-container");
    scrollableContainer.addEventListener("scroll", () => {
        if (
            scrollableContainer.scrollTop + scrollableContainer.clientHeight >=
            scrollableContainer.scrollHeight
        ) {
            loadJobs();
        }
    });

    document.addEventListener("DOMContentLoaded", loadJobs);