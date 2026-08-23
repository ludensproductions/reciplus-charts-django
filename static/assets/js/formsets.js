import { getFormsetConfig } from './formset_config.js'
import { separateIdStringFromFinalIndex, initialConfig } from './formsetFunctions.js'


const { formId: currentFormId } = getFormsetConfig();

/**
 * Method that sets the value of options that are tags as "new_" + value to identify new objects in the backend.
 *
 * @param {SubmitEvent} evt The event of the form when is submitted.
 */
const changeValues = (evt) => {
    const select2fields = document.querySelectorAll("option[data-select2-tag=\"true\"]");
    select2fields.forEach((select2option) => {
        if (select2option && select2option.getAttribute("data-select2-tag") === "true") {
            const rawValue = select2option.value;

            // Cambiamos el valor del option para que se envíe como "new_..."
            select2option.value = "new_" + rawValue;
        }
    });
}

function initializeFormsets() {
    const mainForm = document.getElementById(currentFormId);
    if (!mainForm) return;

    mainForm.addEventListener("input", (event) => {
        const [initialString, selectIndex] = separateIdStringFromFinalIndex(event.target.id);

        if (initialString == 'id_select') {
            const hiddenInput = document.getElementById(`id_hidden-${selectIndex}`);
            if (hiddenInput) hiddenInput.hidden = (event.target.value !== '3');
        }
    });

    mainForm.addEventListener("submit", changeValues);
    initialConfig(mainForm);
}

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initializeFormsets);
} else {
    initializeFormsets();
}
