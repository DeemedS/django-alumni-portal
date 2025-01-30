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
                const eventCard = document.createElement("div");
                eventCard.className = "card mb-3";
                eventCard.innerHTML = `
                    <div class="card-body">
                        <h5 class="card-title">${eventDetails.title}</h5>
                        <p class="card-text">${eventDetails.body}</p>
                        <a href="/events/view/${eventDetails.slug}" class="btn btn-primary">View Event</a>
                    </div>
                `;
                eventsContainer.appendChild(eventCard);
            }
        });
    }

    const savedEvents = await fetchSavedEvents();
    await renderEvents(savedEvents);
});
