document.addEventListener('DOMContentLoaded', function() {
    const switches = document.querySelectorAll('.toggle-switch');

    switches.forEach(function(switchElement) {
        switchElement.addEventListener('click', function(event) {
            event.preventDefault();

            const action = switchElement.dataset.action;
            const url = switchElement.dataset.url;

            if (action === 'disable') {
                $('#deleteForm').attr('action', url);
                $('#delete-modal').modal('show');
            } else if (action === 'enable') {
                $('#enableForm').attr('action', url);
                $('#enable-modal').modal('show');
            }
        });
    });
});
