class ContentsEvents {
    constructor() {
        this.triggerElement = document.getElementById("id_content_type");

        this.dependantForms = {
            article_form: document.getElementById("article-form"),
            video_form: document.getElementById("video-form"),
        };

        this.dependantFormsTriggerMap = {
            article_form: "article",
            video_form: "video",
        };

        this._contentTypeEvent = null;
        this.setEvents();

        // Run once at init
        this.updateVisibility(this.triggerElement.value);
    }

    setEvents() {
        this._contentTypeEvent = (event) => {
            this.updateVisibility(event.target.value);
        };
        this.triggerElement.addEventListener("change", this._contentTypeEvent);
    }

    updateVisibility(currentValue) {
        for (const [formId, triggerValue] of Object.entries(this.dependantFormsTriggerMap)) {
            const formContainer = this.dependantForms[formId];
            if (!formContainer) continue;

            // Get all inputs in the form section
            const inputs = formContainer.querySelectorAll("input, select, textarea");

            const isActive = currentValue === triggerValue;

            if (isActive) {
                // Show and enable all fields
                formContainer.style.display = "";
                inputs.forEach((input) => {
                    input.disabled = false;
                    // remove fallback hidden if exists
                    const hidden = input.form.querySelector(`[data-hidden-field="${input.name}"]`);
                    if (hidden) hidden.remove();
                });
            } else {
                // Hide and disable all fields
                formContainer.style.display = "none";
                inputs.forEach((input) => {
                    input.disabled = true;

                    // Add hidden fallback field (so value can safely clear)
                    let hidden = document.createElement("input");
                    hidden.type = "hidden";
                    hidden.name = input.name;
                    hidden.value = ""; // reset value
                    hidden.dataset.hiddenField = input.name;

                    // Remove any previous hidden with same name
                    input.form.querySelectorAll(`[data-hidden-field="${input.name}"]`).forEach(el => el.remove());
                    input.form.appendChild(hidden);
                });
            }
        }
    }
}

document.addEventListener("DOMContentLoaded", () => {
    new ContentsEvents();
});
