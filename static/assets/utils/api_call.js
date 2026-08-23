const callJsonApiView = async (url, csrfToken, method="GET", bodyJson=null) => {
    const options = {
        method: method,
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        }
    };
    if(bodyJson) {
        options['body'] = JSON.stringify(bodyJson);
    }
    const response = await fetch(url, options)
    return await response.json()
}

const callFormDataApiView = async (url, csrfToken, method="GET", bodyFormData = null) => {
    const options = {
        method: method,
        headers: {
            'X-CSRFToken': csrfToken,
        }
    };
    if(bodyFormData) {
        options['body'] = bodyFormData;
    }
    const response = await fetch(url, options)
    return await response.json()
}
