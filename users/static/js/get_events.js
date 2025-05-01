document.addEventListener("DOMContentLoaded", async function () {
    const eventsContainer = document.getElementById("events-container");
    async function fetchSavedEvents() {
        try {
            const response = await fetch("/events/userevents/");
            if (!response.ok) {
                throw new Error("Failed to fetch saved events.");
            }
            return await response.json();
        } catch (error) {
            console.error("Error fetching saved events:", error);
            return [];
        }
    }

    async function fetchEventsDetails(eventId) {
        try {
            const response = await fetch(`/api/event-details/${eventId}/`);
            if (!response.ok) {
                throw new Error(`Failed to fetch event details for ID: ${eventId}`);
            }
            return await response.json();
        } catch (error) {
            console.error("Error fetching event details:", error);
            return null;
        }
    }

    async function renderEvents(events) {
        eventsContainer.innerHTML = "";

        if (!events.events || events.events.length === 0) {
            eventsContainer.innerHTML = `<p class="text-muted">No saved events found.</p>`;
            return;
        }
        const eventDetailsList = await Promise.all(events.events.map(event => fetchEventsDetails(event.id)));

        eventDetailsList.forEach(eventDetails => {
            if (eventDetails) {
                // Parse the raw date and format it
                const rawDate = eventDetails.date;
                const eventDate = new Date(rawDate);
                const formattedDate = eventDate.toLocaleDateString("en-US", {
                    year: "numeric",
                    month: "long",
                    day: "numeric",
                });

                const sentences = eventDetails.body.split(". "); 
                let truncatedBody = sentences.slice(0, 2).join(". ");
                if (sentences.length > 2) {
                    truncatedBody += "..."; 
                }
        
                const eventCard = document.createElement("div");
                eventCard.className = "card mb-3";
                eventCard.innerHTML = `
                    <div class="card-body">
                        <div class="d-flex justify-content-between">
                            <h5 class="fw-bold">${eventDetails.title}</h5>
                            <i class="fa-solid fa-bookmark"></i>
                        </div>
                        <p class="text-muted mb-1">
                            <i class="bi bi-calendar"></i>${formattedDate}
                        </p>
                        <p>${truncatedBody}</p>
                        <a href="/events/view/${eventDetails.slug}" class="alumni-btn">View Event</a>
                    </div>
                `;
                eventsContainer.appendChild(eventCard);
            }
        });
    }

    const savedEvents = await fetchSavedEvents();
    await renderEvents(savedEvents);
});
