document.body.addEventListener("htmx:wsAfterMessage", () => {
    const el = document.getElementById("chat-messages");
    el.scrollTop = el.scrollHeight;
});
