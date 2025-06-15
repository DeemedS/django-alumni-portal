document.addEventListener("DOMContentLoaded", async function () {
    const eventsContainer = document.getElementById("events-container");
    const paginationContainer = document.getElementById("pagination-container");

    async function fetchSavedEvents(page = 1) {
        try {
            const response = await fetch(`/api/events/userevents/?page=${page}`);
            if (!response.ok) {
                throw new Error("Failed to fetch saved events.");
            }
            return await response.json();
        } catch (error) {
            console.error("Error fetching saved events:", error);
            return null;
        }
    }

    function renderPagination(next, previous, currentPage) {
        paginationContainer.innerHTML = "";

        if (previous) {
            const prevBtn = document.createElement("button");
            prevBtn.textContent = "Previous";
            prevBtn.className = "btn btn-secondary me-2";
            prevBtn.addEventListener("click", () => loadEvents(currentPage - 1));
            paginationContainer.appendChild(prevBtn);
        }

        if (next) {
            const nextBtn = document.createElement("button");
            nextBtn.textContent = "Next";
            nextBtn.className = "btn btn-secondary";
            nextBtn.addEventListener("click", () => loadEvents(currentPage + 1));
            paginationContainer.appendChild(nextBtn);
        }
    }

    async function renderEvents(data, page) {
        eventsContainer.innerHTML = "";

        if (!data || !data.results || data.results.length === 0) {
            eventsContainer.innerHTML = `<p class="text-muted">No saved events found.</p>`;
            return;
        }

        data.results.forEach(event => {

            const rawDate = event.date;
            const eventDate = new Date(rawDate);
            const formattedDate = eventDate.toLocaleDateString("en-US", {
                year: "numeric",
                month: "long",
                day: "numeric",
            });

            const sentences = event.body.split(". "); 
            let truncatedBody = sentences.slice(0, 2).join(". ");
            if (sentences.length > 2) {
                truncatedBody += "..."; 
            }

            const eventCard = document.createElement("div");
            eventCard.className = "card mb-3";
            eventCard.innerHTML = `
                <div class="card-body">
                    <div class="d-flex justify-content-between">
                        <h5 class="fw-bold">${event.title}</h5>
                        <i class="fa-solid fa-bookmark"></i>
                    </div>
                    <p class="text-muted mb-1">
                        <i class="bi bi-calendar"></i>${formattedDate}
                    </p>
                    <p>${truncatedBody}</p>
                    <a href="/events/view/${event.slug}" class="alumni-btn">View Event</a>
                </div>
            `;
            eventsContainer.appendChild(eventCard);
        });

        renderPagination(data.next, data.previous, page);
    }

    async function loadEvents(page = 1) {
        const savedEvents = await fetchSavedEvents(page);
        await renderEvents(savedEvents, page);
    }

    await loadEvents(); // Initial load
});
