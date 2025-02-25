function createPagination(currentPage, totalPages, visiblePages) {
    $('#pagination').empty();

    function addPage(page, isActive = false, isDisabled = false, text = null) {
        let activeClass = isActive ? ' active' : '';
        let disabledClass = isDisabled ? ' disabled' : '';
        let displayText = text || page;
        let pageLink = `<li class="page-item${activeClass}${disabledClass}">
                            <a class="page-link" href="#" data-page="${page}">${displayText}</a>
                        </li>`;
        $('#pagination').append(pageLink);
    }

    addPage(currentPage - 1, false, currentPage === 1, '&laquo;');

    let startPage, endPage;
    let halfVisible = Math.floor(visiblePages / 2);

    if (currentPage <= halfVisible + 1) {
        startPage = 1;
        endPage = Math.min(visiblePages, totalPages);
    } else if (currentPage + halfVisible >= totalPages) {
        startPage = totalPages - visiblePages + 1;
        endPage = totalPages;
    } else {
        startPage = currentPage - halfVisible;
        endPage = currentPage + halfVisible;
    }

    if (startPage > 1) {
        addPage(1);
        if (startPage > 2) {
            $('#pagination').append('<li class="page-item disabled"><span class="page-link">...</span></li>');
        }
    }

    for (let i = startPage; i <= endPage; i++) {
        addPage(i, i === currentPage);
    }

    if (endPage < totalPages) {
        if (endPage < totalPages - 1) {
            $('#pagination').append('<li class="page-item disabled"><span class="page-link">...</span></li>');
        }
        addPage(totalPages);
    }

    addPage(currentPage + 1, false, currentPage === totalPages, '&raquo;'); // Next Button
}
