document.addEventListener("DOMContentLoaded", function () {
    const table = document.querySelector("#ipi-table");

    if (table && typeof DataTable !== "undefined") {
        const actionsLabel = JSON.parse(document.getElementById("actions_label").textContent);
        const emptyTableMessage = JSON.parse(document.getElementById("empty_table_message").textContent);

        const actionColumns = Array.from(table.querySelectorAll("thead th"))
            .map((header, index) => ({text: header.textContent.trim(), index}))
            .filter(({text}) => text === actionsLabel)
            .map(({index}) => index);

        new DataTable(table, {
            paging: false,
            searching: false,
            order: [],
            info: false,
            language: {emptyTable: emptyTableMessage},
            columnDefs: [{orderable: false, targets: actionColumns}],
        });
    }
});

function checkForm(form) {
    const submitButton = form.querySelector("#btn-registrar");
    if (!submitButton) return true;

    submitButton.disabled = true;
    window.setTimeout(() => { submitButton.disabled = false; }, 1000);
    return true;
}
