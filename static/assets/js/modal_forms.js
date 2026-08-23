function setModalFormAction(formId, url) {
    const query = new URLSearchParams(window.location.search).toString();
    const form = document.getElementById(formId);
    if (form) form.action = query ? `${url}?${query}` : url;
}

function destroy(url) {
    setModalFormAction("deleteForm", url);
}

function enable(url) {
    setModalFormAction("enableForm", url);
}

function formSubmit() {
    document.getElementById("deleteForm")?.requestSubmit();
}

function enableFormSubmit() {
    document.getElementById("enableForm")?.requestSubmit();
}
