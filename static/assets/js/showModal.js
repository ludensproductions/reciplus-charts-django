let loadingSpinner = document.querySelector('#overlay-spinner')


; (function () {
    const modalShow = new bootstrap.Modal(document.getElementById('showModal'));

    htmx.on("htmx:beforeRequest", (e) => {

        loadingSpinner.style.visibility = 'visible';

    });


    htmx.on("htmx:afterSwap", (e) => {

        if (e.detail.target.id == "dialogModal") {
            loadingSpinner.style.visibility = 'hidden';
            modalShow.show();
        }
    });

    htmx.on("htmx:beforeSwap", (e) => {
        if (e.detail.target.id == "dialogModal" && e.detail.xhr.response == 200) {
            modalShow.hide();
            e.detail.shouldSwap = false;
            if (e.detail.xhr.status == 200){
                location.reload()
            }
        }
    });

    htmx.on("hidden.bs.modal", (e) => {
        const child_form = e.target.querySelector("#codigo_barra_form");

        if (child_form) {
            location.reload()
        }
        document.getElementById("dialogModal").innerHTML = "";
        // Check if the hidden modal contains the specific form

    });
})();
