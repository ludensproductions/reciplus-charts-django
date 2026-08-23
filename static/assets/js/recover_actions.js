$(document).ready(function () {
    $(".btn-recover").on("click", function () {
        let id = $(this).data("id");
        let baseUrl = $(this).data("url");

        let finalUrl = baseUrl.replace("1", id);
        $("#recoverForm").attr("action", finalUrl);
    });

    $(".btn-recover-submit").on("click", function () {
        $("#recoverForm").submit();
    });
});
