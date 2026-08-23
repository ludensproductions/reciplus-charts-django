
class UserEvents {
    constructor() {

        this.departamento = $('#id_departamento');
        this.puesto = $('#id_puesto');
        this.domicilioEstado = $('#id_domicilio-estado');
        this.domicilioMunicipio = $('#id_domicilio-municipio');
        this.domicilioCodigoPostal = $('#id_domicilio-codigo_postal');
        this.hasDomicilioInput = $('#id_has_domicile');
        this.domicilioForm = document.getElementById('domicilioForm');
        this.confirmModal = new bootstrap.Modal(document.getElementById('confirm-modal'));

        this.deleteDomicilio = false;
        this.deleteAddressLabel = JSON.parse(document.getElementById('deleteAddressLabel').textContent);
        this.addAddressLabel = JSON.parse(document.getElementById('addAddressLabel').textContent);
        this.textCollapser = `${this.deleteAddressLabel}:`;
        this.textExpander = `${this.addAddressLabel}:`;


        this.requiredDomicilioFields = [
            'id_domicilio-estado',
            'id_domicilio-municipio',
            'id_domicilio-colonia',
            'id_domicilio-codigo_postal',
            'id_domicilio-calle',
            'id_domicilio-numero_exterior',
        ]

        this.registerEvents();
        this.hasDomicilio();

    }

    registerEvents = () => {

        this.departamento.on('select2:clear', (e) => {
            this.puesto.val(null).trigger('change');
        });

        this.domicilioEstado.on('select2:clear', (e) => {
            this.domicilioMunicipio.val(null).trigger('change');
            this.domicilioCodigoPostal.val(null).trigger('change');
        });

        this.domicilioMunicipio.on('select2:clear', (e) => {
            this.domicilioMunicipio.val(null).trigger('change');
        });




        this.domicilioForm.addEventListener('show.bs.collapse', this.onColapseDomicilio);
        this.domicilioForm.addEventListener('hide.bs.collapse', this.onHideColapseDomicilio);
        document.getElementById('confirm-button-modal').addEventListener('click', this.onClickConfirmModal);
        document.getElementById('form-fixed-id').addEventListener('submit', this.onSubmitForm);


    };


    onSubmitForm = (e) => {
        const select = document.querySelector('#id_domicilio-codigo_postal');  // cambia el ID si es otro
        const selectedOption = select.options[select.selectedIndex];

        if (selectedOption && selectedOption.getAttribute('data-select2-tag') === 'true') {
            const rawValue = selectedOption.value;

            // Cambiamos el valor del option para que se envíe como "new_..."
            selectedOption.value = 'new_' + rawValue;
        }

        // Si necesitas hacer validaciones, puedes usar e.preventDefault() aquí
        // e.preventDefault();
    }

    hasDomicilio = () => {
        const hasDomicilioInput = document.getElementById('hasDomicilio');
        const hasDomicilio = JSON.parse(hasDomicilioInput.textContent);
        console.log(hasDomicilio);

        if (hasDomicilio) {
            this.openAcordeon();
            this.hasDomicilioInput.val("True").trigger('change');
        }else{
            this.deleteDomicilio = true;
            this.hasDomicilioInput.val("False").trigger('change');
        }
    }

    onColapseDomicilio = (e) => {
        const accordionLabel = document.getElementById('accordionLabel');
        accordionLabel.textContent = this.textCollapser;

        this.hasDomicilioInput.val("True").trigger('change');

        //set requiredd fields
        this.requiredDomicilioFields.forEach(field => {
            const fieldElement = document.getElementById(field);
            if (fieldElement) {
                fieldElement.setAttribute('required', 'required');
            }
            //add * to label
            const labelElement = document.querySelector(`label[for="${field}"]`);
            if (labelElement) {
                const labelText = labelElement.innerHTML.trim();
                if (!labelText.endsWith('*')) {
                    labelElement.innerHTML = labelText + '*';
                }
            }
        });
    }

    onHideColapseDomicilio = (e) => {
        const primaryKeyElement = document.getElementById('primaryKey');
        const primaryKey = JSON.parse(primaryKeyElement.textContent);

        if (!this.deleteDomicilio && primaryKey != null) {
            e.preventDefault();
            this.confirmModal.show();
            return;
        }

        this.hasDomicilioInput.val("False").trigger('change');
        accordionLabel.textContent = this.textExpander;

        //remove requiredd fields
        this.requiredDomicilioFields.forEach(field => {
            const fieldElement = document.getElementById(field);
            if (fieldElement) {
                fieldElement.removeAttribute('required');
            }
            //remove * to label
            const labelElement = document.querySelector(`label[for="${field}"]`);
            if (labelElement) {
                labelElement.innerHTML = labelElement.innerHTML.replace('*', '');
            }
        });

    }



    onClickConfirmModal = (e) => {

        this.confirmModal.hide(); // Hide the modal
        this.deleteDomicilio = true;
        this.hasDomicilioInput.val("False").trigger('change');
        this.closeAcordeon();


        const domicilioForm = document.querySelector('#domicilioForm');
        const inputs = domicilioForm.querySelectorAll('input');
        const selects = $(domicilioForm).find('select');

        inputs.forEach(input => {
            input.value = '';
        });

        //reset selects
        selects.each(function () {
            $(this).val(null).trigger('change');
        });

    }

    openAcordeon = () => {
        const domicilioForm = document.getElementById('domicilioForm');
        domicilioForm.classList.remove('collapse');
        domicilioForm.classList.add('show');
        const accordionLabel = document.getElementById('accordionLabel');
        accordionLabel.textContent = this.textCollapser;
    }

    closeAcordeon = () => {
        const domicilioForm = document.getElementById('domicilioForm');
        domicilioForm.classList.remove('show');
        domicilioForm.classList.add('collapse');
        const accordionLabel = document.getElementById('accordionLabel');
        accordionLabel.textContent = this.textExpander;
    }


}

new UserEvents();
