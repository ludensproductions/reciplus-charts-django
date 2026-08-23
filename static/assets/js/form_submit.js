document.addEventListener("DOMContentLoaded", function() {
    let processingMessage = JSON.parse(document.getElementById("processing_message").textContent);

    var form = document.getElementById("form-fixed-id") || document.querySelector("form[id^='form-']");
    if (form) {
        form.addEventListener("submit", function(event) {
            var submitButton = form.querySelector("button[type='submit'], input[type='submit']");
            if (submitButton) {
                submitButton.disabled = true;
                submitButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> ' + processingMessage;
            }
        });
    }
});
