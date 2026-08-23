function setBanAction(url, userName, isBanned) {
    let queryParams = new URLSearchParams(window.location.search);
    url = url + "?" + queryParams.toString();

    const banForm = $("#banForm");
    banForm.attr("action", url);

    const unbanTitle = banForm.data("unban-title");
    const unbanConfirm = banForm.data("unban-confirm");
    const unbanBody = banForm.data("unban-body");
    const banTitle = banForm.data("ban-title");
    const banConfirm = banForm.data("ban-confirm");
    const banBody = banForm.data("ban-body");
    const banBodySuffix = banForm.data("ban-body-suffix");

    if (isBanned) {
        $("#banModalTitle").text(unbanTitle);
        $("#banModalBody").text(unbanBody + " " + userName + "?");
        $("#banModalConfirmBtn").text(unbanConfirm);
        $("#banModalConfirmBtn").removeClass("btn-danger").addClass("btn-warning");
    } else {
        $("#banModalTitle").text(banTitle);
        $("#banModalBody").text(banBody + " " + userName + "? " + banBodySuffix);
        $("#banModalConfirmBtn").text(banConfirm);
        $("#banModalConfirmBtn").removeClass("btn-warning").addClass("btn-danger");
    }
}

function banFormSubmit() {
    $("#banForm").submit();
}
