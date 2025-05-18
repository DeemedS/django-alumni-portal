let combined = [];

$(document).ready(function () {
    const articleUrl = "/api/filtered-articles/?page_size=10&is_active=true";
    const eventUrl = "/api/filtered-events/?page_size=10&is_active=true";
    const jobUrl = "/api/filtered-jobposts/?page_size=10&is_active=true";

    $.when($.get(articleUrl), $.get(eventUrl), $.get(jobUrl))
        .done(function (articleResponse, eventResponse, jobResponse) {
            const articles = articleResponse[0]?.results.map(item => ({
                ...item,
                type: "article",
                created_at: new Date(item.created_at),
            })) || [];

            const events = eventResponse[0]?.results.map(item => ({
                ...item,
                type: "event",
                created_at: new Date(item.created_at),
            })) || [];

            const jobs = jobResponse[0]?.results.map(item => ({
                ...item,
                type: "job",
                created_at: new Date(item.created_at),
            })) || [];

            combined = [...articles, ...events, ...jobs]  // 2. Assign combined here
                .sort((a, b) => b.created_at - a.created_at)
                .slice(0, 30);

            const container = $("#news-feed-container").empty();

            combined.forEach((item, index) => {
                let cardHTML = "";

                if (item.type === "article" || item.type === "event") {
                    const title = item.title || (item.type === "article" ? "Untitled" : "Untitled Event");
                    const body = item.body || "";
                    const isLong = body.split(/\s+/).length > 50;
                    const imageUrl = item.type === "article" ? (item.thumbnail || "/static/images/arcdologo.jpg") : (item.banner || "/static/images/arcdologo.jpg");
                    const label = item.type === "article" ? "NEWS & ANNOUNCEMENT" : "EVENT";

                    cardHTML = `
                        <div class="card card-custom mb-3 mt-3">
                            <div class="card-body">
                                <div class="d-flex justify-content-between align-items-center mb-3">
                                    <div class="d-flex align-items-center gap-2">
                                        <div class="card-profile-img">
                                            <img src="/static/images/arcdologo.jpg" alt="ARCDO logo">
                                        </div>
                                        <div>
                                            <h6 class="mb-0">ARCDO</h6>
                                            <small class="text-muted">${label}</small>
                                        </div>
                                    </div>
                                </div>
                                <div class="card-title">
                                    <strong>${title}</strong><br>
                                </div>
                                <pre class="mb-0 body-text" data-index="${index}" style="white-space:pre-wrap;">${
                                    isLong 
                                    ? getPreviewByWords(body, 35) + '<span class="see-more" style="color:blue;cursor:pointer;">See more</span>' 
                                    : escapeHtml(body)
                                }</pre>

                                
                                <div class="card-img">
                                    <img src="${imageUrl}" alt="Preview Image" onerror="this.onerror=null;this.src='/static/images/default_image.png';" class="mb-3">
                                </div>
                            </div>
                            <div class="border-top d-flex justify-content-around text-muted py-2 interaction-bar">
                                <div><i class="fa-regular fa-heart me-1"></i>Like</div>
                                <div><i class="fa fa-paper-plane me-1"></i>Send</div>
                            </div>
                        </div>
                    `;
                } else if (item.type === "job") {
                    const companyLogo = item.company_logo || "/static/images/arcdologo.jpg";
                    const jobTitle = item.title || "Untitled Job";
                    const companyName = item.company || "Unknown Company";
                    const location = item.location || "Location not specified";
                    const jobType = item.job_type || "N/A";
                    const salary = item.salary ? item.salary + " PHP" : "Not specified";
                    const applyUrl = item.apply_url || "#";

                    cardHTML = `
                        <div class="card card-custom mb-3 mt-3">
                            <div class="card-body">
                                <div class="d-flex justify-content-between align-items-center mb-3">
                                    <div class="d-flex align-items-center gap-2">
                                        <div class="card-profile-img">
                                            <img src="${companyLogo}" alt="Company Logo" onerror="this.onerror=null;this.src='/static/images/arcdologo.jpg';">
                                        </div>
                                        <div>
                                            <h6 class="mb-0">ARCDO</h6>
                                            <small class="text-muted">Jobs</small>
                                        </div>
                                    </div>
                                </div>
                                <div class="job-card-content">
                                    <div class="job-card-company">
                                        <img src="${companyLogo}" alt="Company Logo" onerror="this.onerror=null;this.src='/static/images/arcdologo.jpg';">
                                    </div>
                                    <div class="job-card-details">
                                        <h3 class="job-card-title">${jobTitle}</h3>
                                        <p><i class="fa-solid fa-building me-1"></i>${companyName}</p>
                                        <p class="job-card-location"><i class="fa-solid fa-location-dot me-1"></i>${location}</p>
                                        <p><i class="fa-solid fa-briefcase me-1"></i>Job Type: ${jobType}</p>
                                        <p><i class="fa-solid fa-dollar-sign me-1"></i>Salary: ${salary}</p>
                                    </div>
                                    <div class="job-card-button">
                                        <a href="${applyUrl}" target="_blank" rel="noopener noreferrer">Apply Now</a>
                                    </div>
                                </div>
                            </div>
                            <div class="border-top d-flex justify-content-around text-muted py-2 interaction-bar">
                                <div><i class="fa-regular fa-heart me-1"></i>Like</div>
                                <div><i class="fa-regular fa-bookmark me-1"></i>Save Job</div>
                                <div><i class="fa fa-paper-plane me-1"></i>Send</div>
                            </div>
                        </div>
                    `;
                }

                container.append(cardHTML);
            });
        })
        .fail(function () {
            console.error("Failed to fetch some feed content.");
            $("#news-feed-container").html(`<p class="text-danger">Failed to load content. Please try again later.</p>`);
        });
});

$("#news-feed-container").on("click", ".see-more", function () {
    const $pre = $(this).closest("pre");
    const index = $pre.data("index");
    const item = combined[index];
    if (!item) return;

    const fullText = item.body || "";

    if ($(this).text().trim() === "See less") {
        const previewText = getPreviewByWords(fullText, 35);
        $pre.html(`${escapeHtml(previewText)}<span class="see-more">See more</span>`);
    } else {
        $pre.html(`${escapeHtml(fullText)}\n<span class="see-more">See less</span>`);
    }
});



function getPreviewByWords(text, maxWords = 30) {
    const lines = text.split('\n'); // preserve lines
    let wordCount = 0;
    let resultLines = [];

    for (const line of lines) {
        const trimmedLine = line.trim();
        const words = trimmedLine.split(/\s+/);

        if (trimmedLine === "") {
            // preserve empty line but don't add to word count
            resultLines.push("");
            continue;
        }

        if (wordCount + words.length <= maxWords) {
            resultLines.push(line); // keep original line with spacing
            wordCount += words.length;
        } else {
            // Add only the remaining words from this line
            const remaining = maxWords - wordCount;
            const partialLine = words.slice(0, remaining).join(' ');
            resultLines.push(partialLine);
            break;
        }
    }

    return resultLines.join('\n') + '...';
}

function escapeHtml(unsafe) {
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");
}
