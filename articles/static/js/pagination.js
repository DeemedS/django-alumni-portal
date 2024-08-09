function createPagination(currentPage, totalPages, visiblePages) {
    $('#pagination').empty();
    
    function addPage(page, isActive = false) {
        var activeClass = isActive ? ' active' : '';
        var pageLink = '<li class="page-item' + activeClass + '"><a class="page-link" href="#" data-page="' + page + '">' + page + '</a></li>';
        $('#pagination').append(pageLink);
    }

    if (totalPages <= visiblePages) {
        for (var i = 1; i <= totalPages; i++) {
            addPage(i, i === currentPage);
        }
    } else {
        var startPage, endPage;
        
        if (currentPage <= Math.ceil(visiblePages / 2)) {
            startPage = 1;
            endPage = visiblePages - 1;
        } else if (currentPage + Math.floor(visiblePages / 2) >= totalPages) {
            startPage = totalPages - visiblePages + 2;
            endPage = totalPages;
        } else {
            startPage = currentPage - Math.floor(visiblePages / 2);
            endPage = currentPage + Math.floor(visiblePages / 2);
        }
        
        if (startPage > 1) {
            addPage(1);
            if (startPage > 2) {
                $('#pagination').append('<li class="page-item disabled"><span class="page-link">...</span></li>');
            }
        }

        for (var i = startPage; i <= endPage; i++) {
            addPage(i, i === currentPage);
        }
        
        if (endPage < totalPages) {
            if (endPage < totalPages - 1) {
                $('#pagination').append('<li class="page-item disabled"><span class="page-link">...</span></li>');
            }
            addPage(totalPages);
        }
    }
}