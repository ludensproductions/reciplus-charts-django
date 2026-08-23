async function makeRequest(url, options = {}) {
    const defaultOptions = {
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken, // Comes from the definition that notification already uses.
        },
    };

    const mergedOptions = { ...defaultOptions, ...options };

    try {
        const response = await fetch(url, mergedOptions);

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
    } catch (error) {
        console.error("Request failed:", error);
        throw error;
    }
}

document.addEventListener("DOMContentLoaded", (evt) => {
    const emitActivityButton = document.getElementById("emit-activity-btn");
    const apiBaseUrl = emitActivityButton?.dataset.apiUrl;

    if (!emitActivityButton || !apiBaseUrl) return;

    emitActivityButton.addEventListener("click", async (evt) => {
        await makeRequest(apiBaseUrl, {method: "POST"});
    });
});
