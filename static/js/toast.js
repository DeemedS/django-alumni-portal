function showToast(title, message, type) {
    var toastHtml = `
        <div class="toast" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="toast-header">
                <strong class="me-auto text-${type}">${title}</strong>
                <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        </div>
        `;
        $('.toast-container').append(toastHtml);
        var toast = new bootstrap.Toast($('.toast').last()[0]);
        toast.show();
}