import { getFormsetConfig } from './formset_config.js';
import { startSelect2 } from './utils/utils.js';

const { formsets: formsetJson } = getFormsetConfig();

/**
 * @param {HTMLElement} parentDiv HTML element that contains a formset's parent div
 * @returns {void} This function receives a parent div as a parameter and subtracts 1 to Django's hidden input
 * of initial formsets if the deletion involved a formset that was already in our DB.
 */
function subtractUponFormsetDelete(parentDiv, mainContainer_id) {
    const targetConfig = formsetJson[mainContainer_id];
    if (!targetConfig) return;

    let totalFormsHiddenInput = document.getElementById(targetConfig.total_forms_id);
    if (!totalFormsHiddenInput) return;

    totalFormsHiddenInput.value = parseInt(totalFormsHiddenInput.value) - 1;

    if(typeof parentDiv.getAttribute("name") !== "string") {
        let initialFormsHiddenInput = document.getElementById(targetConfig.initial_forms_id)

        if(initialFormsHiddenInput && initialFormsHiddenInput.value > 0) {
            initialFormsHiddenInput.value = parseInt(initialFormsHiddenInput.value) - 1;
        }
    }
}

/**
 *
 * @param {string} numberedString String with a number separated by hyphens
 * @param {number} counter The number that will replace the old one
 * @returns {string} This function receives a string with a number separated by hyphens and returns the same string
 * with its number replaced by the counter received as a parameter
 */
function renumberString(numberedString, counter) {

    // Change the number in the name/id of our formset's div. We'll split it, replace the last index, and join it again
    numberedString = numberedString.split("-")

    for(let index in numberedString) {
        if( !isNaN(numberedString[index]) ) {
            numberedString[index] = counter;
        }
    }

    numberedString = numberedString.join("-")
    return numberedString;

    // // We split the string, increase the last index, and join the split into a string again
    // numberedString = numberedString.split("-")
    // let maxIndex = numberedString.length - 1
    // numberedString[maxIndex] = counter
    // numberedString = numberedString.join("-")
    // return numberedString;
}

/**
 *
 * @param {string} numberedString String with a number separated by hyphens
 * @param {number} counter The number that will replace the old one
 * @returns {string} This function receives a string with a number separated by hyphens and returns the same string
 * with its number replaced by the counter received as a parameter
 */
function numberString(numberedString, counter) {

    // Change the number in the name/id of our formset's div. We'll split it, replace the last index, and join it again
    numberedString = numberedString.split("-")
    let foundPrefix = false;

    for(let index in numberedString) {
        if( numberedString[index] == '__prefix__' ) {
            numberedString[index] = counter;
            foundPrefix = true;
        }
    }

    numberedString = numberedString.join("-")

    if(!foundPrefix) {
        return renumberString(numberedString, counter);
    }
    return numberedString;
}

/**
 *
 * @param {string} fullString The string that conforms the ID of our HTML element
 * @returns Returns an array with the string of the ID without the number as the first index,
 * while the number at the end of our is located in the second index of our returned array
 */
function separateIdStringFromFinalIndex(fullString) {
    let splittedString = fullString.split("-")
    let finalIndex = splittedString.pop()                // Remove the last index from our
    return [splittedString.join("-"), finalIndex]
}

/**
 * @param {HTMLElement} mainContainer Main div that contains the various formsets' parent divs
 * @returns {void} This function receives a formset's class and resets the numbers of the
 * formsets and their inputs from index 0 to n
 */
function resetNumbers(mainContainer) {

    // Iterate all of the children (divs) inside the main container
    for(let index = 0; index < mainContainer.children.length; index++) {

        let formset = mainContainer.children[index]

        // Change the id of the formset's div (except for the first one since it has no id)
        if(formset.id !== "") {
            formset.id = renumberString(formset.id, index)

            // Finally, iterate and rename the inputs inside the parent divs of our formsets
            let parentDivs = formset.querySelectorAll("div")

            for(let i in parentDivs) {
                // I have no idea why, but a phantom function is iterated here, so we must check if we're looking at an object
                if(typeof parentDivs[i] === "object") {
                    // Change the number in the name/id of our formset's div. We'll split it, replace the last index, and join it again
                    let divId = parentDivs[i].id
                    let parentDiv = document.getElementById(divId)

                    if (parentDiv !== null) {
                        parentDiv.id = renumberString(divId, index)

                        // Get all nested tags that are inputs
                        let nestedInputs = parentDiv.parentElement.getElementsByTagName("input")
                        let nestedSelects = parentDiv.getElementsByTagName("select")
                        let nestedTextareas = parentDiv.getElementsByTagName("textarea")
                        let nestedLabels = parentDiv.getElementsByTagName("label")
                        let nestedParentDivs = parentDiv.getElementsByTagName("div")


                        // Iterate over all inputs and set their name/id attribute with the counter
                        for (let i = 0; i < nestedInputs.length; i++) {
                            // Set name
                            let inputName = nestedInputs[i].name
                            nestedInputs[i].name = numberString(inputName, index)

                            // Set id
                            let inputId = nestedInputs[i].id
                            nestedInputs[i].id = numberString(inputId, index)
                        }

                        // Iterate over all selects and set their name/id attribute with the counter
                        for (let i = 0; i < nestedSelects.length; i++) {
                            // Set name
                            let inputName = nestedSelects[i].name
                            nestedSelects[i].name = numberString(inputName, index)

                            // Set id
                            let inputId = nestedSelects[i].id
                            nestedSelects[i].id = numberString(inputId, index)
                        }
                        // Iterate over all textAreas and set their name/id attribute with the counter
                        for (let i = 0; i < nestedTextareas.length; i++) {
                            // Set name
                            let inputName = nestedTextareas[i].name
                            nestedTextareas[i].name = numberString(inputName, index)

                            // Set id
                            let inputId = nestedTextareas[i].id
                            nestedTextareas[i].id = numberString(inputId, index)
                        }
                        // Iterate over all labels and set their for attribute with the counter
                        for (let i = 0; i < nestedLabels.length; i++) {
                            // Set for
                            let inputFor = nestedLabels[i].htmlFor
                            nestedLabels[i].htmlFor = numberString(inputFor, index)
                        }
                        // Iterate over all parent divs and set their id attribute with the counter
                        for (let i = 0; i < nestedParentDivs.length; i++) {
                            // Set id
                            let inputId = nestedParentDivs[i].id
                            let finalId = numberString(inputId, index)
                            nestedParentDivs[i].id = finalId
                        }
                    }
                }
            }

            let hiddenInputs = mainContainer.children[index].querySelectorAll('[type="hidden"]');

            for (let i = 0; i < hiddenInputs.length; i++) {
                // Set name
                let inputName = hiddenInputs[i].name
                hiddenInputs[i].name = numberString(inputName, index)

                // Set id
                let inputId = hiddenInputs[i].id
                hiddenInputs[i].id = numberString(inputId, index)
            }
        }
    }
}

/**
 * @param {HTMLElement} mainContainer Main div that contains the various formsets' parent divs
 * @returns {void} This function receives a formset's class and resets the numbers of the
 * formsets from index 0 to n
 */
function resetParentDivNumbers(mainContainer) {

    // Iterate all of the children (divs) inside the main container
    for(let index = 0; index < mainContainer.children.length; index++) {

        let formset = mainContainer.children[index]

        // Change the id of the formset's div (except for the first one since it has no id)
        if(formset.id !== "") {
            formset.id = renumberString(formset.id, index)
        }
    }
}

/**
 *
 * @param {string} divId - The name of your parent div
 * @param {HTMLElement} inputDiv Parent div that includes the whole formset and its inputs
 * @param {HTMLElement} mainContainer Main div that contains the various formsets' parent divs
 * @param {number} counter - The number of the formset that will be created
 * @return {void} This function receives a formset div and clones it, then it inserts it at the end of the list
 */
function cloneFormset(divId, inputDiv, mainContainer, counter) {
    let clonedDivNode = inputDiv

    numberString(divId, counter)

    clonedDivNode.setAttribute("name", `${divId}`)
    clonedDivNode.setAttribute("id", `${divId}`)

    // Get all nested tags that are inputs
    let nestedInputs = clonedDivNode.getElementsByTagName("input")
    let nestedSelects = clonedDivNode.getElementsByTagName("select")
    let nestedTextareas = clonedDivNode.getElementsByTagName("textarea")
    let nestedLabels = clonedDivNode.getElementsByTagName("label")
    let nestedParentDivs = clonedDivNode.getElementsByTagName("div")

    // Iterate over all inputs and set their name/id attribute with the counter
    for (let i = 0; i < nestedInputs.length; i++) {
        // Set name
        let inputName = nestedInputs[i].name
        nestedInputs[i].name = numberString(inputName, counter)

        // Set id
        let inputId = nestedInputs[i].id
        nestedInputs[i].id = numberString(inputId, counter)
    }
    // Iterate over all selects and set their name/id attribute with the counter
    for (let i = 0; i < nestedSelects.length; i++) {
        // Set name
        let inputName = nestedSelects[i].name
        nestedSelects[i].name = numberString(inputName, counter)

        // Set id
        let inputId = nestedSelects[i].id
        nestedSelects[i].id = numberString(inputId, counter)
    }
    // Iterate over all textAreas and set their name/id attribute with the counter
    for (let i = 0; i < nestedTextareas.length; i++) {
        // Set name
        let inputName = nestedTextareas[i].name
        nestedTextareas[i].name = numberString(inputName, counter)

        // Set id
        let inputId = nestedTextareas[i].id
        nestedTextareas[i].id = numberString(inputId, counter)
    }
    // Iterate over all labels and set their for attribute with the counter
    for (let i = 0; i < nestedLabels.length; i++) {
        // Set for
        let inputFor = nestedLabels[i].htmlFor
        nestedLabels[i].htmlFor = numberString(inputFor, counter)
    }
    // Iterate over all parent divs and set their id attribute with the counter
    for (let i = 0; i < nestedParentDivs.length; i++) {
        // Set id
        let inputId = nestedParentDivs[i].id
        let finalId = numberString(inputId, counter)
        nestedParentDivs[i].id = finalId
    }

    clonedDivNode.value = counter
    mainContainer.appendChild(clonedDivNode)

    initDjangoSelect2(clonedDivNode);

    resetParentDivNumbers(mainContainer)
}

/**
 *
 * @param {string} templateId The id of the template div
 * @returns {void} Function that receives a template div and clones it to append at the corresponding
 * main container
 */
function generateFormsetHTML(templateId) {
    let templateElement = document.getElementById(templateId);
    if (!templateElement) return;

    // The HTMLElement of the div we clone
    let inputsDivToClone = templateElement.content.cloneNode(true);
    inputsDivToClone = inputsDivToClone.children[0];    // Parse from fragment to Object

    // Add 1 to the counter of our django hidden input
    const targetConfig = formsetJson[templateElement.dataset.container_target] || {};
    let mainContainerId = targetConfig.total_forms_id;

    let totalFormsHiddenInput = document.getElementById(mainContainerId);
    if (!totalFormsHiddenInput) return;

    totalFormsHiddenInput.value = parseInt(totalFormsHiddenInput.value) + 1;

    // Id of our HTML element
    let idOfParentDiv = inputsDivToClone.getAttribute("id");

    // An anchor to prepend the cloned div
    let testContainer = document.getElementById(templateElement.dataset.container_target);
    // We must use a callback so that we can pass arguments to the cloneFormset function
    cloneFormset(idOfParentDiv, inputsDivToClone, testContainer, totalFormsHiddenInput.value - 1);
}

/**
 * @param {HTMLElement} mainContainerElement - The string that will be modified
 * @param {HTMLElement} formsetParentDiv - The number that will be added to the string
 * @returns {void} This function the formset's main container and the formset's parent div
 * whose delete button was clicked and removes it from the DOM
*/
function deleteFormset(mainContainerElement, formsetParentDiv) {
    // Adjust the values in Django's hidden inputs (if it applies)
    subtractUponFormsetDelete(formsetParentDiv, mainContainerElement.id);

    // Remove HTML of the deleted formset
    formsetParentDiv.remove(formsetParentDiv);

    // Reset the id numeration of the formsets and their nested inputs
    resetNumbers(mainContainerElement);


    // reinitializeSelect2(mainContainerElement.id);
}


/**
 * @param {HTMLElement} formulario The form that will be submitted
 * @param {string} oneToNFormsets An array with the ids of the main containers of our formsets that must
 * always have at least one formset
 * @returns {void}
 */
function initialConfig(formulario) {

    // Button Click Logic
    formulario.addEventListener("click", (e) => {
        if (e.target.nodeName == 'BUTTON' || e.target.nodeName == 'I' || e.target.nodeName == 'SPAN' || e.target.nodeName == 'path' || e.target.nodeName == 'svg') {
            let button_parent = e.target.closest('BUTTON')
            if (!button_parent) return
            let dataset_template = button_parent.dataset.template

            if(dataset_template !== undefined) {
                // Add a new formset
                generateFormsetHTML(dataset_template)
            }
            else if (button_parent.classList.contains('delete-formset')) {
                let mainContainer = e.target
                let formsetParentDiv = mainContainer
                let first = false
                while (mainContainer && !Object.prototype.hasOwnProperty.call(formsetJson, mainContainer.id)) {
                    if (first) {
                        formsetParentDiv = mainContainer
                    }
                    mainContainer = mainContainer.parentElement
                    first = true
                }
                if (!mainContainer) return

                const targetConfig = formsetJson[mainContainer.id] || {};
                if(targetConfig.oneToNFormsets === true) {
                    if(mainContainer.children.length > 1) {
                        deleteFormset(mainContainer, formsetParentDiv)
                    }
                    else return
                }else{
                    deleteFormset(mainContainer, formsetParentDiv)
                }
            }
        }
    })
}


/**
 * @mainContainer {HTMLElement} The main container that holds the new formset
 * @returns {void} This function initializes Django Select2 in all select elements that are found in the new formset
 */
function initDjangoSelect2(mainContainer) {
    // Init Django Select2 in the cloned select elements if it applies
    const selects = $(mainContainer).find(".django-select2");
    if (selects.length > 0) {
        selects.djangoSelect2();
    }
}

export { separateIdStringFromFinalIndex, initialConfig }
