class ReservationEvents {
    constructor() {
        this.triggerElement = document.getElementById("id_reservation_type");

        this.dependantFields = {
            id_extra_fee: document.getElementById("id_extra_fee").closest(".col-xs-12.col-md-6.col-lg-4"),
            id_promotion_points: document.getElementById("id_promotion_points").closest(".col-xs-12.col-md-6.col-lg-4"),
        };

        this.dependantFieldsTriggerMap = {
            id_extra_fee: "unexpected",
            id_promotion_points: "standard",
        };

        this.defaultDependantFieldsValues = {
            id_extra_fee: 0.0,
            id_promotion_points: 0,
        };

        this._reservationTypeEvent = null;
        this.setEvents();

        // Run once at init
        this.updateVisibility(this.triggerElement.value);
    }

    setEvents() {
        this._reservationTypeEvent = (event) => {
            this.updateVisibility(event.target.value);
        };
        this.triggerElement.addEventListener("change", this._reservationTypeEvent);
    }

    updateVisibility(currentValue) {
        for (const [fieldId, triggerValue] of Object.entries(this.dependantFieldsTriggerMap)) {
            const element = this.dependantFields[fieldId];
            if (!element) continue;

            const input = element.querySelector("input, select, textarea");
            if (!input) continue;

            if (currentValue !== triggerValue) {
                // Reset and disable input
                input.value = this.defaultDependantFieldsValues[fieldId];
                input.disabled = true;

                // Add hidden fallback
                let hidden = document.createElement("input");
                hidden.type = "hidden";
                hidden.name = input.name;
                hidden.value = this.defaultDependantFieldsValues[fieldId];
                hidden.dataset.hiddenField = fieldId;

                // Remove old hidden fallback if any
                input.form.querySelectorAll(`[data-hidden-field="${fieldId}"]`).forEach(el => el.remove());

                input.form.appendChild(hidden);

                // Hide UI field
                element.style.display = "none";
            } else {
                // Enable input and remove hidden fallback
                input.disabled = false;
                input.form.querySelectorAll(`[data-hidden-field="${fieldId}"]`).forEach(el => el.remove());

                // Show UI field
                element.style.display = "";
            }
        }
    }
}

document.addEventListener("DOMContentLoaded", () => {
    new ReservationEvents();
});
