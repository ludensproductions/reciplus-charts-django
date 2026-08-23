let email = document.getElementById("email")
let password = document.getElementById("password")
let verifyPassword = document.getElementById("verifyPassword")
let submitBtn = document.getElementById("submitBtn")
let emailErrorMsg = document.getElementById('emailErrorMsg')
let passwordErrorMsg = document.getElementById('passwordErrorMsg')

let imagePreview = document.getElementById('img-preview')
let originalImage = imagePreview.src
let originalImageSplitCount = originalImage.split("/").length
let imageInput = document.getElementById('id_image')
let noImageText = document.getElementById("noImageText")
let clearImageButton = document.getElementById("clearImage")
let clearImageCheckBox = document.getElementById("image-clear_id")
let divIdImage = document.getElementById("div_id_image");
divIdImage.style.position = "absolute";

let imageErrorMsg = $('#error_1_id_image')
if(imageErrorMsg) {
    imageErrorMsg.appendTo("#errorMessagesDiv");
    imageErrorMsg.addClass("text-danger").removeClass("invalid-feedback");
}

// FUNCTIONS

function displayErrorMsg(type, msg) {
    if(type == "email") {
        emailErrorMsg.style.display = "block"
        emailErrorMsg.innerHTML = msg
        submitBtn.disabled = true
    }
    else {
        passwordErrorMsg.style.display = "block"
        passwordErrorMsg.innerHTML = msg
        submitBtn.disabled = true
    }
}

function hideErrorMsg(type) {
    if(type == "email") {
        emailErrorMsg.style.display = "none"
        emailErrorMsg.innerHTML = ""
        submitBtn.disabled = true
        if(passwordErrorMsg.innerHTML == "")
            submitBtn.disabled = false
    }
    else {
        passwordErrorMsg.style.display = "none"
        passwordErrorMsg.innerHTML = ""
        if(emailErrorMsg.innerHTML == "")
            submitBtn.disabled = false
    }
}

// Validate password upon change
password.addEventListener("input", function() {

    // If password has no value, then it won't be changed and no error will be displayed
    if(password.value.length == 0 && verifyPassword.value.length == 0) hideErrorMsg("password")

    // If password has a value, then it will be checked. In this case the passwords don't match
    else if(password.value !== verifyPassword.value) displayErrorMsg("password", "Las contraseñas no coinciden")

    // When the passwords match, we check the length
    else {
        // Check if the password has 8 characters or more
        if(password.value.length >= 8)
            hideErrorMsg("password")
        else
            displayErrorMsg("password", "La contraseña debe tener al menos 8 caracteres")
    }
})
verifyPassword.addEventListener("input", function() {
    if(password.value !== verifyPassword.value)
        displayErrorMsg("password", "Las contraseñas no coinciden")
    else {
        // Check if the password has 8 characters or more
        if(password.value.length >= 8)
            hideErrorMsg("password")
        else
            displayErrorMsg("password", "La contraseña debe tener al menos 8 caracteres")
    }
})

// Open Image Selection Upon Button Click
document.getElementById("photoBtn").addEventListener("click", function() {
    $("#id_image").click();
});

// Clear Image Script
if(clearImageButton) {
    clearImageButton.addEventListener("click", function() {
        clearImageCheckBox.checked = true;
        clearImageButton.disabled = true
        noImageText.style.display = "block"
        imagePreview.style.display = "none"
        imageInput.value = ""
    });
}

// Render Image Upon Change (Jquery) Script
imageInput.addEventListener("change", function() {
    if(this.files && this.files[0]) {
        var reader = new FileReader();
        reader.onload = function(e) {

            noImageText.style.display = "none"
            imagePreview.style.display = "inline";
            $('#img-preview').attr('src', e.target.result);
        }

        reader.readAsDataURL(this.files[0]);
        imageErrorMsg.hide();

        if(clearImageCheckBox) {
            clearImageCheckBox.checked = false;
            clearImageButton.disabled = false
        }
    }
    else {
        imagePreview.style.display = "none"
        noImageText.style.display = "block"

        if(clearImageCheckBox) {
            clearImageCheckBox.checked = true;
            clearImageButton.disabled = true
        }
    }
});
