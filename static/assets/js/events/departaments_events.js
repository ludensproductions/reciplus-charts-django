
class DepartamentEvents {
    constructor() {

        this.formsetId = document.getElementById('list_position');

        this.checkFirstCheckbox();
        this.registerEvents();

    }

    registerEvents = () => {
        this.formsetId.addEventListener('click', this.onChangeIsJefe);
    };

    onChangeIsJefe = (e) => {
        if (e.target.type !== 'checkbox') return;

        // if is checked then uncheck the others
        if (e.target.checked){
            const checkboxes = this.formsetId.querySelectorAll('input[type="checkbox"]');
            checkboxes.forEach(checkbox => {
                if (checkbox !== e.target){
                    checkbox.checked = false;
                }
            });
        };
    }

    checkFirstCheckbox = () => {
        const checkboxes = this.formsetId.querySelectorAll('input[type="checkbox"]');
        let checked = false;
        checkboxes.forEach(checkbox => {
            if (checkbox.checked) checked = true;
        });
        if (!checked) {
            checkboxes[0].checked = true;
        }
    }

}

new DepartamentEvents();

    

