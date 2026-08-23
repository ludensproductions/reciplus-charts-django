export function changeDisplayParent(element, display, required = false) {

    if (typeof element === 'string') {
        element = document.getElementById(element);
    }

    element.value = '';


    let labelElement = element.parentElement.querySelector(`label[for="${element.id}"]`);

    if (required) {
        labelElement.innerHTML = `${labelElement.innerHTML.trim()}*`
    }else{
        labelElement.innerHTML = labelElement.innerHTML.trim().replace('*', '');
    }

    return element.parentElement.parentElement.parentElement.parentElement.style.display = display;
}


export function markRequiredWithId(id, required = true) {
    let labelElement = document.querySelector(`#${id}`);

    labelElement.innerHTML = labelElement.innerHTML.trim().replace('*', '');

    if (required) {
        labelElement.innerHTML = `${labelElement.innerHTML.trim()}*`
    }
}



export function removeError(section_id=null) {
    let elements = document.querySelectorAll('.error-message');

    if (section_id) {
        elements = document.querySelectorAll(`#${section_id} .error-message`);
    }

    elements.forEach((element) => {
        element.remove();
    });
}




export function handleKeyDown(event) {
    if (event.target && event.target.type === 'number') {
        let maxValue = event.target.getAttribute('max');
        let currentValue = event.target.value;

        const keyCode = event.key;

        if (['e', '-', '+', '*', '/'].includes(keyCode)) event.preventDefault();

        if (isNaN(keyCode) && keyCode != '.') return

        if (!maxValue) return;

        currentValue = currentValue + keyCode;

        const currentValueLenght = currentValue.length;

        if (currentValue.includes('.')){

            const [integerCurrent, decimalCurrent] = currentValue.split('.');
            const [integerMax, decimalMax] = maxValue.split('.');

            console.log(decimalCurrent.length, decimalMax.length);

            if (decimalCurrent.length > decimalMax.length) event.preventDefault();

            if (integerCurrent > integerMax)  event.preventDefault();

        }else {
            if (maxValue.includes('.')) {
                if (currentValueLenght > maxValue.split('.')[0].length) {
                    event.target.value = currentValue.slice(0, 7) + '.' + currentValue.slice(7);
                    event.preventDefault();
                }

            }else{
                if (currentValueLenght > maxValue.length) {
                    event.preventDefault();
                }

            }

        }

    }else if (event.target && event.target.type === 'text') {

        //validate if key match with regex
        let regex = event.target.getAttribute('pattern');
        let value = event.target.value;
        let keyCode = event.key;
        if (keyCode === 'Backspace' || keyCode === 'Delete') return;
        if (!regex) return;
        const reg = new RegExp(regex);
        // if (!reg.test(value + keyCode)) event.preventDefault();


    }
}


export function handlePaste(event) {
    if (event.target && event.target.type === 'number') {
        let maxValue = event.target.getAttribute('max');

        // Get the pasted text
        const pastedText = (event.clipboardData).getData('text');
        const targetValue = event.target.value;
        // Check if the pasted text is a valid number
        if (isNaN(pastedText)) {
            event.preventDefault();
            return;
        }

        maxValue = maxValue.length
        const currentValueLenght = targetValue.length + pastedText.length;
        const newvalue = targetValue + pastedText;

        if (currentValueLenght >= maxValue ) {
            event.preventDefault();
            event.target.value = newvalue.substring(0, 7);
        }
    }else if (event.target && event.target.type === 'text') {
        let regex = event.target.getAttribute('pattern');
        let value = event.target.value;
        let pastedText = (event.clipboardData).getData('text');
        if (!regex) return;
        const reg = new RegExp(regex);
        if (!reg.test(value + pastedText)) event.preventDefault();
    }
}


export function addSingleError(element, errorMessage) {
    const PTag = document.createElement('p');
    PTag.classList.add('error-message');
    PTag.classList.add('text-danger');
    PTag.innerHTML = errorMessage;
    element.parentElement.appendChild(PTag);

}

export function removeSingleError(element) {
    let error = element.parentElement.querySelectorAll('.error-message');

    error.forEach((e) => {
        e.remove();
    });
}



export function getBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => resolve(reader.result);
        reader.onerror = error => reject(null);
    });
}



export function startSelect2(input, options = {}){
    input.select2({
        theme: "bootstrap-5",
        width: 'element',
        closeOnSelect: false,
        allowClear: true,
        placeholder: "---------",
        language: {
            noResults: function () {
                return "No se encontraron resultados";
            },
            searching: function () {
                return 'Buscando...';
            },
            errorLoading: function () {
                return 'No se pudieron cargar los resultados';
            },
        },
        ...options
    });
    // console.log(input.data('select2').$container);
    // const width = input.data('select2').$container.css('width');
    // console.log(width);
    // input.data('select2').$container.css('width', width);
}

export function toggleLoadingScreen (visible) {
    let loadingSpinner = document.querySelector('#overlay-spinner')
    if (visible) {
        loadingSpinner.style.visibility = 'visible';
    } else {
        loadingSpinner.style.visibility = 'hidden';
    }
}
