const cleanErrors = (container) => {
    container.querySelectorAll('.is-invalid').forEach(elem => elem.classList.remove('is-invalid'))
}

const addErrorMsg = (input, errorStr) => {
    input.classList.add('is-invalid');
    document.querySelector(`#${input.id} + p>.error-msg`).textContent = errorStr;
}
