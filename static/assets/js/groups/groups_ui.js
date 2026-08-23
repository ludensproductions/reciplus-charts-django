const searchInput = document.getElementById("search-permissions");
const searchCurrentPermissionInput = document.getElementById("search-current-permissions");
const moveToCurrent = document.getElementById("move-to-current");
const moveToAll = document.getElementById("move-to-all");
const form = document.getElementById("form_id");
const nameInput = document.getElementById("id_display_name");

window.onload = function() {
    setListeners();
    form.setAttribute("novalidate", "");
}

function setListeners() {
    searchInput.addEventListener("input", function(e) {
        return onInputSearchPermission(searchInput, "#all-permission");
    });
    searchCurrentPermissionInput.addEventListener("input", function(e) {
        return onInputSearchPermission(searchCurrentPermissionInput, "#current-permission");
    });

    moveToCurrent.addEventListener("click", function(e) {
        onClickMoveTo("#all-permission", "#current-permission");
    });
    moveToAll.addEventListener("click", function(e) {
        onClickMoveTo("#current-permission", "#all-permission");
    });

    form.addEventListener("submit", onSubmitForm, false);
}

function onSubmitForm(e){
    if (!form.checkValidity()) {
        e.preventDefault()
        e.stopPropagation()
        // send user to the h1 element
        const topElement = document.querySelector("h1") || form;
        topElement.scrollIntoView();
    }

    form.classList.add('was-validated')


    if (nameInput.value.trim() === "") {

        return;
    }


    const currentPermissions = document.querySelectorAll("#current-permission .StackedListContent p");
    const input = document.createElement("select");
    input.name = "permissions";
    input.id = "id_permissions";
    input.multiple = true;
    input.style.display = "none";

    currentPermissions.forEach(permission => {
        const option = document.createElement("option");
        option.value = permission.dataset.permid;
        option.selected = true;
        input.appendChild(option);
    });

    form.appendChild(input);
    console.log(form);
    // form.submit();
}



function onClickMoveTo(source, destination){
    const destinationElement = document.querySelector(`${destination} .StackedList`);
    const permissions = document.querySelectorAll(`${source} .item-selected`);

    permissions.forEach(permission => {
        permission.classList.remove("item-selected");
        destinationElement.prepend(permission);
        permission.classList.remove("item-selected");
    });
}


function onInputSearchPermission(input, container){
    const val = input.value.toLowerCase();
    const permissions = document.querySelectorAll(`${container} .StackedListContent p`);

    permissions.forEach(permission => {
        const text = permission.textContent.toLowerCase();
        const li = permission.parentElement.parentElement;
        if(text.includes(val)){
            li.style.display = "block";
        }else{
            li.style.display = "none";
        }
    });
}
