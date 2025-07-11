let combined = [];
let articlePage = 1;
let eventPage = 1;
let jobPage = 1;
let isLoading = false;
let hasMore = {
    article: true,
    event: true,
    job: true
};

let lastLoadedType = null;

function getNextType() {
    const types = ["article", "event", "job"];

    // Rotate based on last loaded type
    const startIndex = lastLoadedType ? (types.indexOf(lastLoadedType) + 1) % types.length : 0;

    for (let i = 0; i < types.length; i++) {
        const type = types[(startIndex + i) % types.length];
        if (hasMore[type]) {
            lastLoadedType = type;
            return type;
        }
    }

    return null;
}

function fetchData(pageType, page) {
    const baseUrls = {
        article: "/api/filtered-articles/",
        event: "/api/filtered-events/",
        job: "/api/filtered-jobposts/"
    };

    return $.get(`${baseUrls[pageType]}?page=${page}&page_size=3&is_active=true`)
        .then(res => res.results.map(item => ({
            ...item,
            type: pageType,
            created_at: new Date(item.created_at),
        })))
        .catch(() => {
            hasMore[pageType] = false;
            return [];  // return empty array on failure
        });
}

function renderCard(item, index) {
    if (item.type === "article" || item.type === "event") {
        const title = item.title ?? "Untitled";
        const body = item.body ?? "";
        const likeCount = item.like_count ?? 0;
        const isLong = body.split(/\s+/).length > 50;
        const imageUrl = item.type === "article" ? (item.thumbnail || "/static/images/default_image.png") : (item.banner || "/static/images/default_image.png");
        const label = item.type === "article" ? "NEWS & ANNOUNCEMENT" : "EVENT";
        

        return `
            <div class="card card-custom mb-3 mt-3">
                <div class="card-body mb-0">
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
                    <pre class="mb-0 body-text white-space-pre-wrap" data-index="${index}">${
                        isLong 
                        ? getPreviewByWords(body, 35) + '<span class="see-more pointer text-blue-600">See more</span>' 
                        : escapeHtml(body)
                    }</pre>
                    <div class="card-img">
                        <img src="${imageUrl}" alt="Preview Image" class="mb-3">
                    </div>
                </div>
                <div>
                <div class="d-flex justify-content-between align-items-center text-muted">
                    <small class="text-muted px-3 mb-2">
                        <i class="fa-solid fa-heart me-1"></i>
                        <span class="like-number">${likeCount}</span> Likes
                    </small>
                </div>
                </div>
                <div class="border-top d-flex justify-content-around text-muted py-2 interaction-bar">
                    <div class="like-btn"
                        data-id="${item.id}"
                        data-type="${item.type}"
                        data-liked="${item.is_liked}">
                        <i class="${item.is_liked ? 'fa-solid text-danger' : 'fa-regular'} fa-heart me-1"></i>
                        Like
                    </div>
                    <div class="pointer send-button"
                        data-link="${   
                            item.type === 'event'
                                ? `https://alumniportal.guianalankem.com/events/view/${item.slug}`
                                : `https://alumniportal.guianalankem.com/articles/view/${item.slug}`
                        }">
                        <i class="fa fa-paper-plane me-1" id="send"></i>Send
                    </div>
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
        const applyUrl = item.id || "#";
        const likeCount = item.like_count || 0 ;


        return `
            <div class="card card-custom mb-3 mt-3">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <div class="d-flex align-items-center gap-2">
                            <div class="card-profile-img">
                                <img src="${companyLogo}" alt="Company Logo">
                            </div>
                            <div>
                                <h6 class="mb-0">ARCDO</h6>
                                <small class="text-muted">Jobs</small>
                            </div>
                        </div>
                    </div>
                    <div class="job-card-content">
                        <div class="job-card-company">
                            <img src="${companyLogo}" alt="Company Logo">
                        </div>
                        <div class="job-card-details">
                            <h3 class="job-card-title">${jobTitle}</h3>
                            <p><i class="fa-solid fa-building me-1"></i>${companyName}</p>
                            <p class="job-card-location"><i class="fa-solid fa-location-dot me-1"></i>${location}</p>
                            <p><i class="fa-solid fa-briefcase me-1"></i>Job Type: ${jobType}</p>
                            <p><i class="fa-solid fa-dollar-sign me-1"></i>Salary: ${salary}</p>
                        </div>
                        <div class="job-card-button">
                            <a href="/careers/${applyUrl}" target="_blank" rel="noopener noreferrer">Apply Now</a>
                        </div>
                    </div>
                </div>
                <div class="d-flex justify-content-between align-items-center text-muted">
                    <small class="text-muted px-3 mb-2">
                        <i class="fa-solid fa-heart me-1"></i>
                        <span class="like-number">${likeCount}</span> Likes
                    </small>
                </div>
                <div class="border-top d-flex justify-content-around text-muted py-2 interaction-bar">
                    <div class="like-btn"
                        data-id="${item.id}"
                        data-type="${item.type}"
                        data-liked="${item.is_liked}">
                        <i class="${item.is_liked ? 'fa-solid text-danger' : 'fa-regular'} fa-heart me-1"></i>
                        Like
                    </div>
                    <div><i class="fa-regular fa-bookmark me-1"></i>Save Job</div>
                    <div class="pointer send-button" data-link="https://alumniportal.guianalankem.com/careers/${item.id}">
                    <i class="fa fa-paper-plane me-1" id="send"></i>Send</div>
                </div>
            </div>
        `;
    }

    return '';
}

function loadMore() {
    if (isLoading || (!hasMore.article && !hasMore.event && !hasMore.job)) return;

    isLoading = true;

    const nextType = getNextType();

    if (!nextType) {
        isLoading = false;
        return;
    }

    const pageMap = { article: articlePage, event: eventPage, job: jobPage };

    fetchData(nextType, pageMap[nextType])
        .then(items => {
            if (items.length > 0) {
                if (nextType === "article") articlePage++;
                if (nextType === "event") eventPage++;
                if (nextType === "job") jobPage++;
            } else {
                hasMore[nextType] = false;
            }

            const startIndex = combined.length;
            items.sort((a, b) => b.created_at - a.created_at);
            combined.push(...items);
            const container = $("#news-feed-container");
            items.forEach((item, i) => {
                container.append(renderCard(item, startIndex + i));
            });
        })
        .catch(() => {
            hasMore[nextType] = false;
        })
        .always(() => {
            isLoading = false;
        });
}

$(document).ready(function () {
    window.alumniDataReady.then(() => {
        loadMore(); // Initial load
    });
});

let scrollTimeout;
$(window).on("scroll", function () {
    if (scrollTimeout) return;
    scrollTimeout = setTimeout(() => {
        scrollTimeout = null;

        const scrollTop = $(window).scrollTop();
        const windowHeight = $(window).height();
        const documentHeight = $(document).height();
        const scrollPercent = (scrollTop + windowHeight) / documentHeight;

        if (scrollPercent >= 0.8 && (hasMore.article || hasMore.event || hasMore.job)) {
            loadMore();
        }
    }, 200); // throttle delay
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
    const lines = text.split('\n');
    let count = 0;
    let preview = [];

    for (const line of lines) {
        if (line.trim() === "") {
            preview.push("");
            continue;
        }

        const words = line.trim().split(/\s+/);
        if (count + words.length <= maxWords) {
            preview.push(line);
            count += words.length;
        } else {
            preview.push(words.slice(0, maxWords - count).join(" "));
            break;
        }
    }

    return preview.join('\n') + "...";
}

function escapeHtml(unsafe) {
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");
}


$("#news-feed-container").on("click", ".like-btn", function () {
    const $btn = $(this);
    const itemId = $btn.data("id");
    const itemType = $btn.data("type");
    const $icon = $btn.find("i");
    const $count = $btn.closest(".card").find(".like-number");
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]')?.value;

    $.ajax({
        url: `/api/${itemType}${itemType === 'job' ? 'posts' : 's'}/${itemId}/like/`,
        type: "POST",
        headers: { "X-CSRFToken": csrfToken },
        success: function (res) {
            $count.text(res.like_count);
            $btn.data("liked", res.liked);
            $icon
                .toggleClass("fa-solid text-danger", res.liked)
                .toggleClass("fa-regular", !res.liked);
        },
        error: function () {
            alert("Please log in to like this item.");
        }
    });
});

$("#news-feed-container").on("click", ".send-button", function () {
    handleSend(this);
});
