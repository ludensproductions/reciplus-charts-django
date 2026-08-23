document.addEventListener("DOMContentLoaded", (evt) => {
    document.addEventListener("htmx:configRequest", function(event) {
        if (event.target.role !== "switch") {
            return;
        }
        event.target.disabled = true;
    });

    document.addEventListener("htmx:afterRequest", function(event) {
        // Check if event target is the checkbox for enabling/disabling
        if (event.target.role !== "switch") {
            return;
        }
        const response = event.detail.xhr.responseText;
        if (response === "ERROR") {
            event.target.checked = !event.target.checked;
        }
        location.reload();
    });
});
