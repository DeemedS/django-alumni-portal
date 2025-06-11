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
        const title = item.title || (item.type === "article" ? "Untitled" : "Untitled Event");
        const body = item.body || "";
        const isLong = body.split(/\s+/).length > 50;
        const imageUrl = item.type === "article" ? (item.thumbnail || "/static/images/arcdologo.jpg") : (item.banner || "/static/images/arcdologo.jpg");
        const label = item.type === "article" ? "NEWS & ANNOUNCEMENT" : "EVENT";
        const likeCount = item.like_count || 0;

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
                    <div class="pointer" onclick="handleSend(this)" data-link="https://alumniportal.guianalankem.com/${item.type}/${item.id}">
                    <i class="fa fa-paper-plane me-1" id="send"></i>Send</div>
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
                    <div class="pointer" onclick="handleSend(this)" data-link="https://alumniportal.guianalankem.com/careers/${item.id}">
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

    const promises = [];
    if (hasMore.article) promises.push(fetchData("article", articlePage));
    if (hasMore.event) promises.push(fetchData("event", eventPage));
    if (hasMore.job) promises.push(fetchData("job", jobPage));

    Promise.all(promises).then(results => {
        const [articles = [], events = [], jobs = []] = results;

        if (articles.length > 0) articlePage++;
        else hasMore.article = false;

        if (events.length > 0) eventPage++;
        else hasMore.event = false;

        if (jobs.length > 0) jobPage++;
        else hasMore.job = false;

        const newItems = [...articles, ...events, ...jobs]
            .sort((a, b) => b.created_at - a.created_at);

        const container = $("#news-feed-container");
        newItems.forEach(item => {
            combined.push(item);
            const index = combined.length - 1;
            container.append(renderCard(item, index));
            $('#news-feed-container img').on('error', function() {
                if (!this.src.includes('default_image.png')) {
                    this.src = '/static/images/default_image.png';
                }
            });
        });

        isLoading = false;
    }).catch(() => {
        isLoading = false;
        console.error("Error loading data.");
    });
}

$(document).ready(function () {
    loadMore(); // Initial load
});

$(window).on("scroll", function () {
    const scrollTop = $(window).scrollTop();
    const windowHeight = $(window).height();
    const documentHeight = $(document).height();

    const scrollPercent = (scrollTop + windowHeight) / documentHeight;

    if (scrollPercent >= 0.8 && (hasMore.article || hasMore.event || hasMore.job)) {
        loadMore();
    }
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


$("#news-feed-container").on("click", ".like-btn", function () {
    const $btn    = $(this);
    const itemId  = $btn.data("id");
    const itemType= $btn.data("type");     // 'article' | 'event' | 'job'
    const $card   = $btn.closest(".card");
    const $icon   = $btn.find("i");
    const $count  = $card.find(".like-number");
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]')?.value;

    $.ajax({
        url: `/api/${itemType}${itemType === 'job' ? 'posts' : 's'}/${itemId}/like/`,
        type: "POST",
        headers: { "X-CSRFToken": csrfToken },
        success: function (res) {
            $count.text(res.like_count);

            if (res.liked) {
                $icon.removeClass("fa-regular").addClass("fa-solid text-danger");
            } else {
                $icon.removeClass("fa-solid text-danger").addClass("fa-regular");
            }
            $btn.data("liked", res.liked);
        },
        error: function () {
            alert("Please log in to like this item.");
        }
    });
});
